import os
BASE_DIR = os.getcwd()
import sys
sys.path.append(BASE_DIR)

import string
from random import choice

chars = string.digits

userids = ["ca11h",
"ca13",
"mca12",
"ab10ae",
"smc10e",
"hmc13f",
"swf11",
"si13f",
"kak12f",
"dl10f",
"ll13j",
"jl11ah",
"ncm09g",
"mm13ag",
"am11s",
"dop11",
"jp13ab",
"rp13t",
"gs13h",
"ss12an",
"kv13c",
"mb11r"
]

user_pass = {}
for user in userids:
    user_pass[user] = ''.join(choice(chars) for _ in range(5))

user_pass["pkumar"] = "00000"
user_pass["bp11d"] = "11111"
user_pass["mb11r"] = "22222"

fp = open("users_passwords.py", "w")
fp.write("USERS_PASSWORDS = " + str(user_pass))
fp.close()
