import re
def validate_email(userid):
    pattern='^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(pattern,userid):
        print("Valid email id")
    else:
        print("Invalid email id")
# user_id=input('enter the email id:')
# validate_email(user_id)