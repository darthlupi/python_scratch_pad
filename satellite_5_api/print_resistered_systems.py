#!/usr/bin/python
import xmlrpclib

SAT_URL = "https://hostname/rpc/api"
SAT_USER = "username"
SAT_PASS = "password"
client = xmlrpclib.Server(SAT_URL, verbose=0)
key = client.auth.login(SAT_USER, SAT_PASS)

syslist = client.system.listSystems(key)
for sys in syslist:
  print sys['name']
