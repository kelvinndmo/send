import re

class Validators:
    def valid_destination_name(self,destination):
        ''' validate destination name '''
        regex = "^[a-zA-Z0-9_ ]{1,}$"
        return re.match(regex, destination)


    def valid_origin_name(self,origin):
        ''' validate origin name '''
        regex = "^[a-zA-Z0-9_ ]{2,}$"
        return re.match(regex, origin)
    
    def valid_name(self, username):
        """ Valid username """
        return re.match("^[a-zA-Z0-9]{6,}$", username)

    def valid_password(self, password):
        """validate for password """
        # positive look ahead
        return re.match("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[a-zA-Z0-9]{8,15}$",
                        password)

    def valid_email(self, email):
        """ validate for email """
        return re.match("^[^@]+@[^@]+\.[^@]+$", email)

    def valid_inputs(self, string_inputs):
        """ validate for inputs """
        return re.match("^[a-zA-Z0-9-\._@ ]+$", string_inputs)
        # return re.match("^[a-zA-Z0-9-\._@ ]+$", string_inputs)

    def valid_is_admin(self, is_admin):
        """ validate is_admin """
        return re.match("^[0-1]{,1}$", is_admin)


    # def valid_person_name(customer_name):
    #     '''validate person's name'''
    #     regex = "^[a-zA-Z ]{4,}$"
    #     return re.match(regex, customer_name)

    # def valid_destination(destination):
    #     '''validate destination name'''
    #     regex = "^[a-zA-Z 0-9]{3,}$"
    #     return re.match(regex, destination)
