#!/usr/bin/python
"""  Route53 Update routine """

from __future__ import print_function
import boto
from time import sleep
from termcolor import colored
import sys
from boto.route53.record import ResourceRecordSets


class Route53:
    def __init__(self, hosted_zone_id):
        self.conn = boto.connect_route53()
        self.hosted_zone_id = hosted_zone_id
        self.commited = None
        self.host = None
        self.target = None


    def update_route53(self, change_req):
        """ update a route53 entry """
        existing_entries = self.conn.get_all_rrsets(self.hosted_zone_id)
        changes = ResourceRecordSets(self.conn, self.hosted_zone_id)

        for item in existing_entries:
            if item.type == self.record_type and \
                item.name == self.host + '.' and \
                change_req['delete'] is True:
                change = changes.add_change("DELETE",
                                            self.host,
                                            item.type,
                                            ttl=item.ttl)
            #  Note: This value has to match exactly with the record
            #  but we're reading it straight from the source.
                change.add_value(item.resource_records[0])
                sleep(2)

        #  We either don't exist or need to update our existing entry
        #  (its already been deleted)
        if change_req['update'] is True:
            change = changes.add_change("CREATE", self.host, self.record_type, ttl=change_req['ttl'])
            change.add_value(self.target)

        self.commited = False
        timeout = 5

        while self.commited is False:
            try:
                self.status = changes.commit().ChangeResourceRecordSetsResponse.ChangeInfo.Status
                self.commited = True
                if 'PENDING' in self.status:
                    print (colored("Route53 OK: {} Created".format(self.host), 'green'))
                return self.commited
            except boto.route53.exception.DNSServerError as error:
                print (error)
                if timeout >= 5:
                    print ("Route53 unable to complete transaction")
                    sys.exit(1)
                if 'InvalidInput' in str(error):
                    print ({})
                    break
                else:
                    print ("Unable to make DNS entry:  Sleeping 30s -> {}".format(error))
                    sleep(30)
                timeout += 1

def main():
    """ Command Line Callable """

if __name__ == "__main__":
    main()
