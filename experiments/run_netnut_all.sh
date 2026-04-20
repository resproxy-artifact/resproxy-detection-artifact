#!/bin/bash
# NetNut full experiment: ISP-level proxy
# Multi-server timing + browser fingerprint
set -euo pipefail
cd /home/ubuntu/resproxy-detection
set -a; source .env 2>/dev/null; set +a

COUNTRIES="us,kr,de,jp,br,gb,au,in,sg,fr,za,ru,id,mx,ca"
N=20

declare -A DOMAINS
DOMAINS[us]="${SERVER_US_DOMAIN}"
DOMAINS[ap]="${SERVER_AP_DOMAIN}"
DOMAINS[eu]="${SERVER_EU_DOMAIN}"
DOMAINS[sa]="${SERVER_SA_DOMAIN}"

echo "=== NetNut Full Experiment ==="
echo "Start: $(date -u)"

###############################################
# Start tshark on all servers
###############################################
sudo pkill tshark 2>/dev/null; sleep 1
sudo nohup tshark -i enX0 -f "tcp port 443" -w /tmp/capture_netnut.pcap </dev/null >/dev/null 2>&1 &

for IP in ${SERVER_AP_IP} ${SERVER_EU_IP} ${SERVER_SA_IP}; do
    ssh ubuntu@${IP} "
        sudo pkill tshark 2>/dev/null; sleep 1
        IFACE=\$(ip -br link show | grep -v lo | head -1 | awk '{print \$1}')
        sudo tshark -i \$IFACE -f 'tcp port 443' -w /tmp/capture_netnut.pcap &>/dev/null &
    " 2>/dev/null &
done
wait
sleep 2

###############################################
# Multi-server timing: HTTP CONNECT + SOCKS5
###############################################
echo "=== NetNut multi-server timing ==="
PIDS=()

for region in "${!DOMAINS[@]}"; do
    domain="${DOMAINS[$region]}"
    logfile="data/experiment_logs/multiserver_netnut_${region}_$(date +%Y%m%d_%H%M%S).log"

    (
        echo "=== [${region}] ${domain} START: $(date -u) ==="
        python3 -u experiments/run_proxy.py netnut http_connect direct \
            --domain "${domain}" --countries "${COUNTRIES}" --n ${N}
        python3 -u experiments/run_proxy.py netnut socks5 direct \
            --domain "${domain}" --countries "${COUNTRIES}" --n ${N}
        echo "=== [${region}] ${domain} COMPLETE: $(date -u) ==="
    ) > "${logfile}" 2>&1 &

    PIDS+=($!)
    echo "  Launched ${region} → ${domain} (PID: $!)"
done

echo "  Waiting for timing..."
for pid in "${PIDS[@]}"; do
    wait $pid
    echo "  PID $pid finished"
done
echo "=== NetNut timing DONE: $(date -u) ==="

curl -s -X POST "${MATTERMOST_WEBHOOK}" \
  -H "Content-Type: application/json" \
  -d '{"text": "✅ NetNut multi-server timing complete (4 servers × 15 countries × HC+S5). Starting browser..."}'

###############################################
# Browser fingerprint: 3 UA profiles
###############################################
echo "=== NetNut browser ==="

# Restart tshark locally for browser
sudo pkill tshark 2>/dev/null; sleep 1
sudo nohup tshark -i enX0 -f "tcp port 443" -w /tmp/capture_netnut_browser.pcap </dev/null >/dev/null 2>&1 &
sleep 1

PIDS=()
for ua in windows_chrome macos_chrome windows_firefox; do
    logfile="data/experiment_logs/browser/browser_matrix_netnut_${ua}_$(date +%Y%m%d_%H%M%S).log"
    (
        python3 -u experiments/run_browser.py netnut http_connect direct \
            --countries "${COUNTRIES}" --n 10 --ua ${ua}
    ) > "${logfile}" 2>&1 &
    PIDS+=($!)
    echo "  Launched netnut/${ua} (PID: $!)"
done

echo "  Waiting for browser..."
for pid in "${PIDS[@]}"; do
    wait $pid
done
echo "=== NetNut browser DONE ==="

curl -s -X POST "${MATTERMOST_WEBHOOK}" \
  -H "Content-Type: application/json" \
  -d '{"text": "✅ NetNut browser fingerprint complete (3 UA × 15 countries)."}'

###############################################
# Collect pcap + DB
###############################################
echo "=== Collecting data ==="

sudo pkill tshark 2>/dev/null; sleep 1
sudo cp /tmp/capture_netnut.pcap data/captures/us/20260329_netnut_multi.pcap 2>/dev/null
sudo cp /tmp/capture_netnut_browser.pcap data/captures/us/20260329_netnut_browser.pcap 2>/dev/null
sudo chown ubuntu:ubuntu data/captures/us/20260329_netnut_*.pcap 2>/dev/null

for region_ip in "ap:${SERVER_AP_IP}" "eu:${SERVER_EU_IP}" "sa:${SERVER_SA_IP}"; do
    region="${region_ip%%:*}"
    IP="${region_ip##*:}"
    ssh ubuntu@${IP} "sudo pkill tshark 2>/dev/null; sleep 1; sudo chmod 644 /tmp/capture_netnut.pcap 2>/dev/null"
    scp ubuntu@${IP}:/tmp/capture_netnut.pcap "data/captures/${region}/20260329_netnut_multi.pcap" 2>/dev/null && echo "${region} pcap OK"
    scp ubuntu@${IP}:~/resproxy-detection/data/results/requests.db "data/db/${region}_netnut.db" 2>/dev/null && echo "${region} DB OK"
done

echo "=== ALL NETNUT COMPLETE: $(date -u) ==="

curl -s -X POST "${MATTERMOST_WEBHOOK}" \
  -H "Content-Type: application/json" \
  -d '{"text": "✅ NetNut ALL experiments complete\n- ISP-level architecture\n- 4 servers × 15 countries × HC+S5 + browser\n- Data collected, ready for analysis"}'
