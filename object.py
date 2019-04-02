# classe que define um objeto basico do universo de representacao

class Object:

    # string name_, type_;

    # construtor

    def __init__(self, name, type):
        self.name_ = name
        self.type_ = type

    # retorna o nome do objeto
    def get_name(self):
        return self.name_

    # retorna o tipo do objeto
    def get_type(self):
        return self.type_

    # altera o nome do objeto
    def set_name(self, name):
        self.name_ = name


# end of class Object
