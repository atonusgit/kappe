#!/usr/bin/bash

. .env

curl -X POST https://content.dropboxapi.com/2/files/download\
     --header "Authorization: Bearer $DROPBOX_AUTH_TOKEN"\
     --header "Dropbox-API-Arg: {\"path\": \"/container.tar.gz\"}" > ~/kappe/container.tar.gz
tar -xvzf ~/kappe/container.tar.gz -C ~/kappe
mv ~/kappe/home/pi/sensor_logs/* ~/kappe/sensor_logs
rm ~/kappe/container.tar.gz
rm -r ~/kappe/home
