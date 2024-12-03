import cv2
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# Function to capture image
def capture_image():
    cam = cv2.VideoCapture(0)  # 0 is the default camera
    if not cam.isOpened():
        print("Failed to access the camera")
        return None

    result, image = cam.read()
    if result:
        # Define the filename
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        # Save the image
        cv2.imwrite(filename, image)
        print(f"Image saved as {filename}")
        cam.release()  # Release the camera
        return filename  # Return the path of the saved image
    else:
        print("Failed to capture image")
        cam.release()
        return None


# Function to send the captured image via email
def send_email(image_path):
    if image_path is None:
        print("No image to send")
        return 

    sender_email = "sender_emails"
    receiver_email = "receiver_email"
    password = "Use app-specific password"

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Laptop Access Detected"

    # Attach the file
    with open(image_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(image_path)}")
        msg.attach(part)

    # Sending the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use port 587 for TLS
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Email sent with attachment {os.path.basename(image_path)}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()


if __name__ == "__main__":
    image_path = capture_image()  # Capture the image
    send_email(image_path)  # Send the captured image via email
