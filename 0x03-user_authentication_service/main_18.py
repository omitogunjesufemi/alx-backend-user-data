#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

print(auth.create_session(email))
print(auth.create_session("unknown@email.com"))

reset_token = auth.get_rest_password_token(email)
print(f"Reset Token: {reset_token}")

auth.update_password(reset_token, "Jesus loves me")
