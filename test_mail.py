from flask_mail import Mail, Message
from flask import Flask

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp-mail.outlook.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='Aurorra1123@outlook.com',
    MAIL_PASSWORD='fgggsfrekkulguvc'
)

mail = Mail(app)

with app.app_context():
    try:
        msg = Message('Test Email',
                    sender='Aurorra1123@outlook.com',
                    recipients=['Aurorra1123@outlook.com'])
        msg.body = 'This is a test email.'
        mail.send(msg)
        print('Email sent successfully')
    except Exception as e:
        print(f'Error sending email: {e}') 