from Bien import Bien
class Accion(Bien):
    def __init__(self, nombre, elasticidad_precio, elasticidad_ingreso, empresa, nombreAccion):
        super().__init__(nombre, elasticidad_precio, elasticidad_ingreso)
        self.id = nombreAccion
        self.empresa = empresa

    def __str__(self):
        return f"Accion de {self.empresa.nombre}"