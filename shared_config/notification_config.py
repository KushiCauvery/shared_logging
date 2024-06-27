import os

# SMTP SERVER CREDENTIALS
SEND_EXCEPTION_NOTIFICATIONS_TO_EMAIL = "hdfclife-server-updates@kuliza.com"

#Email SMTP Credentials
USE_SMTP_SSL = True
SMTP_USERNAME = 'hdfclifedev@gmail.com'
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_PORT = 465
SMTP_DOMAIN = 'smtp.gmail.com'
SMTP_FROM_EMAIL = 'hdfclifedev@gmail.com'
SUPPORT_EMAIL = 'HDFC Life Support - no reply <support@hdfclife.com>'
REPLY_TO_ADDRESS = 'no-reply@hdfclife.com'
INVESTOR_EMAIL = 'HDFC Life - Investor Relations <investorrelations@hdfclife.com>'

CUSTOM_FROM_EMAIL_ID = {
    'Group_Term_Insurance': 'onlinegi@hdfclife.com',
    'customer_concern': 'channelp@hdfclife.com'
}