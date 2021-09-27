#!/bin/bash

. ~/kappe/.env

files=$(find ~/kappe/sensor_logs/*)
tar -czvf ~/kappe/sensor_logs_bk.tar.gz $files
mv ~/kappe/sensor_logs_bk.tar.gz ~/sensor_logs_bk.tar.gz

curl -s -X POST https://api.dropboxapi.com/2/files/delete \
    --header "Authorization: Bearer $DROPBOX_AUTH_TOKEN" \
    --header "Content-Type: application/json" \
    --data "{\"path\": \"/sensor_logs_bk.tar.gz\"}"

curl -s -X POST https://content.dropboxapi.com/2/files/upload \
    --header "Authorization: Bearer $DROPBOX_AUTH_TOKEN" \
    --header "Dropbox-API-Arg: {\"path\": \"/sensor_logs_bk.tar.gz\"}" \
    --header "Content-Type: application/octet-stream" \
    --data-binary @sensor_logs_bk.tar.gz

rm ~/sensor_logs_bk.tar.gz
