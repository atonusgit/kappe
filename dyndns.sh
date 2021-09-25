#!/usr/bin/bash

. ~/kappe/.env

kappe=$(curl https://ipinfo.io/ip)
curl -u $VALLE_DYNDNS_USERNAME:$VALLE_DYNDNS_PASSWORD http://valle.fi/dyndns/?ip=$kappe
curl -u $VALLE_DYNDNS_USERNAME:$VALLE_DYNDNS_PASSWORD http://valle.fi/dyndns/
