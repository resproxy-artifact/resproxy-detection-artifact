/*
 * ngx_http_proxy_detect_module.c
 *
 * Server-side residential proxy detection via TLS timing analysis.
 *
 * Measures the time gap between TCP accept and TLS ClientHello arrival.
 * Direct connections send ClientHello immediately (< 6ms), while proxied
 * connections exhibit a full RTT delay (100-300ms) because the proxy must
 * relay the SYN-ACK to the real client before receiving the ClientHello.
 *
 * Three operating modes:
 *   monitor - log only, no action (default)
 *   header  - inject X-Proxy-* headers into backend requests
 *   block   - reject proxied connections with configurable HTTP error
 *
 * Directives:
 *   proxy_detect on|off;                    (default: off)
 *   proxy_detect_threshold <ms>;            (default: 6)
 *   proxy_detect_mode monitor|header|block; (default: monitor)
 *   proxy_detect_block_code <code>;         (default: 403)
 *   proxy_detect_block_message "<text>";    (default: empty)
 *
 * Variables:
 *   $proxy_detect_gap_ms   - ACK-to-ClientHello gap (ms, 1 decimal)
 *   $proxy_detect_score    - normalized score 0.00-1.00
 *   $proxy_detect_flag     - "direct" or "proxied"
 *   $proxy_detect_tcp_rtt  - kernel TCP RTT estimate (ms, 1 decimal)
 */

#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>
#include <time.h>
#include <netinet/tcp.h>


/* Mode constants */
#define NGX_HTTP_PROXY_DETECT_MONITOR  0
#define NGX_HTTP_PROXY_DETECT_HEADER   1
#define NGX_HTTP_PROXY_DETECT_BLOCK    2


/* Per-connection measurement data, stored via SSL ex_data */
typedef struct {
    ngx_msec_int_t  gap_ms;        /* whole milliseconds */
    ngx_uint_t      gap_frac;      /* tenths of ms (0-9) */
    ngx_uint_t      tcp_rtt_us;    /* TCP RTT in microseconds from TCP_INFO */
    unsigned        measured:1;
} ngx_http_proxy_detect_conn_ctx_t;


/* Server-level configuration */
typedef struct {
    ngx_flag_t  enable;
    ngx_uint_t  threshold;         /* ms */
    ngx_uint_t  mode;              /* monitor=0, header=1, block=2 */
    ngx_uint_t  block_code;        /* HTTP status for block mode */
    ngx_str_t   block_message;     /* response body for block mode */
} ngx_http_proxy_detect_srv_conf_t;


/* SSL ex_data index */
static int  ngx_http_proxy_detect_ssl_index = -1;


/* Forward declarations */
static ngx_int_t ngx_http_proxy_detect_preconfiguration(ngx_conf_t *cf);
static ngx_int_t ngx_http_proxy_detect_postconfiguration(ngx_conf_t *cf);
static void *ngx_http_proxy_detect_create_srv_conf(ngx_conf_t *cf);
static char *ngx_http_proxy_detect_merge_srv_conf(ngx_conf_t *cf,
    void *parent, void *child);

static ngx_int_t ngx_http_proxy_detect_gap_variable(ngx_http_request_t *r,
    ngx_http_variable_value_t *v, uintptr_t data);
static ngx_int_t ngx_http_proxy_detect_score_variable(ngx_http_request_t *r,
    ngx_http_variable_value_t *v, uintptr_t data);
static ngx_int_t ngx_http_proxy_detect_flag_variable(ngx_http_request_t *r,
    ngx_http_variable_value_t *v, uintptr_t data);
static ngx_int_t ngx_http_proxy_detect_rtt_variable(ngx_http_request_t *r,
    ngx_http_variable_value_t *v, uintptr_t data);

static void ngx_http_proxy_detect_ssl_cb(const SSL *ssl_conn,
    int where, int ret);
static ngx_int_t ngx_http_proxy_detect_access_handler(ngx_http_request_t *r);


