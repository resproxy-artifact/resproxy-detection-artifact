#!/bin/bash
# Oxylabs full experiment: residential + mobile + ISP
# 3 types × 4 servers × 15 countries × 2 protocols × 20 requests = 7,200
# Then browser: 3 types × 3 UA × 15 countries × 10 = 1,350
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

echo "=== Oxylabs Full Experiment (Residential + Mobile + ISP) ==="
echo "Start: $(date -u)"

###############################################
# PHASE 1: Multi-server timing (3 types × 4 servers)
###############################################

for PROVIDER in oxylabs oxylabs_mobile oxylabs_isp; do
    echo ""
    echo "=== ${PROVIDER} multi-server ==="
    PIDS=()

    for region in "${!DOMAINS[@]}"; do
        domain="${DOMAINS[$region]}"
        logfile="data/experiment_logs/multiserver_${PROVIDER}_${region}_$(date +%Y%m%d_%H%M%S).log"

        (
            echo "=== [${region}] ${domain} START: $(date -u) ==="
            python3 -u experiments/run_proxy.py ${PROVIDER} http_connect direct \
                --domain "${domain}" --countries "${COUNTRIES}" --n ${N}
            python3 -u experiments/run_proxy.py ${PROVIDER} socks5 direct \
                --domain "${domain}" --countries "${COUNTRIES}" --n ${N}
            echo "=== [${region}] ${domain} COMPLETE: $(date -u) ==="
        ) > "${logfile}" 2>&1 &

        PIDS+=($!)
        echo "  Launched ${region} → ${domain} (PID: $!)"
    done

    echo "  Waiting for ${PROVIDER}..."
    for pid in "${PIDS[@]}"; do
        wait $pid
        echo "  PID $pid finished"
    done
    echo "=== ${PROVIDER} DONE: $(date -u) ==="
done

echo ""
echo "=== ALL TIMING COMPLETE: $(date -u) ==="

curl -s -X POST "${MATTERMOST_WEBHOOK}" \
  -H "Content-Type: application/json" \
  -d '{"text": "✅ Oxylabs timing complete (residential+mobile+ISP × 4 servers). Starting browser..."}'

###############################################
# PHASE 2: Browser fingerprint (3 types × 3 UA)
###############################################

# Restart tshark locally for browser
sudo pkill tshark 2>/dev/null; sleep 1
sudo nohup tshark -i enX0 -f "tcp port 443" -w /tmp/capture_oxylabs_browser.pcap </dev/null >/dev/null 2>&1 &
sleep 1

for PROVIDER in oxylabs oxylabs_mobile oxylabs_isp; do
    echo ""
    echo "=== ${PROVIDER} browser ==="
    PIDS=()
    for ua in windows_chrome macos_chrome windows_firefox; do
        logfile="data/experiment_logs/browser/browser_matrix_${PROVIDER}_${ua}_$(date +%Y%m%d_%H%M%S).log"
        (
            python3 -u experiments/run_browser.py ${PROVIDER} http_connect direct \
                --countries "${COUNTRIES}" --n 10 --ua ${ua}
        ) > "${logfile}" 2>&1 &
        PIDS+=($!)
        echo "  Launched ${PROVIDER}/${ua} (PID: $!)"
    done
    echo "  Waiting..."
    for pid in "${PIDS[@]}"; do
        wait $pid
    done
    echo "=== ${PROVIDER} browser DONE ==="
done

sudo pkill tshark 2>/dev/null; sleep 1
sudo cp /tmp/capture_oxylabs_browser.pcap data/captures/us/20260328_oxylabs_browser.pcap 2>/dev/null
sudo chown ubuntu:ubuntu data/captures/us/20260328_oxylabs_browser.pcap 2>/dev/null

echo ""
echo "=== ALL EXPERIMENTS COMPLETE: $(date -u) ==="

###############################################
# PHASE 3: Collect pcap + DB
###############################################

echo "=== Collecting data ==="

# Local timing pcap
sudo cp /tmp/capture_oxylabs.pcap data/captures/us/20260328_oxylabs_multi.pcap 2>/dev/null
sudo chown ubuntu:ubuntu data/captures/us/20260328_oxylabs_multi.pcap 2>/dev/null

# Remote
for region_ip in "ap:${SERVER_AP_IP}" "eu:${SERVER_EU_IP}" "sa:${SERVER_SA_IP}"; do
    region="${region_ip%%:*}"
    IP="${region_ip##*:}"
    ssh ubuntu@${IP} "sudo pkill tshark 2>/dev/null; sleep 1; sudo chmod 644 /tmp/capture_oxylabs.pcap 2>/dev/null"
    scp ubuntu@${IP}:/tmp/capture_oxylabs.pcap "data/captures/${region}/20260328_oxylabs_multi.pcap" 2>/dev/null && echo "${region} pcap OK"
    scp ubuntu@${IP}:~/resproxy-detection/data/results/requests.db "data/db/${region}_oxylabs.db" 2>/dev/null && echo "${region} DB OK"
done

echo "=== DATA COLLECTION COMPLETE ==="

curl -s -X POST "${MATTERMOST_WEBHOOK}" \
  -H "Content-Type: application/json" \
  -d '{"text": "✅ Oxylabs ALL experiments complete\n- 3 types (residential/mobile/ISP) × 4 servers × 15 countries\n- + browser fingerprint (3 types × 3 UA × 15 countries)\n- Total: ~8,550 new connections"}'
