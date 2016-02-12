#!/usr/bin/python
import os, sys, socket, ipaddress
def get_ip(host):
  ip = '' 
  error = ''
  try:
    ip = socket.gethostbyname(host) 
  except Exception, e:
    error = str(e) 
  return ip + error


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
    ip = get_ip(host) 
    print host + "," + ip + ",B001" 

if __name__ == '__main__':
  try:
    main()
  except Exception, e:
    print str(e)
    sys.exit()  
