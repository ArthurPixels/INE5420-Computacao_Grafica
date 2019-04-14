# classe que define um objeto basico do universo de representacao

from abc import abstractmethod


class Object:

    # int id;
    # string name_, type_;

    # construtor
    def __init__(self, id, name, type):
        self.id_ = id
        self.name_ = name
        self.type_ = type

    # metodo abstrato que define a maneira como o objeto eh desenhado na tela
    @abstractmethod
    def draw(self, transform, da_width, da_height, cairo):
        pass

    @abstractmethod
    def update_scn(self, transform):
        pass

# end of class Object
