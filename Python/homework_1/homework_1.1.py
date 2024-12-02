class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def makesound(self):
        print(f"{self.name} говорит: {self.sound}")


class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, "Meow")
        self.color = color

    def makesound(self):
        print(f"{self.name} ({self.color}) говорит: {self.sound}")


class Dog(Animal):
    def __init__(self, name, color):
        super().__init__(name, "Woof")
        self.color = color

    def makesound(self):
        print(f"{self.name} ({self.color}) говорит: {self.sound}")


cat = Cat("Гамлет", "серый")
dog = Dog("Марвел", "белый")

cat.makesound()
dog.makesound()
