# !/usr/bin/env python
##############################################################################
# send_mail.py
# Command to wrap secure mail functionality and send emails to one or more
# users.
# https://github.com/DigiLog-N/EmailNotifier
# Copyright 2020 Canvass Labs, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################
from smtplib import SMTP, SMTPHeloError, SMTPAuthenticationError, SMTPNotSupportedError, SMTPException, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError
from email.mime.text import MIMEText
from socket import gaierror
from argparse import ArgumentParser


class TLSUser:
    def __init__(self, host, port, user, password, verify_parameters=False):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.smtp = None

        if verify_parameters:
            # Attempt to connect to the server on object creation, so that if
            # parameters are incorrect, the user finds out that the object
            # is invalid now, rather than later. Assume that any smtp servers
            # going down would continue to be down for the send() call
            # anyway.
            self._login()
            self._disconnect()

    def _login(self):
        # create and initialze the SMTP object
        smtp = SMTP(self.host, self.port)
        # starttls() performs connection negotiation before login
        smtp.starttls()
        # log into TLS Secured connection with username and password.
        smtp.login(self.user, self.password)

        # if no exceptions occurred, then this object is good.
        # allow member tobe non-null w/good objects only.
        self.smtp = smtp
        #self.smtp.set_debuglevel(1)

    def _disconnect(self):
        self.smtp.quit()
        # once quit() has been called, the object does not appear to remain valid.
        self.smtp = None

    def send(self, subject, message, list_of_recipients, hangup=True):
        '''
        Simple send, where multiple recipients are always visible to each other.
        :param subject: subject line of the message
        :param message: the text of the message
        :param list_of_recipients: a list of one or more email addresses.
        :param hangup: hangs up after sending message. Set to False to prevent having to reconnect w/in a loop.
        :return: None if successful. Raises Error if unsuccessful.
        '''
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.user
        msg['To'] = ", ".join(list_of_recipients)

        if not self.smtp:
            self._login()

        # any email addresses in the list that are obviously invalid such as 'il.com' or 'foo' will be returned in
        # invalid_addresses. Addresses that are valid, but happen to not exist, such as 'non.existant.user@gmail.com'
        # will still be successful.
        invalid_addresses = self.smtp.sendmail(self.user, list_of_recipients, msg.as_string())

        if invalid_addresses:
            raise ValueError("The following addresses are invalid: %s" % ' '.join(invalid_addresses.keys()))

        if hangup:
            self._disconnect()


class GMailUser(TLSUser):
    def __init__(self, user, password, verify_parameters=False):
        self.host = "smtp.gmail.com"
        self.port = 587
        super().__init__(self.host, self.port, user, password, verify_parameters=verify_parameters)


def main(user, password, subject, message, addressed_to):
    try:
        email_alert = GMailUser(user, password, verify_parameters=False)
        email_alert.send(subject, message, addressed_to, hangup=True)
    except SMTPHeloError as e:
        raise ValueError("I said HELO, but the server ignored me: %s" % str(e))
    except SMTPAuthenticationError as e:
        raise ValueError("The SMTP server did not accept your username and/or password: %s" % str(e))
    except SMTPNotSupportedError as e:
        raise ValueError("The AUTH and/or SMTPUTF8 command is not supported by this server: %s" % str(e))
    except SMTPException as e:
        raise ValueError("A suitable authentication method couldn't be found: %s" % str(e))
    except gaierror as e:
        raise ValueError("Invalid SMTP host name: %s" % str(e))
    except RuntimeError as e:
        raise EnvironmentError("TLS and/or SSL support is not available to your Python interpreter: %s" % str(e))
    except SMTPRecipientsRefused as e:
        raise ValueError("All recipients were refused. Please verify your list of recipients is correct.")
    except SMTPSenderRefused as e:
        raise ValueError("Sender refused From=%s: %s" % (user, str(e)))
    except SMTPDataError as e:
        # TODO: This should probably be a different kind of error.
        #  consider wrapping all errors in a digilog-N specific error type.
        #  catching all of these errors here and re-raising them as a merged set of types is mainly
        #  to prevent downstream code from having to know/handle all of these very specific errors.
        #  Yet, we want to be fairly robust; we need to know if a user did not receive an email.
        raise ValueError("Server replied w/unexpected error code: %s" % str(e))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-u", "--user", help="GMail account user name", required=True)
    # TODO: this should really be replaced with a file read or something.
    parser.add_argument("-p", "--password", help="GMail account password", required=True)
    parser.add_argument("-m", "--message_file", help="text/HTML file containing message", required=True)
    parser.add_argument("-s", "--subject", help="subject line", required=True)
    parser.add_argument("-r", "--recipient", action="append", help="an intended recipient of the message", required=True)

    args = parser.parse_args()

    #addressed_to = ['user.1@gmail.com', 'user.2@gmail.com']

    print(args.recipient)

    if args.message_file:
        with open(args.message_file, 'r') as f:
            message = f.read()
            main(args.user,
                 args.password,
                 args.subject,
                 message,
                 args.recipient)
