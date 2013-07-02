from settings import SMTP_USER, SMTP_PASSWORD, HOST_NAME
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_smtp_mail(message,to):
	gmail_user = SMTP_USER
	gmail_pwd = SMTP_PASSWORD 
	msj = MIMEMultipart('alternative')
	msj['FROM'] = gmail_user
	msj['Subjent'] = "cotiwin"
	msj.attach(MIMEText(message, 'html', 'UTF-8'))
	smtpserver = SMTP("smtp.gmail.com",587) 
	smtpserver.ehlo() 
	smtpserver.starttls() 
	smtpserver.ehlo()
	smtpserver.login(gmail_user, gmail_pwd) 
	smtpserver.sendmail(gmail_user, to, msj.as_string())
	smtpserver.close()