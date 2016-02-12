#!/usr/bin/python

import requests
import json

#No real error trapping.
#Just experimenting with the get next IP  and assign a host record method INFOBLOX provides.
post_data = {'name': 'fixed-next.example.com',
             'ipv4addrs':[
               #{ 'ipv4addr': '10.243.84.12', }
               { 'ipv4addr': 'func:nextavailableip:10.243.84.0/22', }
             ],
             'configure_for_dns': bool(0),
            }
r = requests.post('https://11.48.119.119/wapi/v1.2/record:host',
                  data=json.dumps(post_data),
                  auth=('user', 'password'),
                  verify=False)
print r.text
