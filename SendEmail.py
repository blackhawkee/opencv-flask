import smtplib
from email.message import EmailMessage
email = EmailMessage()
TEST_EMAIL = 'marricksteve@gmail.com'
email['from'] = TEST_EMAIL
email['to'] = TEST_EMAIL
email['subject'] = 'Test - Abnormal Event Detected'
email.set_content('Abnomal Event Detected in the Video Processing')

def email_alert():
	with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()
		smtp.login(TEST_EMAIL, 'uhrkwpnrtzuupysb')
		smtp.send_message(email)
		# print('The mail was sent!')