#!/usr/bin/env python3
"""
Load .env file and provide config to all experiment/analysis scripts.
Usage:
    from load_env import CONFIG, SERVERS, PROVIDERS
"""

import os
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent / ".env"


def load_dotenv(path=ENV_PATH):
    """Parse .env file into os.environ."""
    if not path.exists():
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def _env(key, default=""):
    return os.environ.get(key, default)


def _env_int(key, default=0):
    v = os.environ.get(key, "")
    return int(v) if v else default


# Load on import
load_dotenv()

# Server infrastructure
SERVERS = {
    "us": {"ip": _env("SERVER_US_IP"), "domain": _env("SERVER_US_DOMAIN")},
    "ap": {"ip": _env("SERVER_AP_IP"), "domain": _env("SERVER_AP_DOMAIN")},
    "eu": {"ip": _env("SERVER_EU_IP"), "domain": _env("SERVER_EU_DOMAIN")},
    "sa": {"ip": _env("SERVER_SA_IP"), "domain": _env("SERVER_SA_DOMAIN")},
}
CF_DOMAIN = _env("SERVER_CF_DOMAIN")
ADMIN_EMAIL = _env("ADMIN_EMAIL")

# Proxy providers
PROVIDERS = {
    "brightdata": {
        "host": _env("BRIGHTDATA_HOST"),
        "http_connect_port": _env_int("BRIGHTDATA_HTTP_PORT"),
        "socks5_port": _env_int("BRIGHTDATA_SOCKS5_PORT"),
        "username": _env("BRIGHTDATA_USER"),
        "password": _env("BRIGHTDATA_PASS"),
        "country_mode": "username_suffix",
        "country_format": "-country-{country}",
        "architecture": "super-proxy",
    },
    "brightdata_mobile": {
        "host": _env("BRIGHTDATA_MOBILE_HOST"),
        "http_connect_port": _env_int("BRIGHTDATA_MOBILE_HTTP_PORT"),
        "socks5_port": None,
        "username": _env("BRIGHTDATA_MOBILE_USER"),
        "password": _env("BRIGHTDATA_MOBILE_PASS"),
        "country_mode": "username_suffix",
        "country_format": "-country-{country}",
        "architecture": "mobile",
    },
    "brightdata_isp": {
        "host": _env("BRIGHTDATA_ISP_HOST"),
        "http_connect_port": _env_int("BRIGHTDATA_ISP_HTTP_PORT"),
        "socks5_port": None,
        "username": _env("BRIGHTDATA_ISP_USER"),
        "password": _env("BRIGHTDATA_ISP_PASS"),
        "country_mode": "username_suffix",
        "country_format": "-country-{country}",
        "architecture": "isp",
    },
    "soax": {
        "host": _env("SOAX_HOST"),
        "http_connect_port": _env_int("SOAX_HTTP_PORT"),
        "socks5_port": _env_int("SOAX_SOCKS5_PORT"),
        "username": _env("SOAX_USER"),
        "password": _env("SOAX_PASS"),
        "country_mode": "username_suffix",
        "country_format": "-country-{country}",
        "architecture": "super-proxy",
    },
    "oxylabs": {
        "host": _env("OXYLABS_HOST"),
        "http_connect_port": _env_int("OXYLABS_HTTP_PORT"),
        "socks5_port": _env_int("OXYLABS_SOCKS5_PORT"),
        "username": _env("OXYLABS_USER"),
        "password": _env("OXYLABS_PASS"),
        "country_mode": "username_suffix",
        "country_format": "-cc-{country}",
        "architecture": "super-proxy",
    },
    "oxylabs_mobile": {
        "host": _env("OXYLABS_HOST"),
        "http_connect_port": _env_int("OXYLABS_HTTP_PORT"),
        "socks5_port": _env_int("OXYLABS_SOCKS5_PORT"),
        "username": _env("OXYLABS_USER"),
        "password": _env("OXYLABS_PASS"),
        "country_mode": "username_suffix",
        "country_format": "-sm-cc-{country}",
        "architecture": "mobile",
    },
    "oxylabs_isp": {
        "host": _env("OXYLABS_HOST"),
        "http_connect_port": _env_int("OXYLABS_HTTP_PORT"),
        "socks5_port": _env_int("OXYLABS_SOCKS5_PORT"),
        "username": _env("OXYLABS_USER"),
        "password": _env("OXYLABS_PASS"),
        "country_mode": "username_suffix",
        "country_format": "-rs-cc-{country}",
        "architecture": "isp",
    },
    "iproyal": {
        "host": _env("IPROYAL_HOST"),
        "http_connect_port": _env_int("IPROYAL_HTTP_PORT"),
        "socks5_port": _env_int("IPROYAL_SOCKS5_PORT"),
        "username": _env("IPROYAL_USER"),
        "password": _env("IPROYAL_PASS"),
        "country_mode": "password_suffix",
        "country_format": "_country-{country}",
        "architecture": "p2p",
    },
    "netnut": {
        "host": _env("NETNUT_HOST"),
        "http_connect_port": _env_int("NETNUT_HTTP_PORT"),
        "socks5_port": _env_int("NETNUT_SOCKS5_PORT") or None,
        "username": _env("NETNUT_USER"),
        "password": _env("NETNUT_PASS"),
        "country_mode": "username_suffix",
        "country_format": "-{country}",
        "architecture": "isp-level",
    },
}

RIPE_ATLAS_API_KEY = _env("RIPE_ATLAS_API_KEY")
MATTERMOST_WEBHOOK = _env("MATTERMOST_WEBHOOK")

# Full config dict (backward compatible with providers.json readers)
CONFIG = {
    "providers": PROVIDERS,
    "ripe_atlas": {"api_key": RIPE_ATLAS_API_KEY},
    "server": {
        "ip": SERVERS["us"]["ip"],
        "domain_direct": SERVERS["us"]["domain"],
        "domain_cf": CF_DOMAIN,
    },
    "servers": SERVERS,
}


if __name__ == "__main__":
    import json
    print(json.dumps(CONFIG, indent=2))
