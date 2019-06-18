import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self, login, password, smtr_host, smtr_port, imap_host):
        self.login = login
        self.password = password
        self.smtr_host = smtr_host
        self.smtr_port = int(smtr_port)
        self.imap_host = imap_host

    def send_mail(self, subject, message, *args):
        recipients_list = list(args)
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients_list)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        message_send = smtplib.SMTP(self.smtr_host, self.smtr_port)
        message_send.ehlo()
        message_send.starttls()
        message_send.ehlo()
        message_send.login(self.login, self.password)
        message_send.sendmail(self.login, recipients_list, msg.as_string())
        message_send.quit()

    def recieve_mail(self, header=None):
        mail = imaplib.IMAP4_SSL(self.imap_host)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(str(raw_email))
        mail.logout()


if __name__ == '__main__':
    snich69 = Mail('login@gmail.com', 'qwerty', 'smtp.gmail.com', '587', 'imap.gmail.com')
    snich69.send_mail("it's subject", "It's message", 'vasya@email.com', 'petya@email.com')
    snich69.recieve_mail()
