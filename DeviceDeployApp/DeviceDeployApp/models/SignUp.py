from werkzeug.security import generate_password_hash, check_password_hash

class SignUp(object):
    def __init__(self, first, last, email, password):
        self.first = first.title() 
        self.last = last.title()
        self.email = email
        self.password = generate_password_hash(password)

    