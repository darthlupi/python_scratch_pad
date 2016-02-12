#!/usr/bin/python

import sys

###################################################
##Simple reverse DNS generator
##Generates file based on a /24 provided as input
##Created by Robert Lupinek 5/3/2012
##Modified by Robert Lupinek 5/3/2012

if (len(sys.argv) <= 1):
    sys.exit("Please the network IP of a /24 subnet please...\nExample:\ngererate_reverse.py 192.168.1.0")

ip = sys.argv[1];
domain = ".dchp.yourdns.net."

octs = ip.split('.')

if (len(octs) < 3):
    sys.exit("Please the network IP of a /24 subnet please...\nExample:\ngererate_reverse.py 192.168.1.0")

forward_name = octs[0] + '.' + octs[1] + '.' + octs[2];
reverse_name = octs[2] + '.' + octs[1] + '.' + octs[0];
address_max = 256;


print """$ORIGIN .
$TTL 3600       ; 1 hour"""
print reverse_name+ """.in-addr.arpa  IN SOA  ns1.yourns.com. ns2.yourns.com. (
                                2006020911 ; serial
                                900        ; refresh (15 minutes)
                                3600       ; retry (1 hour)
                                2592000    ; expire (4 weeks 2 days)
                                900        ; minimum (15 minutes)
                                )
                        NS      ns1.yourns.com.
                        NS      ns2.yourns.com.
$ORIGIN """+ reverse_name+ """.in-addr.arpa.
$TTL 300        ; 5 minutes
"""

for next in range(0, address_max):
        print str(next) + "                             PTR             " + forward_name + '.' + str(next) + domain;