/* Mode enum for ngx_conf_set_enum_slot */
static ngx_conf_enum_t ngx_http_proxy_detect_modes[] = {
    { ngx_string("monitor"), NGX_HTTP_PROXY_DETECT_MONITOR },
    { ngx_string("header"),  NGX_HTTP_PROXY_DETECT_HEADER },
    { ngx_string("block"),   NGX_HTTP_PROXY_DETECT_BLOCK },
    { ngx_null_string, 0 }
};


/* Directives */
static ngx_command_t ngx_http_proxy_detect_commands[] = {

    { ngx_string("proxy_detect"),
      NGX_HTTP_MAIN_CONF|NGX_HTTP_SRV_CONF|NGX_CONF_FLAG,
      ngx_conf_set_flag_slot,
      NGX_HTTP_SRV_CONF_OFFSET,
      offsetof(ngx_http_proxy_detect_srv_conf_t, enable),
      NULL },

    { ngx_string("proxy_detect_threshold"),
      NGX_HTTP_MAIN_CONF|NGX_HTTP_SRV_CONF|NGX_CONF_TAKE1,
      ngx_conf_set_num_slot,
      NGX_HTTP_SRV_CONF_OFFSET,
      offsetof(ngx_http_proxy_detect_srv_conf_t, threshold),
      NULL },

    { ngx_string("proxy_detect_mode"),
      NGX_HTTP_MAIN_CONF|NGX_HTTP_SRV_CONF|NGX_CONF_TAKE1,
      ngx_conf_set_enum_slot,
      NGX_HTTP_SRV_CONF_OFFSET,
      offsetof(ngx_http_proxy_detect_srv_conf_t, mode),
      &ngx_http_proxy_detect_modes },

    { ngx_string("proxy_detect_block_code"),
      NGX_HTTP_MAIN_CONF|NGX_HTTP_SRV_CONF|NGX_CONF_TAKE1,
      ngx_conf_set_num_slot,
      NGX_HTTP_SRV_CONF_OFFSET,
      offsetof(ngx_http_proxy_detect_srv_conf_t, block_code),
      NULL },

    { ngx_string("proxy_detect_block_message"),
      NGX_HTTP_MAIN_CONF|NGX_HTTP_SRV_CONF|NGX_CONF_TAKE1,
      ngx_conf_set_str_slot,
      NGX_HTTP_SRV_CONF_OFFSET,
      offsetof(ngx_http_proxy_detect_srv_conf_t, block_message),
      NULL },

    ngx_null_command
};


/* Module context */
static ngx_http_module_t ngx_http_proxy_detect_module_ctx = {
    ngx_http_proxy_detect_preconfiguration,     /* preconfiguration */
    ngx_http_proxy_detect_postconfiguration,    /* postconfiguration */

    NULL,                                       /* create main conf */
    NULL,                                       /* init main conf */

    ngx_http_proxy_detect_create_srv_conf,      /* create srv conf */
    ngx_http_proxy_detect_merge_srv_conf,       /* merge srv conf */

    NULL,                                       /* create loc conf */
    NULL                                        /* merge loc conf */
};


/* Module definition */
ngx_module_t ngx_http_proxy_detect_module = {
    NGX_MODULE_V1,
    &ngx_http_proxy_detect_module_ctx,
    ngx_http_proxy_detect_commands,
    NGX_HTTP_MODULE,
    NULL, NULL, NULL, NULL,
    NULL, NULL, NULL,
    NGX_MODULE_V1_PADDING
};


/* ========================================================================
 * Variables
 * ======================================================================== */

static ngx_http_variable_t ngx_http_proxy_detect_vars[] = {

    { ngx_string("proxy_detect_gap_ms"), NULL,
      ngx_http_proxy_detect_gap_variable, 0, 0, 0 },

    { ngx_string("proxy_detect_score"), NULL,
      ngx_http_proxy_detect_score_variable, 0, 0, 0 },

    { ngx_string("proxy_detect_flag"), NULL,
      ngx_http_proxy_detect_flag_variable, 0, 0, 0 },

    { ngx_string("proxy_detect_tcp_rtt"), NULL,
      ngx_http_proxy_detect_rtt_variable, 0, 0, 0 },

      ngx_http_null_variable
};


