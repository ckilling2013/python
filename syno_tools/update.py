#!/usr/bin/python

import ipgetter
import argparse
from route53_update import Route53
import os.path
import sys
from utilities import load_file
from utilities import dump_file

def ddns_update(self):

    if os.path.isfile(self.filename):
        json_data = load_file(self.filename)
        json_data['status'] = False
    else:
        json_data = {}
        json_data['status'] = True
        

    route53 = Route53(self.hosted_zone_id)
    route53.target = ipgetter.myip()

    if self.host in json_data and json_data['status'] is False:
        try:
            if json_data[self.host] != route53.target:
                print 'Delete and Recreate is required'
                request = {"delete": True, "update": True, "ttl": 30}
            else:
                print "No Action Needed"
                sys.exit(0)
        except (NameError, KeyError):
            request = {"delete": False, "update": True, "ttl": 30}

        route53.host = self.host
        route53.record_type = self.record_type
        if route53.update_route53(request) is True:
            json_data['status'] = True

    json_data[self.host] = route53.target
    dump_file(json_data, self.filename)


def main():
    """ Command Line Callable """
    """ Arg processing if directly called """
    msg = 'Configure and Create a stack based on inputs'

    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("--hosted_zone_id",
                        type=str,
                        help="Route53 Hosted ID Zone",
                        required=True)
    parser.add_argument("-c",
                        "--host",
                        type=str,
                        help="Host",
                        required=True)
    parser.add_argument("-f",
                        "--filename",
                        type=str,
                        help="Holder File(also include dir)",
                        required=False,
                        default='/tmp/ip_finder')
    parser.add_argument("-t",
                        "--record_type",
                        type=str,
                        help="Type",
                        required=True)

    ddns_update(parser.parse_args())

if __name__ == "__main__":
    main()
