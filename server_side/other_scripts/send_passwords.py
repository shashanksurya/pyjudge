import os
BASE_DIR = os.getcwd()
import sys
sys.path.append(BASE_DIR)

import time
from email_handler import (send_email,
                           get_auth_server,
                           compose_message,
                           sender_id)

from users_passwords import USERS_PASSWORDS

email_ids = [val + "@my.fsu.edu" for val in USERS_PASSWORDS.keys()]     #if val not in ["bp11d", "pkumar"]]

server = get_auth_server()
subject = "Python Class, Fall 2014: Script to submit solutions"
msg_body = """
#!/bin/bash

#######################################################

if [ "$#" -eq 2 ]; then

    unset pyclass_username
    unset pyclass_password

    echo "Enter username:"
    read pyclass_username

    echo "Enter password"
    read -s pyclass_password

    curl -F "file=@$2" -F "enctype=multipart/form-data" "http://128.186.61.238/:5000/user/$pyclass_username/password/$pyclass_password/upload/$1"
else

    printf "\nUsage:\n\t ./submit <problem_no> <file_name>\n\n"

fi

#######################################################
           """
for userid, password in USERS_PASSWORDS.items():
    if userid not in ["pkumar"]:
        receiver = userid + "@my.fsu.edu"
        #msg_body = password
        msg = compose_message(sender_id, receiver, subject, msg_body)
        send_email(server, sender_id, receiver, msg)
        time.sleep(1)
