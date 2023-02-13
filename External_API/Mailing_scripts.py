### Sending emails with the Postmark Python library
import io
from dotenv import load_dotenv
load_dotenv()
import os
from postmarker.core import PostmarkClient

def send_email(receiver_email,receiver_name):
    postmark = PostmarkClient(server_token= os.getenv('Posmarker_Server_Token'))
    postmark.emails.send(
        From='contact@crypto-goose.com',
        To=receiver_email,
        Subject='Welcome to Crypto Goose',
        HtmlBody= io.open("External_API/email_template.html", 'r').read()
    )
#receiver_name = "bill"

#send_email('dudeabides3000@gmail.com',receiver_name)
