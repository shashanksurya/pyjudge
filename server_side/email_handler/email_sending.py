import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_id = "einstein.newton.ta@gmail.com"
#sender_pass = open("pass_file", "r").read()
sender_pass = "takokaam"

def send_email(authenticated_server, sender, receiver, msg):
    """ Sending emails. Assume authentication has already been done.
    """
    authenticated_server.sendmail(sender, receiver, msg)


def get_auth_server(username="einstein.newton.ta@gmail.com", password=sender_pass):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(username, password)
    return server


def compose_message(from_addr, to_addr, subject, body):
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    return msg.as_string()


if __name__ == "__main__":
    print(test_msg())
