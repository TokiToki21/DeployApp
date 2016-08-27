
class Users(object):
    def __init__(self, email, password, permissions):
        self.email = email.title()
        self.password = password
        self.permissions = permissions
