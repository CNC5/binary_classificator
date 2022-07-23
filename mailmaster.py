import smtplib
host = 'smtp.gmail.com'
port = 465
server = smtplib.SMTP_SSL(host, port)


class fetcher():
	def login(self, *credentials):
		login, atoken = credentials
		self.mb = MailBox(server).login(login, atoken)

	def fetch(self, spec_mail):
		messages = self.mb.fetch(criteria=\
				AND(seen=False, from_=spec_mail),\
				mark_seen=False,\
				bulk=True)

		return messages
