class Bien:
    def __init__(self, nombre, elasticidad_precio, elasticidad_ingreso):
        self.nombre = nombre
        self.elasticidad_precio = elasticidad_precio
        self.elasticidad_ingreso = elasticidad_ingreso
    
    def __str__(self):
        return f"Nombre: {self.nombre} - Elasticidad precio: {self.elasticidad_precio} - Elasticidad ingreso: {self.elasticidad_ingreso}"