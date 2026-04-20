#!/bin/sh
set -e

CERT_DIR="/etc/letsencrypt/live/encryption-demo.frankhereford.com"
HAPROXY_PEM="/tmp/haproxy-certs/haproxy.pem"

mkdir -p /tmp/haproxy-certs
cat "$CERT_DIR/fullchain.pem" "$CERT_DIR/privkey.pem" > "$HAPROXY_PEM"
chmod 600 "$HAPROXY_PEM"

exec haproxy -f /usr/local/etc/haproxy/haproxy.cfg
