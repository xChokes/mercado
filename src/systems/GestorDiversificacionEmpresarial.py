"""
Sistema Mejorado de Diversificación Empresarial
===============================================

Previene la monopolización y mantiene competencia saludable
"""

import random
import logging
from typing import Dict, List, Any, Optional
import numpy as np

class GestorDiversificacionEmpresarial:
    """Sistema que mantiene diversidad empresarial y previene monopolización"""
    
    def __init__(self, mercado):
        self.mercado = mercado
        self.logger = logging.getLogger(__name__)
        
        # Configuración de diversificación
        self.min_empresas_objetivo = 3  # Mínimo empresas activas
        self.max_empresas_objetivo = 8  # Máximo para rendimiento
        self.concentracion_maxima = 0.6  # Máxima cuota de mercado individual
        
        # Métricas de diversificación
        self.empresas_creadas = 0
        self.split_ups_realizados = 0
        self.incentivos_competencia = 0
        
    def evaluar_y_mantener_competencia(self, ciclo: int):
        """Evalúa y mantiene competencia saludable"""
        try:
            # 1. Verificar número de empresas
            self._verificar_numero_empresas(ciclo)
            
            # 2. Verificar concentración de mercado
            self._verificar_concentracion_mercado(ciclo)
            
            # 3. Incentivar innovación competitiva
            self._incentivar_innovacion_competitiva(ciclo)
            
            # 4. Crear niches de mercado
            self._crear_nichos_especializados(ciclo)
            
        except Exception as e:
            self.logger.error(f"Error manteniendo competencia: {e}")
    
    def _verificar_numero_empresas(self, ciclo: int):
        """Verifica que haya suficientes empresas activas"""
        empresas_activas = [e for e in self.mercado.getEmpresas() if not getattr(e, 'en_quiebra', False)]
        num_empresas = len(empresas_activas)
        
        if num_empresas < self.min_empresas_objetivo:
            empresas_a_crear = self.min_empresas_objetivo - num_empresas
            
            for i in range(empresas_a_crear):
                self._crear_empresa_competidora(ciclo, tipo="complementaria")
                
            self.logger.info(f"Creadas {empresas_a_crear} empresas para mantener competencia mínima")
    
    def _verificar_concentracion_mercado(self, ciclo: int):
        """Verifica que no haya monopolización excesiva"""
        empresas = [e for e in self.mercado.getEmpresas() if not getattr(e, 'en_quiebra', False)]
        
        if len(empresas) == 0:
            return
            
        # Calcular cuotas de mercado por facturación
        facturaciones = []
        for empresa in empresas:
            facturacion = getattr(empresa, 'facturacion_ciclo', empresa.dinero)
            facturaciones.append(max(1, facturacion))
        
        total_facturacion = sum(facturaciones)
        cuotas = [f / total_facturacion for f in facturaciones]
        
        # Verificar si alguna empresa tiene demasiada concentración
        for i, cuota in enumerate(cuotas):
            if cuota > self.concentracion_maxima:
                self.logger.warning(f"Empresa {empresas[i].nombre} tiene {cuota:.1%} del mercado")
                self._aplicar_medidas_antimonopolio(empresas[i], cuota, ciclo)
    
    def _aplicar_medidas_antimonopolio(self, empresa_dominante, cuota: float, ciclo: int):
        """Aplica medidas para reducir concentración excesiva"""
        
        # Medida 1: Crear competidor directo fuerte
        self._crear_empresa_competidora(ciclo, tipo="competidor_directo", empresa_objetivo=empresa_dominante)
        
        # Medida 2: Split-up si la empresa es demasiado grande
        if cuota > 0.8 and hasattr(empresa_dominante, 'dinero') and empresa_dominante.dinero > 500000:
            self._realizar_split_up_empresa(empresa_dominante, ciclo)
        
        # Medida 3: Incentivos a empresas menores
        self._incentivar_empresas_menores(ciclo)
        
        self.logger.info(f"Medidas antimonopolio aplicadas contra {empresa_dominante.nombre}")
    
    def _crear_empresa_competidora(self, ciclo: int, tipo: str = "general", empresa_objetivo=None):
        """Crea empresa competidora especializada"""
        from ..models.EmpresaProductora import EmpresaProductora
        
        # Generar nombre único y especializado
        if tipo == "competidor_directo" and empresa_objetivo:
            nombre_base = f"Rival_{empresa_objetivo.nombre}_C{ciclo}"
        elif tipo == "complementaria":
            nombre_base = f"Complementaria_{len(self.mercado.getEmpresas())}_C{ciclo}"
        elif tipo == "nicho":
            nombre_base = f"Especialista_{ciclo}"
        else:
            nombre_base = f"Competidor_{len(self.mercado.getEmpresas())}_C{ciclo}"
        
        nueva_empresa = EmpresaProductora(nombre_base, self.mercado)
        
        # Capital inicial competitivo
        if tipo == "competidor_directo":
            # Competidor directo tiene capital sustancial
            nueva_empresa.dinero = random.uniform(200000, 400000)
        elif tipo == "nicho":
            # Empresa nicho, capital moderado pero especializada
            nueva_empresa.dinero = random.uniform(80000, 150000)
        else:
            # Empresa complementaria, capital normal
            nueva_empresa.dinero = random.uniform(120000, 250000)
        
        # Especialización por tipo
        self._especializar_empresa(nueva_empresa, tipo, empresa_objetivo)
        
        # Marcar características especiales
        nueva_empresa.es_empresa_diversificacion = True
        nueva_empresa.tipo_diversificacion = tipo
        nueva_empresa.ciclo_entrada = ciclo
        
        self.mercado.personas.append(nueva_empresa)
        self.empresas_creadas += 1
        
        self.logger.info(f"Empresa competidora creada: {nombre_base} ({tipo}) con ${nueva_empresa.dinero:.0f}")
    
    def _especializar_empresa(self, empresa, tipo: str, empresa_objetivo=None):
        """Especializa la empresa según su tipo"""
        
        if tipo == "competidor_directo" and empresa_objetivo:
            # Copiar y mejorar la estrategia de la empresa objetivo
            if hasattr(empresa_objetivo, 'bienes'):
                for bien in list(empresa_objetivo.bienes.keys())[:3]:  # Top 3 productos
                    if bien not in empresa.bienes:
                        empresa.bienes[bien] = []
                    
                    # Precio más competitivo
                    precio_objetivo = empresa_objetivo.precios.get(bien, 50)
                    empresa.precios[bien] = precio_objetivo * 0.9  # 10% más barato
                    
                    # Costo inicial optimizado
                    costo_objetivo = empresa_objetivo.costos_unitarios.get(bien, precio_objetivo * 0.6)
                    empresa.costos_unitarios[bien] = costo_objetivo * 0.85  # Más eficiente
                    
                    # Capacidad competitiva
                    if hasattr(empresa, 'capacidad_produccion'):
                        capacidad_objetivo = getattr(empresa_objetivo, 'capacidad_produccion', {}).get(bien, 10)
                        empresa.capacidad_produccion[bien] = int(capacidad_objetivo * 0.8)  # 80% inicial
        
        elif tipo == "nicho":
            # Crear productos nicho únicos
            productos_nicho = [f"producto_nicho_{i}_{random.randint(1000,9999)}" for i in range(2)]
            
            for producto in productos_nicho:
                empresa.bienes[producto] = []
                # Productos nicho = mayor margen, menor volumen
                costo_base = random.uniform(25, 45)
                empresa.costos_unitarios[producto] = costo_base
                empresa.precios[producto] = costo_base * random.uniform(2.0, 3.5)  # Margen alto
                
                if hasattr(empresa, 'capacidad_produccion'):
                    empresa.capacidad_produccion[producto] = random.randint(3, 8)  # Capacidad pequeña
        
        elif tipo == "complementaria":
            # Productos complementarios a los existentes
            productos_existentes = set()
            for emp in self.mercado.getEmpresas():
                if hasattr(emp, 'bienes'):
                    productos_existentes.update(emp.bienes.keys())
            
            # Crear 2-3 productos complementarios nuevos
            for i in range(random.randint(2, 3)):
                producto_comp = f"complementario_{len(productos_existentes) + i}"
                empresa.bienes[producto_comp] = []
                
                costo_base = random.uniform(20, 40)
                empresa.costos_unitarios[producto_comp] = costo_base
                empresa.precios[producto_comp] = costo_base * random.uniform(1.4, 2.2)
                
                if hasattr(empresa, 'capacidad_produccion'):
                    empresa.capacidad_produccion[producto_comp] = random.randint(8, 15)
    
    def _realizar_split_up_empresa(self, empresa_grande, ciclo: int):
        """Realiza división de empresa muy grande"""
        if not hasattr(empresa_grande, 'bienes') or len(empresa_grande.bienes) < 4:
            return  # No vale la pena dividir
        
        # Crear empresa spin-off con parte de los productos
        productos_originales = list(empresa_grande.bienes.keys())
        productos_spinoff = productos_originales[len(productos_originales)//2:]
        
        nombre_spinoff = f"SpinOff_{empresa_grande.nombre}_C{ciclo}"
        empresa_spinoff = EmpresaProductora(nombre_spinoff, self.mercado)
        
        # Transferir capital (30% de la empresa madre)
        capital_transferido = empresa_grande.dinero * 0.3
        empresa_spinoff.dinero = capital_transferido
        empresa_grande.dinero -= capital_transferido
        
        # Transferir productos
        for producto in productos_spinoff:
            empresa_spinoff.bienes[producto] = empresa_grande.bienes.pop(producto)
            empresa_spinoff.precios[producto] = empresa_grande.precios.get(producto, 50)
            empresa_spinoff.costos_unitarios[producto] = empresa_grande.costos_unitarios.get(producto, 30)
            
            if hasattr(empresa_grande, 'capacidad_produccion') and producto in empresa_grande.capacidad_produccion:
                capacidad_original = empresa_grande.capacidad_produccion[producto]
                empresa_spinoff.capacidad_produccion[producto] = capacidad_original // 2
                empresa_grande.capacidad_produccion[producto] = capacidad_original - capacidad_original // 2
        
        # Marcar características
        empresa_spinoff.es_spinoff = True
        empresa_spinoff.empresa_madre = empresa_grande.nombre
        empresa_spinoff.ciclo_entrada = ciclo
        
        self.mercado.personas.append(empresa_spinoff)
        self.split_ups_realizados += 1
        
        self.logger.info(f"Split-up realizado: {nombre_spinoff} con ${capital_transferido:.0f} y {len(productos_spinoff)} productos")
    
    def _incentivar_empresas_menores(self, ciclo: int):
        """Proporciona incentivos a empresas más pequeñas"""
        empresas = [e for e in self.mercado.getEmpresas() if not getattr(e, 'en_quiebra', False)]
        
        if len(empresas) <= 1:
            return
        
        # Identificar empresas pequeñas (bottom 50%)
        empresas_por_size = sorted(empresas, key=lambda e: getattr(e, 'dinero', 0))
        empresas_pequenas = empresas_por_size[:len(empresas_por_size)//2]
        
        for empresa in empresas_pequenas:
            if random.random() < 0.3:  # 30% probabilidad de incentivo
                # Incentivo de capital
                incentivo = random.uniform(10000, 30000)
                empresa.dinero += incentivo
                empresa.incentivo_competencia = incentivo
                
                self.incentivos_competencia += 1
                
                # Mejora temporal de eficiencia
                if hasattr(empresa, 'costos_unitarios'):
                    for bien in empresa.costos_unitarios:
                        empresa.costos_unitarios[bien] *= 0.95  # 5% más eficiente por 1 ciclo
    
    def _incentivar_innovacion_competitiva(self, ciclo: int):
        """Incentiva innovación para aumentar competencia"""
        empresas = [e for e in self.mercado.getEmpresas() if not getattr(e, 'en_quiebra', False)]
        
        for empresa in empresas:
            if random.random() < 0.15:  # 15% probabilidad por empresa
                self._aplicar_innovacion_competitiva(empresa)
    
    def _aplicar_innovacion_competitiva(self, empresa):
        """Aplica innovación que mejora competitividad"""
        tipos_innovacion = [
            "eficiencia_costos",    # Reduce costos 5-15%
            "diferenciacion",       # Crea variante de producto
            "expansion_capacidad",  # Aumenta capacidad
            "optimizacion_precios"  # Mejora estrategia de precios
        ]
        
        tipo = random.choice(tipos_innovacion)
        
        if tipo == "eficiencia_costos":
            factor_mejora = random.uniform(0.85, 0.95)  # 5-15% reducción costos
            for bien in empresa.costos_unitarios:
                empresa.costos_unitarios[bien] *= factor_mejora
                
        elif tipo == "diferenciacion" and hasattr(empresa, 'bienes'):
            # Crear variante de producto existente
            productos_base = list(empresa.bienes.keys())
            if productos_base:
                producto_base = random.choice(productos_base)
                variante = f"{producto_base}_premium"
                
                if variante not in empresa.bienes:
                    empresa.bienes[variante] = []
                    # Variante premium: +30% costo, +60% precio
                    costo_base = empresa.costos_unitarios.get(producto_base, 30)
                    empresa.costos_unitarios[variante] = costo_base * 1.3
                    empresa.precios[variante] = empresa.precios.get(producto_base, 50) * 1.6
                    
                    if hasattr(empresa, 'capacidad_produccion'):
                        capacidad_base = empresa.capacidad_produccion.get(producto_base, 10)
                        empresa.capacidad_produccion[variante] = max(2, capacidad_base // 4)
        
        elif tipo == "expansion_capacidad" and hasattr(empresa, 'capacidad_produccion'):
            # Expandir capacidad en producto más rentable
            if empresa.capacidad_produccion:
                mejor_producto = max(empresa.capacidad_produccion.keys(), 
                                   key=lambda p: empresa.precios.get(p, 0) - empresa.costos_unitarios.get(p, 0))
                empresa.capacidad_produccion[mejor_producto] = int(empresa.capacidad_produccion[mejor_producto] * 1.5)
        
        elif tipo == "optimizacion_precios":
            # Optimizar precios competitivamente
            for bien in empresa.precios:
                costo = empresa.costos_unitarios.get(bien, empresa.precios[bien] * 0.6)
                margen_optimo = random.uniform(1.3, 1.8)  # Margen más competitivo
                empresa.precios[bien] = costo * margen_optimo
    
    def _crear_nichos_especializados(self, ciclo: int):
        """Crea empresas especializadas en nichos de mercado"""
        if ciclo % 20 == 0 and random.random() < 0.4:  # Cada 20 ciclos, 40% probabilidad
            self._crear_empresa_competidora(ciclo, tipo="nicho")
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Retorna estadísticas del sistema de diversificación"""
        empresas_activas = [e for e in self.mercado.getEmpresas() if not getattr(e, 'en_quiebra', False)]
        
        # Calcular índice Herfindahl-Hirschman (concentración)
        if empresas_activas:
            facturaciones = [max(1, getattr(e, 'dinero', 1)) for e in empresas_activas]
            total_facturacion = sum(facturaciones)
            cuotas_cuadradas = [(f/total_facturacion)**2 for f in facturaciones]
            hhi = sum(cuotas_cuadradas)
        else:
            hhi = 1.0
        
        return {
            'empresas_activas': len(empresas_activas),
            'empresas_creadas_total': self.empresas_creadas,
            'split_ups_realizados': self.split_ups_realizados,
            'incentivos_otorgados': self.incentivos_competencia,
            'hhi_concentracion': hhi,
            'mercado_competitivo': hhi < 0.25,  # HHI < 0.25 = mercado competitivo
            'mercado_concentrado': hhi > 0.6    # HHI > 0.6 = mercado concentrado
        }
