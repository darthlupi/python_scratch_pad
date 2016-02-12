#!/usr/bin/python
import os, sys, socket, ipaddress
import dns.resolver
def is_it_ip(is_it):
  try:
    socket.inet_aton(is_it)
    return True 
  except socket.error:
    return False 
def get_ip(host):
  ip = '' 
  error = ''
  try:
    ip = socket.gethostbyname(host) 
  except Exception, e:
    error = str(e) 
  return ip + error

def get_reverse_dns(ip):
  answers = []
  error = ""
  try:
    answers = dns.reversename.from_address(ip)
  except Exception, e:
    error =  str(e)
  if error:
    hosts = error
  else:
    hosts = ','.join(str(v) for v in answers)
  print answers
  return hosts 

def get_reverse_dns_socket(ip):
  hosts = []
  error = ""
  try:
    hosts = socket.gethostbyaddr(ip)
  except Exception, e:
    error = str(e)
  if error:
    hosts = error
  else:
    hosts = ','.join(str(v) for v in hosts)
  return hosts 

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
  arg_check( len(sys.argv),2 )
  lines = open_file(sys.argv[1])
  for host in lines:
    host = host.rstrip('\n')
    #If the entry is an ip already just do the reverse lookup
    if is_it_ip(host):
      #print "Existing host entries for " + host + " are:" + get_reverse_dns(host)
      print "IP: " + host + " = " + get_reverse_dns_socket(host) 
    #This entry is possibly a host.  Let's try to get the IP Address and then all of dns entries for it. 
    else:
      ip = get_ip(host) 
      print "Host: "  + host + " = " + get_reverse_dns_socket(get_ip(host) )

if __name__ == '__main__':
  try:
    main()
  except Exception, e:
    print str(e)
    sys.exit()  
