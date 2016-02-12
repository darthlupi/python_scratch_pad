#!/usr/bin/python
import infoblox
import argparse
import getpass


def get_args():
    """Get command line args from the user.
    """
    parser = argparse.ArgumentParser(
        description='Standard Arguments for talking to vCenter')

    # because -h is reserved for 'help' we use -s for service
    parser.add_argument('-f', '--fqdn',
                        required=True,
                        action='store',
                        help='FQDN of host to add to DNS')

    # because we want -p for password, we use -o for port
    parser.add_argument('-n', '--network',
			required=True,
                        action='store',
                        help='Network in CIDR notation ')
    args = parser.parse_args()
    return args
ip = ''
args = get_args()

iba_api = infoblox.Infoblox('infoblox.host.com' ,'user', 'password', '1.6', 'default', 'default',False)

try:
    ip = iba_api.get_next_available_ip(args.network)
    print "Next Available IP = " + ip
except Exception as e:
    print e

try:
    host = iba_api.create_host_record_no_dns(ip, args.fqdn)
except Exception as e:
    print e

print "FQDN: " + args.fqdn + " has been assigned the IP Address of: " + ip
