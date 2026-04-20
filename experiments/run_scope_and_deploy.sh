#!/bin/bash
# Scope boundary matrix + Deployment error budget
# Run as single pipeline, notify via Mattermost when done
set -euo pipefail
cd /home/ubuntu/resproxy-detection
source .env

N=30
TARGET="direct-ap.dns-insight.com"  # Tokyo to avoid localhost routing
LOGDIR="data/experiment_logs"
mkdir -p "$LOGDIR/scope" "$LOGDIR/deployment"

echo "=========================================="
echo "SCOPE BOUNDARY + DEPLOYMENT EXPERIMENTS"
echo "Start: $(date -u)"
echo "=========================================="

# Start tshark on Tokyo for scope experiments
ssh ubuntu@${SERVER_AP_IP} "
    sudo pkill tshark 2>/dev/null; sleep 1
    IFACE=\$(ip -br link show | grep -v lo | head -1 | awk '{print \$1}')
    sudo tshark -i \$IFACE -f 'tcp port 443' -w /tmp/capture_scope.pcap &>/dev/null &
    sleep 2 && echo 'Tokyo tshark OK'
" 2>/dev/null

###############################################
# PART 1: SCOPE BOUNDARY MATRIX
###############################################

echo ""
echo "=== SCOPE BOUNDARY MATRIX ==="
echo ""

# 1a. Direct baseline (no tunnel)
echo "--- Direct (no tunnel) ---"
for i in $(seq 1 $N); do
    curl -s -o /dev/null -w "%{http_code},%{time_total}\n" \
      "https://${TARGET}/?src=scope_direct&tunnel=none&n=$i&ts=$(date +%s)" \
      --connect-timeout 10 --max-time 15
    sleep 1
done | tee "$LOGDIR/scope/direct.log"

# 1b. Tor SOCKS5
echo "--- Tor SOCKS5 ---"
for i in $(seq 1 $N); do
    curl -s -o /dev/null -w "%{http_code},%{time_total}\n" \
      --socks5-hostname 127.0.0.1:9050 \
      "https://${TARGET}/?src=scope_tor&tunnel=tor_socks&n=$i&ts=$(date +%s)" \
      --connect-timeout 30 --max-time 45
    sleep 2
done | tee "$LOGDIR/scope/tor.log"

# 1c. Squid explicit CONNECT proxy
echo "--- Squid CONNECT proxy ---"
for i in $(seq 1 $N); do
    curl -s -o /dev/null -w "%{http_code},%{time_total}\n" \
      --proxy "http://127.0.0.1:3128" \
      "https://${TARGET}/?src=scope_squid&tunnel=squid_connect&n=$i&ts=$(date +%s)" \
      --connect-timeout 10 --max-time 15
    sleep 1
done | tee "$LOGDIR/scope/squid.log"

# 1d. WireGuard VPN (already tested, repeat small set for same pcap)
echo "--- WireGuard VPN ---"
mullvad relay set location us 2>&1
mullvad connect 2>&1
sleep 5
for i in $(seq 1 $N); do
    curl -s -o /dev/null -w "%{http_code},%{time_total}\n" \
      "https://${TARGET}/?src=scope_vpn&tunnel=wireguard&n=$i&ts=$(date +%s)" \
      --connect-timeout 10 --max-time 15
    sleep 1
done | tee "$LOGDIR/scope/vpn.log"
mullvad disconnect 2>&1
sleep 2

# 1e. Lab proxy (normal CONNECT) — use local lab proxy if running
if curl -s -o /dev/null -w "%{http_code}" --proxy "http://127.0.0.1:8888" "https://${TARGET}/?test=1" --connect-timeout 5 --max-time 10 2>/dev/null | grep -q 200; then
    echo "--- Lab CONNECT proxy ---"
    for i in $(seq 1 $N); do
        curl -s -o /dev/null -w "%{http_code},%{time_total}\n" \
          --proxy "http://127.0.0.1:8888" \
          "https://${TARGET}/?src=scope_labproxy&tunnel=connect_proxy&n=$i&ts=$(date +%s)" \
          --connect-timeout 10 --max-time 15
        sleep 1
    done | tee "$LOGDIR/scope/labproxy.log"
else
    echo "--- Lab proxy not running, skipping ---"
fi

# 1f. BrightData residential proxy (small set for comparison)
echo "--- BrightData residential proxy ---"
for i in $(seq 1 10); do
    curl -s -o /dev/null -w "%{http_code},%{time_total}\n" \
      --proxy "http://${BRIGHTDATA_USER}-country-us:${BRIGHTDATA_PASS}@${BRIGHTDATA_HOST}:${BRIGHTDATA_HTTP_PORT}" \
      "https://${TARGET}/?src=scope_brightdata&tunnel=residential_proxy&n=$i&ts=$(date +%s)" \
      --connect-timeout 15 --max-time 30
    sleep 2
done | tee "$LOGDIR/scope/brightdata.log"

echo ""
echo "=== SCOPE BOUNDARY COMPLETE ==="

