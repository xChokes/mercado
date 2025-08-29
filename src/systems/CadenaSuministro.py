"""
Gestor de Cadena de Suministro (B2B) entre empresas
===================================================

Este módulo implementa una capa simple de cadena de suministro inter-empresas:
- Define insumos requeridos por empresa según sector/bienes
- Detecta faltantes y genera pedidos B2B a proveedores con stock
- Liquida transferencias de dinero e inventario entre empresas
- Mantiene métricas básicas de desempeño de la cadena

Está diseñado para funcionar sin dependencias externas, usando el estado de
`Mercado`, `Empresa` y el bus de eventos disponible.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional


INSUMOS_DEFAULT = {
    # Reglas simples: todas las empresas usan un poco de MP y Energía
    'Materias_Primas': {'consumo_por_unidad': 1},
    'Energia': {'consumo_por_unidad': 0.2},  # 1 unidad de energía por 5 output
}


class GestorCadenaSuministro:
    """Coordina compras B2B de insumos y abastecimiento entre empresas."""

    def __init__(self, mercado):
        self.mercado = mercado
        self.pedidos_realizados = 0
        self.unidades_abastecidas = 0
        self.valor_transado = 0.0

        # Parámetros básicos de operación
        self.nivel_objetivo_insumo = 30  # objetivo simple por insumo
        self.umbral_reabastecimiento = 10
        self.max_compra_por_ciclo = 15

    # --- Inicialización ---
    def inicializar_red(self):
        """Prepara estructuras en empresas para operar con insumos."""
        for empresa in self.mercado.getEmpresas():
            # Inventario de insumos como contadores enteros
            if not hasattr(empresa, 'inventario_insumos') or not isinstance(getattr(empresa, 'inventario_insumos'), dict):
                empresa.inventario_insumos: Dict[str, int] = {}

            # Declaración de insumos requeridos (simple y segura por defecto)
            if not hasattr(empresa, 'insumos_requeridos') or not isinstance(getattr(empresa, 'insumos_requeridos'), dict):
                empresa.insumos_requeridos: Dict[str, Dict[str, float]] = {}
                # Todas las empresas usan MP y Energía; productoras pueden ampliarlo dinámicamente
                for ins, meta in INSUMOS_DEFAULT.items():
                    if ins in self.mercado.bienes:
                        empresa.insumos_requeridos[ins] = dict(meta)

                # Empresas con foco en bienes industriales usan Acero/Cemento si están disponibles
                for candidato in ['Acero', 'Cemento']:
                    if candidato in self.mercado.bienes and random.random() < 0.3:
                        empresa.insumos_requeridos[candidato] = {'consumo_por_unidad': 0.3}

            # Asegurar contadores iniciales
            for ins in empresa.insumos_requeridos.keys():
                empresa.inventario_insumos.setdefault(ins, 0)

    # --- Ciclo ---
    def ciclo_cadena(self):
        """Ejecuta un ciclo de abastecimiento B2B simple."""
        if not getattr(self, '_inicializado', False):
            try:
                self.inicializar_red()
            finally:
                self._inicializado = True

        for empresa in self.mercado.getEmpresas():
            self._procesar_reabastecimiento_empresa(empresa)

    # --- Lógica interna ---
    def _procesar_reabastecimiento_empresa(self, empresa):
        if not getattr(empresa, 'insumos_requeridos', None):
            return

        for insumo in list(empresa.insumos_requeridos.keys()):
            nivel = int(empresa.inventario_insumos.get(insumo, 0))
            if nivel >= self.umbral_reabastecimiento:
                continue

            faltante = self.nivel_objetivo_insumo - nivel
            cantidad_a_comprar = max(0, min(self.max_compra_por_ciclo, faltante))
            if cantidad_a_comprar <= 0:
                continue

            proveedor, precio = self._buscar_proveedor_con_stock(insumo)
            if not proveedor or precio <= 0:
                continue

            costo_total = cantidad_a_comprar * precio
            if getattr(empresa, 'dinero', 0) < costo_total:
                # Ajustar a lo que pueda pagar
                cantidad_a_comprar = int(empresa.dinero // max(1, precio))
                if cantidad_a_comprar <= 0:
                    continue
                costo_total = cantidad_a_comprar * precio

            # Realizar transferencia B2B (dinero e inventario)
            unidades_transferidas = self._transferir_stock(proveedor, empresa, insumo, cantidad_a_comprar, precio)
            if unidades_transferidas <= 0:
                continue

            # Registrar métricas y evento
            empresa.inventario_insumos[insumo] = empresa.inventario_insumos.get(insumo, 0) + unidades_transferidas
            self.pedidos_realizados += 1
            self.unidades_abastecidas += unidades_transferidas
            self.valor_transado += unidades_transferidas * precio

            # Registrar en sistema de transacciones del mercado (B2B)
            try:
                self.mercado.registrar_transaccion(empresa, insumo, unidades_transferidas, unidades_transferidas * precio, self.mercado.ciclo_actual)
            except Exception:
                pass

    def _buscar_proveedor_con_stock(self, bien: str):
        """Busca proveedor con stock del bien y retorna (empresa, precio)."""
        candidatos = []
        for e in self.mercado.getEmpresas():
            stock = 0
            if hasattr(e, 'bienes') and bien in e.bienes:
                inv = e.bienes[bien]
                stock = len(inv) if isinstance(inv, list) else int(inv or 0)
            if stock > 0:
                precio = float(getattr(e, 'precios', {}).get(bien, 10))
                if precio > 0:
                    candidatos.append((e, precio, stock))

        if not candidatos:
            return None, 0.0

        # Proveedor con mejor precio
        proveedor, precio, _ = min(candidatos, key=lambda t: t[1])
        return proveedor, precio

    def _transferir_stock(self, proveedor, comprador, bien: str, qty: int, precio_unit: float) -> int:
        inv = proveedor.bienes.get(bien, [])
        stock = len(inv) if isinstance(inv, list) else int(inv or 0)
        unidades = max(0, min(qty, stock))
        if unidades <= 0:
            return 0

        costo = unidades * precio_unit
        if getattr(comprador, 'dinero', 0) < costo:
            return 0

        # Transferir dinero
        comprador.dinero -= costo
        proveedor.dinero += costo

        # Mover inventario (listas de InventarioBien)
        if isinstance(inv, list):
            for _ in range(unidades):
                if inv:
                    inv.pop(0)
        else:
            proveedor.bienes[bien] = max(0, int(proveedor.bienes.get(bien, 0)) - unidades)

        # Evento
        try:
            self.mercado.event_bus.publish('b2b', tipo='insumos', bien=bien, qty=unidades,
                                           proveedor=proveedor.nombre, comprador=comprador.nombre,
                                           precio=precio_unit, ciclo=self.mercado.ciclo_actual)
        except Exception:
            pass

        return unidades

    # --- Stats ---
    def obtener_estadisticas(self) -> Dict[str, float]:
        return {
            'pedidos_realizados': self.pedidos_realizados,
            'unidades_abastecidas': self.unidades_abastecidas,
            'valor_transado': self.valor_transado,
        }