static ngx_int_t
ngx_http_proxy_detect_preconfiguration(ngx_conf_t *cf)
{
    ngx_http_variable_t  *var, *v;

    for (v = ngx_http_proxy_detect_vars; v->name.len; v++) {
        var = ngx_http_add_variable(cf, &v->name, v->flags);
        if (var == NULL) {
            return NGX_ERROR;
        }

        var->get_handler = v->get_handler;
        var->data = v->data;
    }

    return NGX_OK;
}


/* ========================================================================
 * Configuration
 * ======================================================================== */

static ngx_int_t
ngx_http_proxy_detect_postconfiguration(ngx_conf_t *cf)
{
    ngx_http_handler_pt        *h;
    ngx_http_core_main_conf_t  *cmcf;

    /* Allocate SSL ex_data index (once) */
    if (ngx_http_proxy_detect_ssl_index == -1) {
        ngx_http_proxy_detect_ssl_index =
            SSL_get_ex_new_index(0, NULL, NULL, NULL, NULL);

        if (ngx_http_proxy_detect_ssl_index == -1) {
            ngx_log_error(NGX_LOG_EMERG, cf->log, 0,
                          "proxy_detect: SSL_get_ex_new_index() failed");
            return NGX_ERROR;
        }
    }

    /* Register access phase handler */
    cmcf = ngx_http_conf_get_module_main_conf(cf, ngx_http_core_module);

    h = ngx_array_push(&cmcf->phases[NGX_HTTP_ACCESS_PHASE].handlers);
    if (h == NULL) {
        return NGX_ERROR;
    }

    *h = ngx_http_proxy_detect_access_handler;

    return NGX_OK;
}


static void *
ngx_http_proxy_detect_create_srv_conf(ngx_conf_t *cf)
{
    ngx_http_proxy_detect_srv_conf_t  *conf;

    conf = ngx_pcalloc(cf->pool, sizeof(ngx_http_proxy_detect_srv_conf_t));
    if (conf == NULL) {
        return NULL;
    }

    conf->enable = NGX_CONF_UNSET;
    conf->threshold = NGX_CONF_UNSET_UINT;
    conf->mode = NGX_CONF_UNSET_UINT;
    conf->block_code = NGX_CONF_UNSET_UINT;

    return conf;
}


static char *
ngx_http_proxy_detect_merge_srv_conf(ngx_conf_t *cf, void *parent, void *child)
{
    ngx_http_proxy_detect_srv_conf_t  *prev = parent;
    ngx_http_proxy_detect_srv_conf_t  *conf = child;
    ngx_http_ssl_srv_conf_t           *sscf;

    ngx_conf_merge_value(conf->enable, prev->enable, 0);
    ngx_conf_merge_uint_value(conf->threshold, prev->threshold, 6);
    ngx_conf_merge_uint_value(conf->mode, prev->mode,
                              NGX_HTTP_PROXY_DETECT_MONITOR);
    ngx_conf_merge_uint_value(conf->block_code, prev->block_code, 403);
    ngx_conf_merge_str_value(conf->block_message, prev->block_message, "");

    /*
     * Install the SSL info callback on EVERY server's SSL_CTX, not just
     * those with proxy_detect enabled. This is necessary because nginx's
     * SNI handling fires SSL_CB_HANDSHAKE_START on the default server's
     * CTX before switching to the target server's CTX. The callback just
     * measures timing (cheap), and the variable/access handlers check
     * conf->enable before acting on the results.
     *
     * SSL ex_data persists across SSL_set_SSL_CTX (SNI context switch),
     * so measurements taken on the default CTX are readable from any
     * server's request handler.
     */
    sscf = ngx_http_conf_get_module_srv_conf(cf, ngx_http_ssl_module);

    if (sscf != NULL && sscf->ssl.ctx != NULL) {
        SSL_CTX_set_info_callback(sscf->ssl.ctx, ngx_http_proxy_detect_ssl_cb);
    }

    if (!conf->enable) {
        return NGX_CONF_OK;
    }

    if (sscf == NULL || sscf->ssl.ctx == NULL) {
        ngx_log_error(NGX_LOG_WARN, cf->log, 0,
                      "proxy_detect: SSL not configured, module disabled");
        conf->enable = 0;
        return NGX_CONF_OK;
    }

    ngx_log_error(NGX_LOG_NOTICE, cf->log, 0,
                  "proxy_detect: enabled (mode=%s, threshold=%ui ms)",
                  conf->mode == NGX_HTTP_PROXY_DETECT_BLOCK   ? "block"   :
                  conf->mode == NGX_HTTP_PROXY_DETECT_HEADER  ? "header"  :
                                                                "monitor",
                  conf->threshold);

    return NGX_CONF_OK;
}


