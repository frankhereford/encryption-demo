FROM haproxy:2.8-alpine
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
COPY --chmod=755 entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
