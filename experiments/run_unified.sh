#!/bin/bash
# Unified Experiment — All providers, all protocols, N=50, 4 servers
# Output: data/unified/20260331/
set -euo pipefail
cd /home/ubuntu/resproxy-detection
set -a; source .env; set +a

DATE="20260331"
OUTDIR="data/unified/${DATE}"
LOGDIR="${OUTDIR}/logs"
N=50
COUNTRIES="us,ca,mx,br,gb,de,fr,za,ru,in,jp,kr,sg,au,id"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

declare -A DOMAINS
DOMAINS[us]="detector.example.com"
DOMAINS[ap]="detector-ap.example.com"
DOMAINS[eu]="detector-eu.example.com"
DOMAINS[sa]="detector-sa.example.com"

PROVIDERS=(brightdata soax oxylabs iproyal netnut oxylabs_mobile oxylabs_isp)

# Helper: send request via proxy
send_request() {
    local proxy_url="$1"
    local target_url="$2"
    curl -sk --max-time 30 --connect-timeout 15 \
        --proxy "$proxy_url" \
        -H "User-Agent: ${UA}" \
        -o /dev/null -w "%{http_code},%{time_total},%{remote_ip}" \
        "$target_url" 2>/dev/null || echo "000,0,error"
}

###############################################
echo "=========================================="
echo "UNIFIED EXPERIMENT"
echo "Date: ${DATE}"
echo "N per cell: ${N}"
echo "Start: $(date -u)"
echo "=========================================="

###############################################
# Start tshark on all 4 servers
###############################################
echo "--- Starting tshark ---"
sudo pkill tshark 2>/dev/null; sleep 1
sudo nohup tshark -i enX0 -f "tcp port 443" -w /tmp/unified_${DATE}.pcap </dev/null >/dev/null 2>&1 &

for region_ip in "ap:${SERVER_AP_IP}" "eu:${SERVER_EU_IP}" "sa:${SERVER_SA_IP}"; do
    region="${region_ip%%:*}"; IP="${region_ip##*:}"
    ssh -o ConnectTimeout=5 ubuntu@${IP} "
        sudo pkill tshark 2>/dev/null; sleep 1
        IFACE=\$(ip -br link show | grep -v lo | head -1 | awk '{print \$1}')
        sudo tshark -i \$IFACE -f 'tcp port 443' -w /tmp/unified_${DATE}.pcap &>/dev/null &
    " 2>/dev/null &
done
wait
sleep 2
echo "tshark started"

###############################################
# EXPERIMENT A: Core proxied dataset
# 7 providers × 4 servers in parallel per provider
###############################################
echo ""
echo "=========================================="
echo "EXPERIMENT A: Core Proxied (7 providers × 15 countries × 4 servers × N=${N})"
echo "=========================================="

CSV="${OUTDIR}/unified_proxied.csv"
echo "timestamp,server,client_ip,gap_ms,tcp_rtt_ms,provider,protocol,country,session_mode,traffic_type,ua_string" > "$CSV"

