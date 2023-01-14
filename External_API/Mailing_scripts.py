### Sending emails with the Postmark Python library
from dotenv import load_dotenv
load_dotenv()
import os
from postmarker.core import PostmarkClient

def send_email(receiver_email,receiver_name):
    postmark = PostmarkClient(server_token= os.getenv('Posmarker_Server_Token'))
    postmark.emails.send(
        From='contact@crypto-goose.com',
        To=receiver_email,
        Subject='Postmark test',
        HtmlBody= f"<div className='email' style='\
            border: 1px solid black;\
            padding: 20px;\
            font-family: sans-serif;\
            line-height: 2;\
            font-size: 20px;\
            '>\
            <h2> Hello There, {receiver_name}!</h2>\
            <p>Test Email</p>\
            <p> Crypto Goose Team</p>\
            </div>"\
     )
receiver_name = "bill"

send_email('contact@crypto-goose.com',receiver_name)
