#!/usr/bin/bash

# Set permissions for /dev/gpiomem
sudo chown root.gpio /dev/gpiomem
sudo chmod g+rw /dev/gpiomem

# Set operating mode to 'online'
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode='online'

# Take down wwan0 interface
sudo ip link set wwan0 down

# Configure raw IP mode
echo 'Y' | sudo tee /sys/class/net/wwan0/qmi/raw_ip

# Bring up wwan0 interface
sudo ip link set wwan0 up

# Start network with specified APN and IP type
sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network="apn='internet',ip-type=4" --client-no-release-cid

# Obtain IP address via DHCP
sudo udhcpc -i wwan0