/* ========================================================================
 * SSL info callback — timing measurement core
 *
 * Fires at SSL_CB_HANDSHAKE_START when SSL_do_handshake() begins.
 * At this point the ClientHello has arrived at the kernel and nginx has
 * read it into the SSL BIO.
 *
 * Accept time is derived from the connection's read timer:
 *   timer.key = ngx_current_msec_at_accept + client_header_timeout
 *   => accept_ms = timer.key - client_header_timeout
 *
 * c->data points to ngx_http_connection_t during the handshake
 * (before any HTTP request is created), giving us access to conf_ctx.
 * ======================================================================== */

static void
ngx_http_proxy_detect_ssl_cb(const SSL *ssl_conn, int where, int ret)
{
    ngx_connection_t                   *c;
    ngx_http_connection_t              *hc;
    ngx_http_core_srv_conf_t           *cscf;
    ngx_http_proxy_detect_conn_ctx_t   *ctx;
    struct timespec                     ts;
    ngx_msec_t                          now_ms, accept_ms, timeout;
    ngx_msec_int_t                      gap_ms;
    ngx_uint_t                          gap_frac;
    struct tcp_info                     ti;
    socklen_t                           ti_len;

    if (!(where & SSL_CB_HANDSHAKE_START)) {
        return;
    }

    c = ngx_ssl_get_connection((ngx_ssl_conn_t *) ssl_conn);
    if (c == NULL) {
        return;
    }

    /* Only measure the initial handshake, skip renegotiation/resumption */
    ctx = SSL_get_ex_data((SSL *) ssl_conn, ngx_http_proxy_detect_ssl_index);
    if (ctx != NULL) {
        return;
    }

    ctx = ngx_pcalloc(c->pool, sizeof(ngx_http_proxy_detect_conn_ctx_t));
    if (ctx == NULL) {
        return;
    }

    hc = (ngx_http_connection_t *) c->data;

    if (c->read->timer_set && hc != NULL && hc->conf_ctx != NULL) {

        /* Look up client_header_timeout */
        cscf = (ngx_http_core_srv_conf_t *)
            hc->conf_ctx->srv_conf[ngx_http_core_module.ctx_index];
        timeout = cscf->client_header_timeout;

        /* Precise current time (same CLOCK_MONOTONIC as ngx_current_msec) */
        clock_gettime(CLOCK_MONOTONIC, &ts);
        now_ms = (ngx_msec_t) (ts.tv_sec * 1000 + ts.tv_nsec / 1000000);
        gap_frac = (ngx_uint_t) ((ts.tv_nsec / 100000) % 10);

        /* Derive accept time from read timer */
        accept_ms = (ngx_msec_t) (c->read->timer.key - timeout);
        gap_ms = (ngx_msec_int_t) (now_ms - accept_ms);

        if (gap_ms < 0) {
            gap_ms = 0;
            gap_frac = 0;
        }

    } else {
        gap_ms = 0;
        gap_frac = 0;
    }

    ctx->gap_ms = gap_ms;
    ctx->gap_frac = gap_frac;

    /* Read TCP RTT from kernel */
    ti_len = sizeof(ti);
    if (getsockopt(c->fd, IPPROTO_TCP, TCP_INFO, &ti, &ti_len) == 0) {
        ctx->tcp_rtt_us = ti.tcpi_rtt;
    }

    ctx->measured = 1;

    SSL_set_ex_data((SSL *) ssl_conn, ngx_http_proxy_detect_ssl_index, ctx);

    ngx_log_debug3(NGX_LOG_DEBUG_HTTP, c->log, 0,
                   "proxy_detect: gap=%i.%ui ms, tcp_rtt=%ui us",
                   gap_ms, gap_frac, ctx->tcp_rtt_us);
}


/* ========================================================================
 * Access phase handler — implements monitor / header / block modes
 * ======================================================================== */

