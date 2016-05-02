#!/usr/bin/python
#
#Description:
# This script will take a port as an argument and wait a specific time testing it every 10 seconds for availablitity.
#Modified:
# 5/2/2016 - Robert Lupinek
#Example for hostname host, wait for SSH to become available for 300 seconds:
# wait_for_port.py --host host --port 22 --wait 300
import sys, optparse, socket, time

def print_stuff():
    print "\nCaptured ctrl+c!"

def exit_clean():
    print_stuff()
    sys.exit(0)

def test_port(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print "Port %s on host %s is reachable." % (port,host)
        return 1
    except socket.error as e:
        print "Error on connect: %s" % e
        return 0
    s.close()


def main():

    usage = "usage: %prog --host [string] --port [integer] --wait [integer]"
    parser = optparse.OptionParser(usage)
    parser.add_option("--host", dest="host", type="string", help="Specify option: --host")
    parser.add_option("--port", dest="port", type="int", help="Specify option: --port")
    parser.add_option("--wait", dest="wait", type="int", help="Specify option: --wait")
    options, arguments = parser.parse_args()

    print "Testing port %s on host %s for %s seconds..." % ( options.port, options.host, options.wait )


    seconds = int(options.wait)
    loop = True
    while loop:
        #Get the port status every 10 seconds or when seconds <= 0
        if seconds % 10 == 0 or seconds <= 0 or seconds == options.wait:
            results = test_port(options.host,options.port)
            if results:
                #Success!
                sys.exit(0)
        if seconds == -1:
            print "looping forever! Press CTRL+C to exit..."
        if seconds % 10 == 0 or seconds <= 0:
            if seconds > 0:
                print "looping for another %s seconds..." % ( seconds )
        seconds -= 1
        #If still looping sleep for 1 second
        if loop:
            time.sleep(1)
        #Timed out :(
        if seconds == 0:
            print "ERROR: Could not connect to port %s on host %s in time specified." % ( options.port, options.host )
            print "Time specified = %s seconds."  % ( options.wait )
            sys.exit(1)
            loop = False

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
        exit_clean()
