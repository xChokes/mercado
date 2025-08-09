"""Funciones y utilidades para pruebas de sistemas avanzados"""
import random
from src.models.Mercado import Mercado
from src.models.Bien import Bien
from src.models.Consumidor import Consumidor
from src.models.Empresa import Empresa
from src.models.EmpresaProductora import EmpresaProductora
from src.config.ConfigEconomica import ConfigEconomica


def crear_bienes_avanzados():
    """Crea un conjunto ampliado de bienes"""
    bienes = {}
    # Bienes básicos
    for nombre in ["Arroz", "Papa", "Pan", "Leche", "Sal", "Aceite", "Azucar"]:
        bienes[nombre] = Bien(nombre, 'alimentos_basicos')
    # Bienes de lujo
    for nombre in ["Carne", "Pollo", "Huevos", "Cafe", "Chocolate"]:
        bienes[nombre] = Bien(nombre, 'alimentos_lujo')
    # Servicios
    for nombre in ["Electricidad", "Agua", "Internet", "Transporte"]:
        bienes[nombre] = Bien(nombre, 'servicios')
    # Bienes duraderos
    for nombre in ["Telefono", "Computadora", "Refrigerador"]:
        bienes[nombre] = Bien(nombre, 'bienes_duraderos')
    return bienes


def configurar_economia_avanzada(mercado):
    """Configura empresas y consumidores diversificados"""
    empresas = []
    # Algunas empresas productoras
    for i in range(2):
        e = EmpresaProductora(f"AgroEmpresa{i+1}", mercado)
        mercado.agregar_persona(e)
        empresas.append(e)
    # Empresas de servicios
    for i in range(2):
        e = Empresa.crear_con_acciones(
            nombre=f"ServiciosEmpresa{i+1}", mercado=mercado, cantidad_acciones=1000, bienes={})
        mercado.agregar_persona(e)
        empresas.append(e)
    # Consumidores
    for i in range(20):
        c = Consumidor(f"Consumidor{i+1}", mercado)
        mercado.agregar_persona(c)
        if c.empleado and empresas:
            empleador = random.choice(empresas)
            if empleador.contratar(c):
                c.empleador = empleador


__all__ = [
    'Mercado', 'Bien', 'Consumidor', 'Empresa', 'EmpresaProductora', 'ConfigEconomica',
    'crear_bienes_avanzados', 'configurar_economia_avanzada'
]
