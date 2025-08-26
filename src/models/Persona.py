import random
from .InventarioBien import InventarioBien

class Persona:
    def __init__(self, mercado):
        self.mercado = mercado  # Guardar referencia al mercado
        self.dinero = 0
        self.bienes = {}  # Bienes en posesión, formato: {'NombreBien': cantidad}
        self.demanda = []  # Bienes que se desean comprar
        self.habilidad_negociacion = random.uniform(0.75, 1.25)  # Habilidad de negociación aleatoria
        self.cartera_acciones = {}  # Cartera de acciones, formato: {'NombreEmpresa': cantidad_acciones}
        self.preferencias = {}  # Se inicializa en las subclases
        self.riesgoCompra = random.uniform(0, 1)  # Riesgo de compra aleatorio
        self.riesgoVenta = random.uniform(0, 1)  # Riesgo de venta aleatorio
        
    def decidir_compra(self, mercado, ciclo):
        """Método básico de decisión de compra - se sobrescribe en subclases"""
        # Implementación base: no tomar decisiones específicas, 
        # las subclases implementarán la lógica específica
        return []
        
    def comprar_bien(self, empresa, bien, cantidad, mercado, ciclo):
        """Método básico de compra - se sobrescribe en subclases"""
        return False
    
    def agregarBien(self, nombre, costo, mercado):
        if nombre not in self.bienes:
            self.bienes[nombre] = []
        self.bienes[nombre].append(InventarioBien(nombre, costo, mercado.bienes))

    def eliminarBien(self, nombre, id):
        if nombre in self.bienes:
            for bien in self.bienes[nombre]:
                if bien.id == id:
                    self.bienes[nombre].remove(bien)
                    break

    def actualizar_ingresos(self):
        """Método básico de actualización de ingresos"""
        # Implementación base: sin cambios en ingresos
        # Las subclases implementarán lógica específica (empleados, empresarios, etc.)
        return
    
    def getPreferencias(self):
        return self.preferencias
        
    def ciclo_persona(self, ciclo, mercado):
        """Método que debe ser implementado por las subclases"""
        raise NotImplementedError("Las subclases deben implementar ciclo_persona")