for PROVIDER in "${PROVIDERS[@]}"; do
    echo ""
    echo "=== ${PROVIDER} ==="

    # Determine protocols
    PROTOCOLS="http_connect"
    # Check SOCKS5 support
    S5=$(python3 -c "
import sys; sys.path.insert(0,'experiments')
from load_env import PROVIDERS
p = PROVIDERS.get('${PROVIDER}',{})
print('yes' if p.get('socks5_port') else 'no')
" 2>/dev/null)
    [ "$S5" = "yes" ] && PROTOCOLS="http_connect socks5"

    for PROTO in $PROTOCOLS; do
        echo "--- ${PROVIDER}/${PROTO} ---"

        # Run 4 servers in parallel
        PIDS=()
        for region in us ap eu sa; do
            domain="${DOMAINS[$region]}"
            logfile="${LOGDIR}/${PROVIDER}_${PROTO}_${region}.log"

            (
                python3 -u experiments/run_proxy.py ${PROVIDER} ${PROTO} direct \
                    --domain "${domain}" \
                    --countries "${COUNTRIES}" \
                    --n ${N} \
                    --sleep-min 2 --sleep-max 3
            ) > "${logfile}" 2>&1 &

            PIDS+=($!)
        done

        # Wait for all 4 servers
        for pid in "${PIDS[@]}"; do
            wait $pid
        done
        echo "${PROVIDER}/${PROTO} complete: $(date -u)"
    done

    # Notify per provider
    curl -s -X POST "${MATTERMOST_WEBHOOK}" -H "Content-Type: application/json" \
        -d "{\"text\": \"✅ Unified Exp A: ${PROVIDER} complete ($(date -u))\"}" 2>/dev/null
done

echo ""
echo "=== EXPERIMENT A COMPLETE: $(date -u) ==="
curl -s -X POST "${MATTERMOST_WEBHOOK}" -H "Content-Type: application/json" \
    -d '{"text": "✅ Unified Experiment A (core proxied) ALL COMPLETE. Starting A2..."}' 2>/dev/null

###############################################
# EXPERIMENT A2: Sticky vs Rotating
###############################################
echo ""
echo "=========================================="
echo "EXPERIMENT A2: Sticky vs Rotating (4 providers × 2 modes × N=20)"
echo "=========================================="

TARGET="${DOMAINS[us]}"
A2_PROVIDERS=(brightdata soax iproyal netnut)

for PROVIDER in "${A2_PROVIDERS[@]}"; do
    for MODE in sticky rotating; do
        echo "--- ${PROVIDER} ${MODE} ---"
        logfile="${LOGDIR}/sticky_${PROVIDER}_${MODE}.log"

        for i in $(seq 1 20); do
            ts=$(date +%s%N | head -c 13)

            if [ "$MODE" = "sticky" ]; then
                SESS="unified_sticky_999"
            else
                SESS="unified_rot_$(date +%s%N | md5sum | head -c 8)"
            fi

            # Build proxy URL based on provider
            case "$PROVIDER" in
                brightdata)
                    proxy_url="http://${BRIGHTDATA_USER}-country-us-session-${SESS}:${BRIGHTDATA_PASS}@${BRIGHTDATA_HOST}:${BRIGHTDATA_HTTP_PORT}"
                    ;;
                soax)
                    proxy_url="http://${SOAX_USER}-country-us:${SOAX_PASS}@${SOAX_HOST}:${SOAX_HTTP_PORT}"
                    ;;
                iproyal)
                    proxy_url="http://${IPROYAL_USER}:${IPROYAL_PASS}_country-us_session-${SESS}@${IPROYAL_HOST}:${IPROYAL_HTTP_PORT}"
                    ;;
                netnut)
                    if [ "$MODE" = "sticky" ]; then
                        proxy_url="http://${NETNUT_USER}-us-sid-${SESS}:${NETNUT_PASS}@${NETNUT_HOST}:${NETNUT_HTTP_PORT}"
                    else
                        proxy_url="http://${NETNUT_USER}-us:${NETNUT_PASS}@${NETNUT_HOST}:${NETNUT_HTTP_PORT}"
                    fi
                    ;;
            esac

            result=$(curl -sk --max-time 30 --connect-timeout 15 \
                --proxy "$proxy_url" \
                -H "User-Agent: ${UA}" \
                -o /dev/null -w "%{http_code},%{time_total}" \
                "https://${TARGET}/?provider=${PROVIDER}&session=${MODE}&n=${i}&ts=${ts}" 2>/dev/null || echo "000,0")

            echo "${ts},${PROVIDER},${MODE},${i},${result}" >> "${logfile}"
            sleep 2
        done
    done
done

echo "=== EXPERIMENT A2 COMPLETE: $(date -u) ==="
curl -s -X POST "${MATTERMOST_WEBHOOK}" -H "Content-Type: application/json" \
    -d '{"text": "✅ Unified Experiment A2 (sticky/rotating) COMPLETE. Starting E..."}' 2>/dev/null

###############################################
# EXPERIMENT E: Scope Boundary
###############################################
echo ""
echo "=========================================="
echo "EXPERIMENT E: Scope Boundary (6 categories × N=100)"
echo "=========================================="

TARGET="${DOMAINS[us]}"
E_N=100

# Direct
echo "--- Direct ---"
for i in $(seq 1 $E_N); do
    curl -sk --max-time 15 -H "User-Agent: ${UA}" -o /dev/null -w "%{http_code},%{time_total}\n" \
        "https://${TARGET}/?src=scope_direct&n=$i&ts=$(date +%s)"
    sleep 1
done > "${LOGDIR}/scope_direct.log"

