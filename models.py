import json

class User:
    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name
        super().__init__()

    def convert_to_json(self):
        return json.dumps(self.__dict__)