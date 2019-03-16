#!/usr/bin/python
""" Auto check of UPS status and email / notify somemone """
import commands
import argparse
from mailjet_rest import Client

class Email:
    """ API EMAIL using mail jet """
    def __init__(self, args):
        self.server = args.server
        self.message = None
        self.toemail = None
        self.frm = args.frm
        self.subject = None
        self.text = None

    def mail_jet_send(self):
        """ Construct Email and send """
        mailjet = Client(auth=(self.api_key, self.api_secret), version='v3.1')

        ## Build the data object ##
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": self.frm,
                        "Name": "Service Account"
                    },
                    "To": [
                        {
                            "Email": self.toemail,
                            "Name": ""
                        }
                    ],
                    "Subject": self.subject,
                    "TextPart": self.text
                }
            ]
        }

        result = mailjet.send.create(data=data)
        print result.status_code
        print result.json()


def response(self, args):
    """ Process and Build Response based on input """
    if self['HR'] == 'Online':
        print "ALL IS GOOD.  No response necessary"
    else:
        mail = Email(args)
        mail.subject = "UPS Notification"
        mail.text = self['text']
        mail.toemail = args.to
        mail.mail_jet_send()


def main():
    """ Check UPS status and email a response """
    parser = argparse.ArgumentParser(description='Configure elasticsearch config files')
    parser.add_argument("--server",
                        type=str,
                        required=False,
                        default='172.1.1.55',
                        help="Hostname")

    parser.add_argument("-f",
                        "--frm",
                        type=str,
                        default='service@killingsworthcomputing.com',
                        help='Email-From')

    parser.add_argument("-t",
                        "--to",
                        type=str,
                        help='To',
                        default='4083156891@tmomail.net')

    args = parser.parse_args()

    valid_results = {
        "OL": {"HR": "Online", "text": "UPS: Status OK"},
        "LB": {"HR": "Low Battery", "text": "UPS: Battery Low"},
        "SD": {"HR": "Shutdown Load", "text": "UPS: is over-subscribed"},
        "CP": {"HR": "Cable Power", "text": "UPS: on Cable Power"},
        "CTS": {"HR": "Clear to Send", "text": "UPS: Clear to Send"},
        "RTS": {"HR": "Ready to Send", "text": "UPS: Ready to Send"},
        "DCD": {"HR": "Data Carrier Detect", "text": "UPS: Data Carrier Detect"},
        "RNG": {"HR": "Ring Indicate", "text": "UPS: Ring Indicate"},
        "DTR": {"HR": "Data Terminal Ready", "text": "UPS: Data Terminal Ready"},
        "ST": {"HR": "Send a Break", "text": "UPS: Send a Break"}
        }

    actionable_results = ['OL', 'LB', 'SD']

    for i in commands.getstatusoutput('upsc ups@localhost ups.status'):
        if i in valid_results and i in actionable_results:
            response(valid_results[i], args)

if __name__ == "__main__":
    main()