# VPN (5 countries × 20)
echo "--- VPN ---"
for loc in us se gb jp de; do
    echo "VPN ${loc}"
    mullvad relay set location ${loc} 2>&1
    mullvad connect 2>&1
    sleep 5
    for i in $(seq 1 20); do
        curl -sk --max-time 15 -H "User-Agent: ${UA}" -o /dev/null -w "%{http_code},%{time_total}\n" \
            "https://${TARGET}/?src=scope_vpn&location=${loc}&n=$i&ts=$(date +%s)"
        sleep 1
    done >> "${LOGDIR}/scope_vpn.log"
    mullvad disconnect 2>&1
    sleep 2
done

# Tor
echo "--- Tor ---"
for i in $(seq 1 $E_N); do
    curl -sk --max-time 45 --socks5-hostname 127.0.0.1:9050 -H "User-Agent: ${UA}" -o /dev/null -w "%{http_code},%{time_total}\n" \
        "https://${TARGET}/?src=scope_tor&n=$i&ts=$(date +%s)"
    sleep 2
done > "${LOGDIR}/scope_tor.log"

# Squid
echo "--- Squid ---"
for i in $(seq 1 $E_N); do
    curl -sk --max-time 15 --proxy "http://127.0.0.1:3128" -H "User-Agent: ${UA}" -o /dev/null -w "%{http_code},%{time_total}\n" \
        "https://${TARGET}/?src=scope_squid&n=$i&ts=$(date +%s)"
    sleep 1
done > "${LOGDIR}/scope_squid.log"

# Lab proxy
echo "--- Lab proxy ---"
# Start lab proxy if not running
if ! ps aux | grep lab_proxy | grep -v grep > /dev/null; then
    nohup python3 experiments/lab_proxy.py </dev/null >/dev/null 2>&1 &
    sleep 2
fi
for i in $(seq 1 $E_N); do
    curl -sk --max-time 15 --proxy "http://127.0.0.1:8888" -H "User-Agent: ${UA}" -o /dev/null -w "%{http_code},%{time_total}\n" \
        "https://${TARGET}/?src=scope_labproxy&n=$i&ts=$(date +%s)"
    sleep 1
done > "${LOGDIR}/scope_labproxy.log"

echo "=== EXPERIMENT E COMPLETE: $(date -u) ==="
curl -s -X POST "${MATTERMOST_WEBHOOK}" -H "Content-Type: application/json" \
    -d '{"text": "✅ Unified Experiment E (scope boundary) COMPLETE."}' 2>/dev/null

###############################################
# Collect pcap from all servers
###############################################
echo ""
echo "=== COLLECTING DATA ==="

sudo pkill tshark 2>/dev/null; sleep 1
sudo cp /tmp/unified_${DATE}.pcap "${OUTDIR}/pcap/us/unified.pcap" 2>/dev/null
sudo chown ubuntu:ubuntu "${OUTDIR}/pcap/us/unified.pcap" 2>/dev/null

for region_ip in "ap:${SERVER_AP_IP}" "eu:${SERVER_EU_IP}" "sa:${SERVER_SA_IP}"; do
    region="${region_ip%%:*}"; IP="${region_ip##*:}"
    ssh ubuntu@${IP} "sudo pkill tshark 2>/dev/null; sleep 1; sudo chmod 644 /tmp/unified_${DATE}.pcap 2>/dev/null"
    scp ubuntu@${IP}:/tmp/unified_${DATE}.pcap "${OUTDIR}/pcap/${region}/unified.pcap" 2>/dev/null && echo "${region} pcap OK"
    scp ubuntu@${IP}:~/resproxy-detection/data/results/requests.db "${OUTDIR}/db_${region}.db" 2>/dev/null && echo "${region} DB OK"
done
cp data/db/us.db "${OUTDIR}/db_us.db" 2>/dev/null

echo ""
echo "=========================================="
echo "ALL UNIFIED EXPERIMENTS COMPLETE: $(date -u)"
echo "=========================================="

curl -s -X POST "${MATTERMOST_WEBHOOK}" -H "Content-Type: application/json" \
    -d '{"text": "🎉 UNIFIED EXPERIMENT ALL COMPLETE\n- A: 7 providers × 15 countries × 4 servers × N=50 × HC+S5\n- A2: 4 providers × sticky/rotating × N=20\n- E: Scope boundary × N=100\n- All pcap + DB collected"}'
