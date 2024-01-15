class Ejemploclase:
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad

    def __str__(self):
        return f"Nombre: {self.nombre} - Cantidad: {self.cantidad}"

ejemplo = {}
ejemplo['locura'] = []
ejemplo['locura'].append(Ejemploclase('hola', 1))
ejemplo['locura'].append(Ejemploclase('chau', 2))
ejemplo['locura'].append(Ejemploclase('hola2', 3))

#sum objects to get a total cantidad of 5
total = sum([x.cantidad for x in ejemplo['locura']])
print(total)
