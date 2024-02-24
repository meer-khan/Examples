# import yagmail

# # Replace with your Outlook email address and generated app password
# outlook_email = "alert@morrowai.com"
# app_password = "Mob85330"

# # Email configuration for Outlook
# yag = yagmail.SMTP(outlook_email, app_password)

# # Send email example
# to_email = "shahmirkhan519@gmail.com"
# subject = "Test Email"
# body = "This is a test email sent through yagmail."

# # Compose and send the email
# yag.send(to=to_email, subject=subject, contents=[body])

# # Close the SMTP connection
# yag.close()



import smtplib
from email.mime.text import MIMEText
from icecream import ic
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config
# Set up the SMTP connection
smtp_server = "smtp.office365.com"
smtp_port = 587
# smtp_user = "a@morrowai.com"
# smtp_password = "Mob85330"
smtp_user = config("EMAIL")
smtp_password = config("EMAIL_PASSWORD")

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_user, smtp_password)

# Compose and send the email
subject = "Test Email"
body = "This is a test email sent through SMTP."

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = smtp_user
msg["To"] = "shahmirkhan519@gmail.com"

error = server.sendmail(smtp_user, ["shahmirkhan519@gmail.com"], msg.as_string())
ic(error)
# Close the SMTP connection
server.quit()
