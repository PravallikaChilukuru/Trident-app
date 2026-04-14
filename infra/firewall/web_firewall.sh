#!/bin/bash

sudo iptables -F
#input rules
sudo iptables -I INPUT 1 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp -i enp0s8 --dport 22 -s 192.168.56.12 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -i eth0 -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
sudo iptables -A INPUT -i enp0s8 -j DROP

#output rules
sudo iptables -A OUTPUT -p tcp --dport 5432 -d 192.168.56.11 -j ACCEPT

# Install persistence package
apt-get update
apt-get install -y iptables-persistent

# Save rules
netfilter-persistent save
