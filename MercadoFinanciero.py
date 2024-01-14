class MercadoFinanciero:
    def __init__(self):
        self.acciones = {}  # formato: {'NombreEmpresa': (cantidad_acciones, precio_accion)}

    def actualizar_precio_accion(self, nombre_empresa, nuevo_precio):
        if nombre_empresa in self.acciones:
            cantidad_acciones = self.acciones[nombre_empresa][0]
            self.acciones[nombre_empresa] = (cantidad_acciones, nuevo_precio)

    def consumidores_con_acciones(self, nombre_empresa):
        return [c for c in self.consumidores if c.cartera_acciones.get(nombre_empresa, 0) > 0]
    
    def emitir_acciones(self, nombre_empresa, cantidad):
        if nombre_empresa in self.acciones:
            cantidad_acciones, precio_actual = self.acciones[nombre_empresa]
            self.acciones[nombre_empresa] = (cantidad_acciones + cantidad, precio_actual)
        else:
            self.acciones[nombre_empresa] = (cantidad, 100)

    def empresas_con_acciones(self, nombre_empresa):
        return [e for e in self.empresas if e.nombre == nombre_empresa]
    