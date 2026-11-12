#!/bin/bash
# VPN false positive test — Mullvad WireGuard
# VPN = IP-layer tunnel → TCP handshake comes from client directly → gap ≈ 0
# Target: Tokyo server (not local, to avoid routing issues)
set -euo pipefail
cd /home/ubuntu/resproxy-detection

set -a; source .env 2>/dev/null; set +a

TARGET="${SERVER_AP_DOMAIN}"  # Tokyo as target
N=20
LOGDIR="data/experiment_logs/vpn"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/vpn_mullvad_$(date +%Y%m%d_%H%M%S).csv"

# VPN locations to test (Mullvad relay locations)
LOCATIONS=(us se gb jp de)

echo "timestamp,vpn_provider,vpn_protocol,vpn_location,vpn_relay,vpn_ip,seq,http_code,time_total" > "$LOGFILE"

echo "=== VPN False Positive Test ==="
echo "Provider: Mullvad"
echo "Protocol: WireGuard"
echo "Target: ${TARGET}"
echo "Locations: ${LOCATIONS[*]}"
echo "N per location: ${N}"
echo "Start: $(date -u)"
echo ""

# Start tshark on Tokyo
echo "Starting tshark on Tokyo..."
ssh ubuntu@${SERVER_AP_IP} "sudo pkill tshark 2>/dev/null; sleep 1; bash /tmp/start_tshark.sh" 2>/dev/null

# Direct baseline (no VPN) to Tokyo
echo "--- Direct baseline (no VPN) ---"
for i in $(seq 1 $N); do
    ts=$(date +%s%N | head -c 13)
    result=$(curl -s -o /dev/null -w "%{http_code},%{time_total}" \
        --connect-timeout 10 --max-time 15 \
        "https://${TARGET}/?src=direct_vpn_baseline&proto=none&location=us-east-1&n=${i}&ts=${ts}" 2>&1 || echo "000,0")
    echo "${ts},none,none,direct,none,$(curl -s ifconfig.me),${i},${result}" >> "$LOGFILE"
    echo "  direct/${i}: ${result}"
    sleep 1
done

# VPN tests — each location
for loc in "${LOCATIONS[@]}"; do
    echo ""
    echo "--- Mullvad WireGuard → ${loc} ---"

    mullvad relay set location "${loc}" 2>&1
    mullvad connect 2>&1
    sleep 5

    # Get VPN status
    vpn_status=$(mullvad status 2>&1)
    vpn_relay=$(echo "$vpn_status" | grep "Relay:" | awk '{print $2}' || echo "unknown")
    vpn_ip=$(echo "$vpn_status" | grep "IPv4:" | awk '{print $NF}' || echo "unknown")
    echo "  Relay: ${vpn_relay}, IP: ${vpn_ip}"

    for i in $(seq 1 $N); do
        ts=$(date +%s%N | head -c 13)
        result=$(curl -s -o /dev/null -w "%{http_code},%{time_total}" \
            --connect-timeout 10 --max-time 15 \
            "https://${TARGET}/?src=vpn&proto=wireguard&location=${loc}&n=${i}&ts=${ts}" 2>&1 || echo "000,0")
        echo "${ts},mullvad,wireguard,${loc},${vpn_relay},${vpn_ip},${i},${result}" >> "$LOGFILE"
        echo "  ${loc}/${i}: ${result}"
        sleep 2
    done

    mullvad disconnect 2>&1
    sleep 2
done

echo ""
echo "=== VPN Test Complete: $(date -u) ==="
echo "Log: ${LOGFILE}"

# Collect pcap from Tokyo
echo "Collecting pcap from Tokyo..."
ssh ubuntu@${SERVER_AP_IP} "sudo pkill tshark 2>/dev/null; sleep 1; sudo chmod 644 /tmp/capture_*.pcap 2>/dev/null"
scp ubuntu@${SERVER_AP_IP}:/tmp/capture_*.pcap "data/captures/ap/vpn_test.pcap" 2>/dev/null && echo "pcap OK" || echo "pcap FAIL"