/* Helper: get per-connection context from the request */
static ngx_http_proxy_detect_conn_ctx_t *
ngx_http_proxy_detect_get_ctx(ngx_http_request_t *r)
{
    if (r->connection->ssl == NULL || r->connection->ssl->connection == NULL) {
        return NULL;
    }

    return (ngx_http_proxy_detect_conn_ctx_t *)
        SSL_get_ex_data(r->connection->ssl->connection,
                        ngx_http_proxy_detect_ssl_index);
}


/*
 * Strip existing X-Proxy-* headers from the client request to prevent
 * spoofing, then inject our measured values.
 */
static ngx_int_t
ngx_http_proxy_detect_inject_headers(ngx_http_request_t *r,
    ngx_http_proxy_detect_conn_ctx_t *ctx,
    ngx_http_proxy_detect_srv_conf_t *conf)
{
    ngx_list_part_t  *part;
    ngx_table_elt_t  *h;
    ngx_table_elt_t  *new_h;
    ngx_uint_t        i;
    u_char           *p;
    ngx_uint_t        score_hundredths;
    const char       *flag;

    /* Phase 1: Strip any client-supplied X-Proxy-* headers (anti-spoofing) */
    part = &r->headers_in.headers.part;
    h = part->elts;

    for (i = 0; /* void */ ; i++) {

        if (i >= part->nelts) {
            if (part->next == NULL) {
                break;
            }
            part = part->next;
            h = part->elts;
            i = 0;
        }

        if (h[i].hash != 0
            && h[i].key.len > 8
            && ngx_strncasecmp(h[i].key.data,
                               (u_char *) "X-Proxy-", 8) == 0)
        {
            h[i].hash = 0;  /* hide from forwarding */
        }
    }

    /* Phase 2: Inject our headers */

    /* X-Proxy-Gap */
    new_h = ngx_list_push(&r->headers_in.headers);
    if (new_h == NULL) {
        return NGX_ERROR;
    }

    p = ngx_pnalloc(r->pool, 32);
    if (p == NULL) {
        return NGX_ERROR;
    }

    new_h->hash = 1;
    ngx_str_set(&new_h->key, "X-Proxy-Gap");
    new_h->lowcase_key = (u_char *) "x-proxy-gap";
    new_h->value.data = p;
    new_h->value.len = ngx_sprintf(p, "%i.%ui", ctx->gap_ms, ctx->gap_frac)
                        - p;

    /* X-Proxy-Score: min(1.00, gap_ms / 200) */
    new_h = ngx_list_push(&r->headers_in.headers);
    if (new_h == NULL) {
        return NGX_ERROR;
    }

    p = ngx_pnalloc(r->pool, 8);
    if (p == NULL) {
        return NGX_ERROR;
    }

    score_hundredths = (ngx_uint_t) ctx->gap_ms / 2;
    if (score_hundredths > 100) {
        score_hundredths = 100;
    }

    new_h->hash = 1;
    ngx_str_set(&new_h->key, "X-Proxy-Score");
    new_h->lowcase_key = (u_char *) "x-proxy-score";
    new_h->value.data = p;
    new_h->value.len = ngx_sprintf(p, "%ui.%02ui",
                                   score_hundredths / 100,
                                   score_hundredths % 100) - p;

    /* X-Proxy-Flag */
    new_h = ngx_list_push(&r->headers_in.headers);
    if (new_h == NULL) {
        return NGX_ERROR;
    }

    flag = ((ngx_uint_t) ctx->gap_ms < conf->threshold) ? "direct" : "proxied";

    new_h->hash = 1;
    ngx_str_set(&new_h->key, "X-Proxy-Flag");
    new_h->lowcase_key = (u_char *) "x-proxy-flag";
    new_h->value.data = (u_char *) flag;
    new_h->value.len = ngx_strlen(flag);

    /* X-Proxy-TCP-RTT */
    if (ctx->tcp_rtt_us > 0) {
        new_h = ngx_list_push(&r->headers_in.headers);
        if (new_h == NULL) {
            return NGX_ERROR;
        }

        p = ngx_pnalloc(r->pool, 32);
        if (p == NULL) {
            return NGX_ERROR;
        }

        new_h->hash = 1;
        ngx_str_set(&new_h->key, "X-Proxy-TCP-RTT");
        new_h->lowcase_key = (u_char *) "x-proxy-tcp-rtt";
        new_h->value.data = p;
        new_h->value.len = ngx_sprintf(p, "%ui.%ui",
                                       ctx->tcp_rtt_us / 1000,
                                       (ctx->tcp_rtt_us % 1000) / 100) - p;
    }

    return NGX_OK;
}


