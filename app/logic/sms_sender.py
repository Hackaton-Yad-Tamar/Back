from twilio.rest import Client
import vonage


class SMSSender:
    def __init__(self, provider, **kwargs):
        self.provider = provider.lower()

        if self.provider == "twilio":
            self.client = Client(kwargs["account_sid"], kwargs["auth_token"])
            self.from_number = kwargs["from_number"]
        elif self.provider == "vonage":
            self.client = vonage.Client(key=kwargs["api_key"], secret=kwargs["api_secret"])
        else:
            raise ValueError("Unsupported SMS provider. Use 'twilio' or 'vonage'.")

    def send_sms(self, to, message):
        if self.provider == "twilio":
            msg = self.client.messages.create(body=message, from_=self.from_number, to=to)
            return msg.sid
        elif self.provider == "vonage":
            response = self.client.sms.send_message({"from": "Vonage", "to": to, "text": message})
            return response


if __name__ == '__main__':
    # Send SMS via Twilio
    sms = SMSSender(provider="twilio", account_sid="your_sid", auth_token="your_token", from_number="+1234567890")
    print(sms.send_sms("+0987654321", "Hello from Twilio!"))

    # Send SMS via Vonage
    sms_vonage = SMSSender(provider="vonage", api_key="your_api_key", api_secret="your_api_secret")
    print(sms_vonage.send_sms("+0987654321", "Hello from Vonage!"))