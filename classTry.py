import json
class Animal(object):
#     __slots__ = ('name', 'age')
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        return "Animal object (name: %s)" % self.name
    __repr__ = __str__
    def getAge(self):
        return self.age
    def animal2dict(self):
        return {
            'name': self.name,
            'age': self.age
        }

class Cat(Animal):
    pass

class Tree(object):
    def __init__(self, name, age):
        self.__name = name
        self.__age = age
    def getAge(self):
        return self.__age

def age_twice(Animal):
    print(Animal.getAge())
    print(Animal.getAge())



if __name__ == '__main__':
    ginny = Cat('Ginny', '23')
    jinbao = Animal('Jinbao', '24')
    meer = Tree('Meer', '85')
    Animal.uni = 'Husky'
    print(jinbao.uni)
    print(Cat.uni)
    print(jinbao)
    print(jinbao.animal2dict())
    print(json.dumps(jinbao, default=Animal.animal2dict))
    print(json.dumps(jinbao.__dict__))



