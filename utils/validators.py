import re

class Validators:
    def valid_destination_name(self,destination):
        ''' validate destination name '''
        regex = "^(?=.*[a-z])[a-zA-Z0-9]{8,15}$"
        return re.match(regex, destination)
  
    def valid_origin_name(self,origin):
        ''' validate origin name '''
        regex ="^(?=.*[a-z])[a-zA-Z0-9]{8,15}$"
        return re.match(regex, origin)
    
    def valid_name(self, username):
        """ Valid username """
        return re.match("^(?=.*[a-z])[a-zA-Z0-9]{8,15}$", username)

    def valid_password(self, password):
        """validate for password """
        return re.match("^(?=.*[a-z])[a-zA-Z0-9]{8,15}$",
                        password)

    def valid_email(self, email):
        """ validate for email """
        return re.match("^[^@]+@[^@]+\.[^@]+$", email)
