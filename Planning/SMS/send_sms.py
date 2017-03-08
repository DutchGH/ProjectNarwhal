from twilio.rest import TwilioRestClient

account_sid = "AC42c2463c98d3496745c2eb91784d3a5c" # Account SID from www.twilio.com/console
auth_token  = "e6b2ef7f4f3068bbf9a6ec80d6d2df5b"  # Auth Token from www.twilio.com/console

client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(body="Hello there matey",
    to="+447866109418",    # phone number
    from_="+441344567727") # Twilio number

print(message.sid)
