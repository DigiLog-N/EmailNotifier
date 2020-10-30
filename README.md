# EmailNotifier

EMail notification implementation is now part of the DigiLog-N project. This project is kept for reference, but is no longer needed to demo DigiLog-N.

sendmail.py:	A command-line utility to send a text file (and possibly an html file) as an email message to multiple users.
The main() function in sendmail.py can be called directly from another program to incorporate sending mail functionality into your program.
All smtplib specific exceptions have been wrapped as ValueErrors and EnvironmentErrors as appropriate; there is no need to dig deep into the behavior of smtplib.

Currently, the smtp code has been fixed to use TLS (aka SSL 3+?). The GMail child class further fixes the port to the standard TLS port 587 and the host to smtp.gmail.com. This can be changed based on need.

sendmail.py superseeds previous python example.

Using SMTP with Gmail, you will have to enable 'less secure access', as John also mentioned. I will expand this sendmail.py to use our digilog-n account as well.

As John mentioned, GMail API w/OAuth 2.0 is still a worthy alternative, I'll put together a demo on the side. Primary reason to use SMTP over GMail is we're not limited to using GMail accounts or implying to the customer that they need to integrate w/GMail.

* A better alternative is to use the Gmail API with OAth 2.0 credentials; see the following URL for details: https://blog.mailtrap.io/send-emails-with-gmail-api/
-	You can send an email that will be received as a Text message (email to SMS gateway); Google “email to text” to see how
