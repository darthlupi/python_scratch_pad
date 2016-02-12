#!/usr/bin/python
import os, sys, socket, ipaddress

def get_ip(hostname):
  ip = socket.gethostbyname(hostname) 
  return ip

def get_network_info(lines,ip):
   network = []
   for line in lines:
     line = line.rstrip('\n')
     network_info = line.split('\t')
     network = unicode(network_info[1] + network_info[2])
     addr4 = ipaddress.ip_address( unicode(ip) )
     try:
       if addr4 in ipaddress.ip_network(network):
	  print ip + " Network: " + network_info[1] + network_info[2] + " Site: " + network_info[0]     
     except Exception, e:
       do = "nothing" 

def open_file(file):
  try:
    file_object = open(file)
    lines = file_object.readlines(  )
    file_object.close(  )
    return lines
  except Exception, e:
    print str(e)
    sys.exit()

def arg_check(provided,expected):
  if provided != expected:
    print "Wrong number of arguments..."
    help()
    sys.exit()

def main ():
  arg_check( len(sys.argv),3 )
  hostname = sys.argv[1]
  ip = get_ip(hostname)
  lines = open_file(sys.argv[2])
  get_network_info(lines,ip)

if __name__ == '__main__':
  try:
    main()
  except Exception, e:
    print str(e)
    sys.exit()  