/*
 * Send a custom block response with the configured status code and body.
 * Called from the access handler when block mode triggers.
 */
static ngx_int_t
ngx_http_proxy_detect_send_block(ngx_http_request_t *r,
    ngx_http_proxy_detect_srv_conf_t *conf)
{
    ngx_int_t    rc;
    ngx_buf_t   *b;
    ngx_chain_t  out;

    /* If no custom message, let nginx generate the default error page */
    if (conf->block_message.len == 0) {
        return conf->block_code;
    }

    r->headers_out.status = conf->block_code;
    r->headers_out.content_length_n = (off_t) conf->block_message.len;

    r->headers_out.content_type.data = (u_char *) "text/plain";
    r->headers_out.content_type.len = sizeof("text/plain") - 1;
    r->headers_out.content_type_lowcase = NULL;

    if (r->method == NGX_HTTP_HEAD) {
        rc = ngx_http_send_header(r);
        if (rc == NGX_ERROR || rc > NGX_OK) {
            return rc;
        }
        ngx_http_finalize_request(r, 0);
        return NGX_DONE;
    }

    rc = ngx_http_send_header(r);
    if (rc == NGX_ERROR || rc > NGX_OK) {
        return rc;
    }

    b = ngx_calloc_buf(r->pool);
    if (b == NULL) {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    b->pos = conf->block_message.data;
    b->last = b->pos + conf->block_message.len;
    b->memory = 1;
    b->last_buf = 1;
    b->last_in_chain = 1;

    out.buf = b;
    out.next = NULL;

    rc = ngx_http_output_filter(r, &out);

    ngx_http_finalize_request(r, rc);
    return NGX_DONE;
}


/*
 * Access phase handler.
 *
 * Runs for every request on servers with proxy_detect enabled.
 * Behavior depends on the configured mode:
 *
 *   monitor: do nothing (variables are still available for log_format)
 *   header:  strip client X-Proxy-* headers, inject measured values
 *   block:   reject proxied connections
 */
static ngx_int_t
ngx_http_proxy_detect_access_handler(ngx_http_request_t *r)
{
    ngx_http_proxy_detect_srv_conf_t  *conf;
    ngx_http_proxy_detect_conn_ctx_t  *ctx;

    conf = ngx_http_get_module_srv_conf(r, ngx_http_proxy_detect_module);

    if (!conf->enable) {
        return NGX_DECLINED;
    }

    ctx = ngx_http_proxy_detect_get_ctx(r);
    if (ctx == NULL || !ctx->measured) {
        return NGX_DECLINED;
    }

    switch (conf->mode) {

    case NGX_HTTP_PROXY_DETECT_MONITOR:
        /* Variables are available for log_format, nothing else to do */
        return NGX_DECLINED;

    case NGX_HTTP_PROXY_DETECT_HEADER:
        if (ngx_http_proxy_detect_inject_headers(r, ctx, conf) != NGX_OK) {
            return NGX_HTTP_INTERNAL_SERVER_ERROR;
        }
        return NGX_DECLINED;

    case NGX_HTTP_PROXY_DETECT_BLOCK:
        if ((ngx_uint_t) ctx->gap_ms >= conf->threshold) {
            ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
                          "proxy_detect: blocked connection "
                          "(gap=%i.%ui ms, threshold=%ui ms)",
                          ctx->gap_ms, ctx->gap_frac, conf->threshold);
            return ngx_http_proxy_detect_send_block(r, conf);
        }
        return NGX_DECLINED;

    default:
        return NGX_DECLINED;
    }
}


/* ========================================================================
 * Variable handlers
 * ======================================================================== */

