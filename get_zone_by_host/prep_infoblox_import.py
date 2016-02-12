#!/usr/bin/python
import os, sys, socket, ipaddress, operator
from struct import pack

def getKey( key ) :
    return key[1] ;

def prepForInfoblox(lines):
  network = []
  file_content = []
  for line in lines:
    line = line.rstrip('\n')
    network_info = line.split('\t')
    #Print the header
    #Get the dot notation netmask
    try:
      mask_stripped = int(network_info[2].lstrip('/'))
      dotmask = str(calcDottedNetmask(mask_stripped ))
      file_content.append( [ "network",network_info[1],dotmask,network_info[0],mask_stripped ] )
    except Exception, e:
      skip = "true that"
  
  #Sort the networks by netmask so that they are inserted in the right order
  #file_content = file_content.sort(operator.itemgetter[2] ) 
  #Create Header
  
  file_content = sorted(file_content, key=operator.itemgetter(4) ) ;
  file_content.insert( 0,[ "header-network","address*","netmask*","EA-Site" ])
  return file_content ;

def calcDottedNetmask(mask):
    #This function will return a dot style netmask from a CIDR
    bits = 0
    for i in xrange(32-mask,32):
        bits |= (1 << i)
    return socket.inet_ntoa(pack('>I', bits))

def openFile(file):
  try:
    file_object = open(file)
    lines = file_object.readlines(  )
    file_object.close(  )
    return lines
  except Exception, e:
    print str(e)
    sys.exit()

def argCheck(provided,expected):
  if provided != expected:
    print "Wrong number of arguments..."
    help()
    sys.exit()

def main ():
  argCheck( len(sys.argv),2 )
  lines = openFile(sys.argv[1])
  output  = prepForInfoblox(lines)
  for f in output :
   print f[0] + ", " + f[1] +", " + f[2] + ", " + f[3];


if __name__ == '__main__':
  try:
    main()
  except Exception, e:
    print str(e)
    sys.exit() 
