class A():
    a = []
    def b(self):
        self.a.append(1)
        print(self.a)

a = A()
a.b()
a.b()

b = A()
b.b()