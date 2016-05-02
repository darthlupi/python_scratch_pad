#!/usr/bin/python
import sys, optparse

def print_stuff():
    print "\nCaptured ctrl+c!"

def exit_clean():
    print_stuff()
    sys.exit(0)

def main():

    usage = "usage: %prog --option [string] "
    parser = optparse.OptionParser(usage)
    parser.add_option("--option", dest="option", type="string", help="Specify option: --option")
    options, arguments = parser.parse_args()

    print "This is your option: %s" % ( options.option )

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
        exit_clean()
