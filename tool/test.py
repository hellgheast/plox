class interface:
    def func():
        raise NotImplementedError("interface function to be implemented")


class test(interface):
    def func(self):
        print("test")

    
tes = test()
tes.func()