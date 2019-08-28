import re


class Validators:
    def valid_destination_name(self, destination):
        ''' validate destination name '''
        regex = "^[a-zA-Z0-9_ ]{1,}$"
        return re.match(regex, destination)

    def valid_origin_name(self, origin):
        ''' validate origin name '''
        regex = "^[a-zA-Z0-9_ ]{2,}$"
        return re.match(regex, origin)

    def valid_name(self, username):
        """ Valid username """
        return re.match("^[a-zA-Z0-9]{2,}$", username)

    def valid_password(self, password):
        """validate for password """
        return re.match("^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$",
                        password)

    def valid_email(self, email):
        """ validate for email """
        return re.match("^[^@]+@[^@]+\.[^@]+$", email)
