# this file is loaded at ~/.profile
# with adding line . ~/kappe/.profile

. ~/kappe/.env

alias ll="ls -lah"

killssh () {
    killall -9 sshd
    killall -9 ssh
}

alias sensorit="ssh $REVERSE_SSH_USERNAME@$REVERSE_SSH_HOSTNAME -p $REVERSE_SSH_PORT"
alias ssock="nohup websocat -t ws-l:$(hostname -I | awk '{print $1;}'):$WEBSOCKET_PORT broadcast:mirror: --ping-interval 60 &"
alias ssensorit="echo 'Katkaistaan mahdollinen yhteys'; sudo kill $(ps -x | grep sshd | grep -v @ | grep -v grep | grep -v ssensorit | awk '{print $1;}'); /usr/bin/sleep 5; echo 'Katkaistu. Odotetaan uuden yhteyden muodostumista...'; while [[ $([[ -z $(ps -x | grep sshd | grep -v @ | grep -v grep | grep -v ssensorit | awk '{print $1;}') ]] && echo 1 || echo 0) -eq 1 ]]; do sleep 1; done; echo 'Yhteys muodostettu'; sleep 2; sensorit"
alias killtunnel="pgrep -a sshd | grep -v priv | grep -v usr | grep -v @ | grep -v accepted | grep -v net | awk '{print $1;}' | xargs kill"
alias sshtunnel="echo  1 > $ROOT_DIRECTORY/switches/ssh_tunnel_sensorit"

cd $ROOT_DIRECTORY
