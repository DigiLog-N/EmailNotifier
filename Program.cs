
//
// Simple C# program to send an email using Gmail server
//
// Based on the following posts:
// (1) Basic mail/SMTP function calls from: https://www.c-sharpcorner.com/article/send-text-message-to-cell-phones-from-a-C-Sharp-application/
// (2) How to set credentials from: https://stackoverflow.com/questions/2766928/how-to-set-username-and-password-for-smtpclient-object-in-net
// (3) How to deal with System.Net.Mail.SmtpException "The SMTP server requires a secure connection or the client was not authenticated. The server response was: 5.7.0 Must issue a STARTTLS command first.", code taken from:
//     https://stackoverflow.com/questions/17462628/the-server-response-was-5-7-0-must-issue-a-starttls-command-first-i16sm1806350
//
// NB: For this simple example, the Gmail account password is stored right in this file.
//
// NB: For the Gmail account we are using to send this email ("cbos.oil.spill@gmail.com"), need to turn ON "Less secure app access".
//     Do this by logging into the Google account; go to Settings ==> Security and look for "Less secure app access".  If this
//     method of sending email hasn't been used in a while, Google will automatically turn this option OFF and you will need to
//     log back in and turn it ON again.
//

using System;
using System.Net.Mail;

namespace SendEmailExample
{
    class Program
    {
        static void Main(string[] args)
        {
            String recipientStr = "john.wilson@erigo.com";
            String fromStr = "cbos.oil.spill@gmail.com";
            String subjectStr = "Hello msg";
            String mailServerStr = "smtp.gmail.com";
            String msg = "Just saying hello!";
            MailMessage message = new MailMessage(fromStr, recipientStr, subjectStr, msg);
            SmtpClient smtpClient = new SmtpClient(mailServerStr,587);
            smtpClient.UseDefaultCredentials = false;
            smtpClient.EnableSsl = true;
            smtpClient.Credentials = new System.Net.NetworkCredential("cbos.oil.spill@gmail.com", "XXXX Password XXXXXX");
            try
            {
                // 2 options for sending out the email
                // (1) synchronous method
                // smtpClient.Send(message);
                // (2) asynchronous method
                //     If we use this method, give the message a little time before quitting the program
                smtpClient.SendAsync(message,null);
                System.Threading.Thread.Sleep(5000);
                
            }
            catch (Exception ex)
            {
                Console.WriteLine("Exception caught in SendEmailExample(): {0}", ex.ToString());
            }
        }
    }
}
