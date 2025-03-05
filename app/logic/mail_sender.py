import smtplib
from email.message import EmailMessage
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailSender:
    def __init__(self, provider, **kwargs):
        self.provider = provider.lower()

        if self.provider == "smtp":
            self.smtp_server = kwargs["smtp_server"]
            self.port = kwargs.get("port", 587)
            self.username = kwargs["username"]
            self.password = kwargs["password"]
        elif self.provider == "sendgrid":
            self.api_key = kwargs["api_key"]
        else:
            raise ValueError("Unsupported email provider. Use 'smtp' or 'sendgrid'.")

    def send_email(self, to, subject, body):
        if self.provider == "smtp":
            msg = EmailMessage()
            msg.set_content(body)
            msg["Subject"] = subject
            msg["From"] = self.username
            msg["To"] = to

            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

        elif self.provider == "sendgrid":
            message = Mail(from_email=self.username, to_emails=to, subject=subject, plain_text_content=body)
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            return response.status_code




if __name__ == '__main__':
    # send by smtp
    email = EmailSender(provider="smtp", smtp_server="smtp.example.com", username="your_email@example.com",
                        password="your_password")
    email.send_email("recipient@example.com", "Test Email", "Hello, this is a test email!")

    # Send Email via SendGrid
    email_sendgrid = EmailSender(provider="sendgrid", api_key="your_sendgrid_api_key",
                                 username="your_email@example.com")
    print(email_sendgrid.send_email("recipient@example.com", "Test Email", "Hello from SendGrid!"))
