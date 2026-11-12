# nginx Dynamic Module

`ngx_http_proxy_detect_module` measures the ACK-to-ClientHello timing
gap inside nginx, without requiring packet capture.

## Contents

- `config` — nginx dynamic module build file
- `ngx_http_proxy_detect_module.c` — module source (803 lines)

## Building

```bash
# Inside an nginx source tree:
./configure --with-compat --add-dynamic-module=/path/to/nginx-module
make modules
cp objs/ngx_http_proxy_detect_module.so /usr/lib/nginx/modules/
```

Then in `nginx.conf`:
```
load_module modules/ngx_http_proxy_detect_module.so;
```

## Measurement approach

- Hooks `SSL_CTX_set_info_callback` to time the ClientHello arrival.
- Derives accept time from nginx's internal connection read timer
  (same `CLOCK_MONOTONIC` source).
- Reads TCP RTT via `getsockopt(TCP_INFO)`.
- SSL ex_data persists across `SSL_set_SSL_CTX`, so measurements on
  the default context are accessible after SNI dispatch.
