import re

# Make a regular expression
# for validating an Email
email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

# for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

# Define a function for
# for validating an Email
def check_mail(email):
    # pass the regular expression
    # and the string in search() method
    if (re.search(email_regex, email)):
        return True
    return False