###############################################
# PART 2: DEPLOYMENT ERROR BUDGET
###############################################

echo ""
echo "=== DEPLOYMENT ERROR BUDGET ==="
echo ""

# 2a. Configure nginx to log timestamps
# Add timing headers to response
sudo tee /etc/nginx/conf.d/timing.conf > /dev/null << 'NGINX'
add_header X-Request-Time $request_time;
add_header X-Upstream-Time $upstream_response_time;
NGINX
sudo nginx -t 2>&1 && sudo systemctl reload nginx

# 2b. Low load baseline: serial requests
echo "--- Low load (serial, 1 req/s) ---"
for i in $(seq 1 30); do
    ts_before=$(date +%s%N)
    resp=$(curl -s -D - -o /dev/null \
      "https://direct.dns-insight.com/?src=deploy_low&load=low&n=$i&ts=$(date +%s)" \
      --connect-timeout 5 --max-time 10 2>&1)
    ts_after=$(date +%s%N)
    req_time=$(echo "$resp" | grep -i x-request-time | awk '{print $2}' | tr -d '\r')
    echo "low/$i: curl=$((($ts_after - $ts_before) / 1000000))ms nginx_req_time=${req_time}s"
    sleep 1
done | tee "$LOGDIR/deployment/low_load.log"

# 2c. Medium load: 10 concurrent
echo "--- Medium load (10 concurrent, 5s) ---"
wrk -t2 -c10 -d5s --latency \
  "https://direct.dns-insight.com/?src=deploy_medium&load=medium" \
  2>&1 | tee "$LOGDIR/deployment/medium_load.log"

# Send measurement requests during medium load
wrk -t2 -c10 -d10s "https://direct.dns-insight.com/?src=deploy_medium_bg&load=medium" &>/dev/null &
WRK_PID=$!
sleep 2
for i in $(seq 1 20); do
    curl -s -o /dev/null -w "%{http_code},%{time_total}\n" \
      "https://direct.dns-insight.com/?src=deploy_medium_measure&load=medium&n=$i&ts=$(date +%s)" \
      --connect-timeout 5 --max-time 10
    sleep 0.5
done | tee "$LOGDIR/deployment/medium_measure.log"
kill $WRK_PID 2>/dev/null
wait $WRK_PID 2>/dev/null

# 2d. High load: 100 concurrent
echo "--- High load (100 concurrent, 5s) ---"
wrk -t4 -c100 -d5s --latency \
  "https://direct.dns-insight.com/?src=deploy_high&load=high" \
  2>&1 | tee "$LOGDIR/deployment/high_load.log"

# Send measurement during high load
wrk -t4 -c100 -d10s "https://direct.dns-insight.com/?src=deploy_high_bg&load=high" &>/dev/null &
WRK_PID=$!
sleep 2
for i in $(seq 1 20); do
    curl -s -o /dev/null -w "%{http_code},%{time_total}\n" \
      "https://direct.dns-insight.com/?src=deploy_high_measure&load=high&n=$i&ts=$(date +%s)" \
      --connect-timeout 5 --max-time 10
    sleep 0.5
done | tee "$LOGDIR/deployment/high_measure.log"
kill $WRK_PID 2>/dev/null
wait $WRK_PID 2>/dev/null

# Clean up nginx timing config
sudo rm -f /etc/nginx/conf.d/timing.conf
sudo nginx -t 2>&1 && sudo systemctl reload nginx

echo ""
echo "=== DEPLOYMENT ERROR BUDGET COMPLETE ==="

###############################################
# COLLECT DATA
###############################################

echo ""
echo "=== COLLECTING DATA ==="

# Stop tshark locally
sudo pkill tshark 2>/dev/null; sleep 1
sudo cp /tmp/capture_scope_deploy.pcap data/captures/us/20260328_scope_deploy.pcap 2>/dev/null
sudo chown ubuntu:ubuntu data/captures/us/20260328_scope_deploy.pcap 2>/dev/null

# Collect Tokyo pcap
ssh ubuntu@${SERVER_AP_IP} "sudo pkill tshark 2>/dev/null; sleep 1; sudo chmod 644 /tmp/capture_scope.pcap 2>/dev/null"
scp ubuntu@${SERVER_AP_IP}:/tmp/capture_scope.pcap data/captures/ap/20260328_scope.pcap 2>/dev/null && echo "Tokyo pcap OK"
scp ubuntu@${SERVER_AP_IP}:~/resproxy-detection/data/results/requests.db data/db/ap_scope.db 2>/dev/null && echo "Tokyo DB OK"

echo ""
echo "=========================================="
echo "ALL EXPERIMENTS COMPLETE: $(date -u)"
echo "=========================================="

# Notify
curl -s -X POST "${MATTERMOST_WEBHOOK}" \
  -H "Content-Type: application/json" \
  -d '{"text": "✅ Scope boundary + Deployment error budget COMPLETE\n- Scope: Direct, Tor, Squid, WireGuard, Lab proxy, BrightData\n- Deploy: Low/Medium/High load tests\n- Ready for analysis"}'
