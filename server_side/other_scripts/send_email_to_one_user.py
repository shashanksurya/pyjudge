import os
BASE_DIR = os.getcwd()
import sys
sys.path.append(BASE_DIR)

from email_handler import (send_email,
                           get_auth_server,
                           compose_message,
                           sender_id)


server = get_auth_server()
subject = "Python Class, Fall 2014: Sample email."
receiver = "piyush@acm.org"
receiver = "bpforfacebook@gmail.com"
msg = compose_message(sender_id, receiver, subject, "I don't know if this email address, einstein.newton.ta is fine.")
send_email(server, sender_id, receiver, msg)
