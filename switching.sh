#!/usr/bin/env sh
#
# switching.sh - script for periodically switching the SSID in Eapmartello
#
# Actually works by restarting Eapmartello for switching the SSID
#
# usage:
#  sudo switching.sh list.csv interface
#   - list: csv file in format SSID:time, one per row
#       - the time is in format that UNIX utilty `sleep` accpets, like "1m", "30s" and so on
#   - interface: the interface to run on, optional, defaults to wlan0


# root check
if ((EUID != 0)); then
  exec sudo -u \#0 $0 $@
fi

iface=$2
if [ -z $iface ]; then
    iface=wlan0
fi

waiter() {
    # sends newline
    sleep $1 ; echo ""
}

#temporary values
time=1m
ssid=eapmartello

continue=true
user_interrupt () {
    continue=false
}
trap user_interrupt SIGINT SIGTERM

echo ""
echo "[switching.sh] looping over SSIDs:"
cat $1
echo ""

while $continue
do
    while IFS=";", read -r ssid time && $continue
    do
        echo "[switching.sh] Running with $ssid for $time"
        waiter $time | sudo python3 martello.py -e $ssid -i $iface
    done < $1
done