/* $proxy_detect_gap_ms — e.g. "0.3", "157.8" */
static ngx_int_t
ngx_http_proxy_detect_gap_variable(ngx_http_request_t *r,
    ngx_http_variable_value_t *v, uintptr_t data)
{
    ngx_http_proxy_detect_conn_ctx_t  *ctx;
    u_char                            *p;

    ctx = ngx_http_proxy_detect_get_ctx(r);

    if (ctx == NULL || !ctx->measured) {
        v->not_found = 1;
        return NGX_OK;
    }

    p = ngx_pnalloc(r->pool, 32);
    if (p == NULL) {
        return NGX_ERROR;
    }

    v->len = ngx_sprintf(p, "%i.%ui", ctx->gap_ms, ctx->gap_frac) - p;
    v->data = p;
    v->valid = 1;
    v->no_cacheable = 0;
    v->not_found = 0;

    return NGX_OK;
}


/* $proxy_detect_score — e.g. "0.00", "0.75", "1.00"
 * score = min(1.0, gap_ms / 200.0)
 */
static ngx_int_t
ngx_http_proxy_detect_score_variable(ngx_http_request_t *r,
    ngx_http_variable_value_t *v, uintptr_t data)
{
    ngx_http_proxy_detect_conn_ctx_t  *ctx;
    u_char                            *p;
    ngx_uint_t                         sh;

    ctx = ngx_http_proxy_detect_get_ctx(r);

    if (ctx == NULL || !ctx->measured) {
        v->not_found = 1;
        return NGX_OK;
    }

    p = ngx_pnalloc(r->pool, 8);
    if (p == NULL) {
        return NGX_ERROR;
    }

    /* score_hundredths = gap_ms * 100 / 200 = gap_ms / 2, capped at 100 */
    sh = (ngx_uint_t) ctx->gap_ms / 2;
    if (sh > 100) {
        sh = 100;
    }

    v->len = ngx_sprintf(p, "%ui.%02ui", sh / 100, sh % 100) - p;
    v->data = p;
    v->valid = 1;
    v->no_cacheable = 0;
    v->not_found = 0;

    return NGX_OK;
}


/* $proxy_detect_flag — "direct" or "proxied" */
static ngx_int_t
ngx_http_proxy_detect_flag_variable(ngx_http_request_t *r,
    ngx_http_variable_value_t *v, uintptr_t data)
{
    ngx_http_proxy_detect_conn_ctx_t  *ctx;
    ngx_http_proxy_detect_srv_conf_t  *conf;

    ctx = ngx_http_proxy_detect_get_ctx(r);

    if (ctx == NULL || !ctx->measured) {
        v->not_found = 1;
        return NGX_OK;
    }

    conf = ngx_http_get_module_srv_conf(r, ngx_http_proxy_detect_module);

    if ((ngx_uint_t) ctx->gap_ms < conf->threshold) {
        v->data = (u_char *) "direct";
        v->len = sizeof("direct") - 1;
    } else {
        v->data = (u_char *) "proxied";
        v->len = sizeof("proxied") - 1;
    }

    v->valid = 1;
    v->no_cacheable = 0;
    v->not_found = 0;

    return NGX_OK;
}


/* $proxy_detect_tcp_rtt — e.g. "18.3" (ms, from kernel TCP_INFO) */
static ngx_int_t
ngx_http_proxy_detect_rtt_variable(ngx_http_request_t *r,
    ngx_http_variable_value_t *v, uintptr_t data)
{
    ngx_http_proxy_detect_conn_ctx_t  *ctx;
    u_char                            *p;

    ctx = ngx_http_proxy_detect_get_ctx(r);

    if (ctx == NULL || !ctx->measured || ctx->tcp_rtt_us == 0) {
        v->not_found = 1;
        return NGX_OK;
    }

    p = ngx_pnalloc(r->pool, 32);
    if (p == NULL) {
        return NGX_ERROR;
    }

    v->len = ngx_sprintf(p, "%ui.%ui",
                         ctx->tcp_rtt_us / 1000,
                         (ctx->tcp_rtt_us % 1000) / 100) - p;
    v->data = p;
    v->valid = 1;
    v->no_cacheable = 0;
    v->not_found = 0;

    return NGX_OK;
}
