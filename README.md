# EmailNotifier
A Notification system based on sending emails and email-to-sms messages. Should be generalizable so that other platforms can be exploited as needed. 

Sample email generation code sent from John. Very similar to what we use
in LiAn's AuthEndpoints, including reduced security setting requirement
in Gmail.

A few notes:

-	the email password is stored in plain text in these source code files; obviously not the best solution
-	the way these examples connect to the Gmail server, you need to turn on “Less secure app access” in the associated Google account (I describe this in the header of each source code file)
-- A better alternative is to use the Gmail API with OAth 2.0 credentials; see the following URL for details: https://blog.mailtrap.io/send-emails-with-gmail-api/
-	You can send an email that will be received as a Text message (email to SMS gateway); Google “email to text” to see how
