from email_validator import validate_email, EmailNotValidError

def _validate_email(email):
    msg = ""
    valid = False
    try:
        valid = validate_email(email)
        email = valid.email
        valid = True
    except EmailNotValidError as e :
        msg = str(e)
    return valid, msg, email       