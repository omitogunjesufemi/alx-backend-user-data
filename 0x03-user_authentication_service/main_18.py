#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

session_id = auth.create_session(email)
print(session_id)
print(auth.create_session("unknown@email.com"))

user = auth.get_user_from_session_id(session_id)
print(f"User: {user.email}, {user.hashed_password}")

reset_token = auth.get_rest_password_token(email)
print(f"Reset Token: {reset_token}")

auth.update_password(reset_token, "Jesus loves me")
user = auth.get_user_from_session_id(session_id)
print(f"User: {user.email}, {user.hashed_password}")
