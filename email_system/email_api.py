from fastapi import FastAPI, File, UploadFile, HTTPException
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from decouple import config
from icecream import ic
app = FastAPI()

def send_email_with_image(image_path, recipient_email):
    # Your email credentials
    sender_email = config("EMAIL")
    sender_password = config("EMAIL_PASSWORD")

    # Create the MIME object
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = "Image Attachment"

    # Attach the image
    ic(image_path)
    with open(image_path, "rb") as image_file:
        image_data = MIMEImage(image_file.read(), name="image.jpg")
        msg.attach(image_data)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

@app.post("/send_image_email")
async def send_image_email( email: str = "", file: UploadFile = File(...),):
    # Check if recipient email is provided
    recipient_email = email
    ic(recipient_email)
    if not recipient_email:
        raise HTTPException(status_code=400, detail="Recipient email is required")

    try:
        # Save the uploaded image to a temporary file
        temp_image_path = f"temp_{file.filename}"
        with open(temp_image_path, "wb") as temp_image:
            temp_image.write(file.file.read())

        # Send the email with the image attachment
        send_email_with_image(temp_image_path, recipient_email)

        # Remove the temporary image file
        os.remove(temp_image_path)

        return {"message": "Email sent successfully"}

    except Exception as ex:
        ic(ex)
