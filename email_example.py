
#
# Simple Python example how to send email using Gmail server.
#
# NB: Note that in this simple example the email password is stored right in this file.
#
# NB: For the Gmail account we are using to send this email ("857lab@gmail.com"), need to turn ON "Less secure app access".
#     Do this by logging into the Google account; go to Settings ==> Security and look for "Less secure app access".  If this
#     method of sending email hasn't been used in a while, Google will automatically turn this option OFF and you will need to
#     log back in and turn it ON again.
#


import smtplib
from email.mime.text import MIMEText


def main():
    emailAlert()


def emailAlert():
    from_em_addr = "857lab@gmail.com"
    from_em_password = "XXXXXXXXXX"
    server_name = "smtp.gmail.com"
    to_em_addr = ["john.wilson@erigo.com", "johnpwilson3@gmail.com"]
    email_msg_str = "This is a test email from John!"
    email_subject_str = "Test email"
    try:
        server = smtplib.SMTP(server_name, 587)
        server.starttls()
        server.login(from_em_addr, from_em_password)
        msg = MIMEText(email_msg_str)
        msg['Subject'] = email_subject_str
        msg['From'] = from_em_addr
        for i in range(len(to_em_addr)):
            msg['To'] = to_em_addr[i]
            server.sendmail(from_em_addr, to_em_addr[i], msg.as_string())
        server.quit()
        print "email notification sent"
    except:
        print "_-_-_-_-_-_-_-_-  ERROR _-_-_-_- _-_-_-_- "
        print "_-_-_-_-_-_-_ EMAIL NOT SENT _-_-_-_-_-_- "

main()
