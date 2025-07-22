class Rectangulo:
    def __init__(self,base,altura):
        self.__base = base
        self.__altura = altura
    def calcular_area(self):
        return self.__base *  self.__altura
    
    def get_base(self):
        return self.__base
    def get_altura (self):
        return  self.__altura
    
    def set_base(self,nueva_base):
        self.__base = nueva_base

    def set_altura(self,nueva_altura):
        self.__altura = nueva_altura
    
#uso de la calse Rectangulo
rect = Rectangulo(5,3)
print("area del rectángulo: ",rect.calcular_area())

#actualizar base
rect.set_base(8)
print("nueva area: ", rect.calcular_area())

#actualizar altura
rect.set_altura(5)
print("nueva area: ",rect.calcular_area() )