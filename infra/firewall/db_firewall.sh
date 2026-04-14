#!/bin/bash

sudo iptables -F
#input rules
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp -s 192.168.56.10 --dport 5432 -j ACCEPT
sudo iptables -A INPUT -p tcp -s 192.168.56.10 --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp -s 192.168.56.12 -j DROP
sudo iptables -A INPUT -p tcp -s 192.168.56.12 --sport 22 -j DROP
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A INPUT -p tcp -i eth0 --dport 22 -j ACCEPT
sudo iptables -A INPUT -j DROP
#sudo iptables -A INPUT -i enp0s8 -j DROP

#output rules
sudo iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A OUTPUT -p tcp --sport 5432 -d 192.168.56.10 -j ACCEPT

# Save rules
sudo netfilter-persistent save_rules
