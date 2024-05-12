import pickle 
import db_connection  #importing database connection 
import streamlit_authenticator as stauth 
from pathlib import Path 

users = db_connection.get_users()
usernames = []
names = []
passwords = []

for user in users:
    '''obtaining all registered email ids and passwords'''
    usernames.append(str(user["EMAIL"]))
    names.append(str(user["ENAME"]))    
    passwords.append(str(user["PASSWORD"]))
    
hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)
