"""
Módulo de Vectorización Optimizada para Simulador de Mercado
============================================================

Contiene funciones vectorizadas usando NumPy y pandas para mejorar
el rendimiento de las operaciones más costosas del simulador.

Objetivo: Reducir tiempo de ejecución en 20-40% mediante:
- Vectorización de cálculos de agregados (PIB, índices, etc.)
- Optimización de loops sobre agentes
- Paralelización opcional de operaciones independientes
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
import multiprocessing as mp
from functools import partial
import warnings

# Suprimir warnings de NumPy para operaciones vectorizadas
warnings.filterwarnings('ignore', category=RuntimeWarning)


class VectorizadorEconomico:
    """Clase principal para operaciones vectorizadas de economía"""
    
    def __init__(self, usar_paralelismo: bool = False, num_workers: Optional[int] = None):
        """
        Inicializa el vectorizador económico
        
        Args:
            usar_paralelismo: Si usar procesamiento paralelo para operaciones costosas
            num_workers: Número de workers para paralelismo (None = auto)
        """
        self.usar_paralelismo = usar_paralelismo
        self.num_workers = num_workers or max(1, mp.cpu_count() - 1)
        
        # Cache para cálculos repetitivos
        self._cache_precios = {}
        self._cache_indices = {}
        
    def calcular_pib_vectorizado(self, transacciones: List[Dict], empresas: List[Any],
                                gobierno: Any = None) -> float:
        """
        Cálculo vectorizado del PIB usando pandas para mayor velocidad
        
        Args:
            transacciones: Lista de transacciones del ciclo
            empresas: Lista de empresas
            gobierno: Instancia del gobierno (opcional)
            
        Returns:
            PIB calculado del ciclo
        """
        try:
            # 1. CONSUMO - Vectorizar suma de transacciones
            if transacciones:
                df_transacciones = pd.DataFrame(transacciones)
                if 'costo_total' in df_transacciones.columns:
                    pib_consumo = df_transacciones['costo_total'].sum()
                else:
                    pib_consumo = 0
            else:
                pib_consumo = 0
            
            # 2. INVERSIÓN - Vectorizar cálculos empresariales
            pib_inversion = self._calcular_inversion_vectorizada(empresas)
            
            # 3. GASTO GUBERNAMENTAL
            pib_gasto_gobierno = 0
            if gobierno:
                pib_gasto_gobierno = getattr(gobierno, 'gasto_ciclo_actual', 0)
                if pib_gasto_gobierno == 0:
                    pib_gasto_gobierno = getattr(gobierno, 'presupuesto', 0) * 0.1
            
            # 4. PIB total con multiplicador
            pib_base = pib_consumo + pib_inversion + pib_gasto_gobierno
            multiplicador = 1.8
            pib_total = pib_base * multiplicador
            
            # PIB mínimo por agente
            num_agentes = len(empresas)  # Aproximación rápida
            pib_minimo = num_agentes * 50
            
            return max(pib_total, pib_minimo)
            
        except Exception as e:
            # Fallback al cálculo tradicional en caso de error
            print(f"⚠️  Error en cálculo vectorizado PIB: {e}")
            return self._calcular_pib_fallback(transacciones, empresas, gobierno)
    
    def _calcular_inversion_vectorizada(self, empresas: List[Any]) -> float:
        """Cálculo vectorizado de inversión empresarial"""
        try:
            # Extraer datos relevantes de empresas en arrays
            dineros = []
            inventarios_valor = []
            
            for empresa in empresas:
                # Dinero empresarial
                dinero = getattr(empresa, 'dinero', 0)
                dineros.append(max(0, dinero))
                
                # Valor de inventario
                valor_inventario = 0
                if hasattr(empresa, 'bienes') and hasattr(empresa, 'precios'):
                    for bien, lista_bien in empresa.bienes.items():
                        precio = empresa.precios.get(bien, 10)
                        cantidad = len(lista_bien) if isinstance(lista_bien, list) else int(lista_bien or 0)
                        valor_inventario += cantidad * precio * 0.1
                
                inventarios_valor.append(valor_inventario)
            
            # Vectorizar cálculos
            if dineros:
                arr_dineros = np.array(dineros)
                arr_inventarios = np.array(inventarios_valor)
                
                # Inversión = 5% del dinero + valor de inventarios
                inversion_total = np.sum(arr_dineros * 0.05) + np.sum(arr_inventarios)
                return float(inversion_total)
            
            return 0.0
            
        except Exception as e:
            print(f"⚠️  Error en cálculo vectorizado inversión: {e}")
            return 0.0
    
    def calcular_indice_precios_vectorizado(self, empresas: List[Any]) -> float:
        """
        Cálculo vectorizado del índice de precios con ponderación optimizada
        
        Args:
            empresas: Lista de empresas
            
        Returns:
            Índice de precios calculado
        """
        try:
            # Extraer precios y pesos de todas las empresas
            precios_data = []
            
            for empresa in empresas:
                if hasattr(empresa, 'precios'):
                    for bien, precio in empresa.precios.items():
                        # Filtrar precios válidos
                        if 0 < precio <= 1000000:
                            # Determinar peso según categoría
                            peso = self._obtener_peso_bien(bien)
                            precios_data.append({'precio': precio, 'peso': peso, 'bien': bien})
            
            if not precios_data:
                return 100.0  # Índice base
            
            # Convertir a DataFrame para operaciones vectorizadas
            df = pd.DataFrame(precios_data)
            
            # Cálculo vectorizado del índice ponderado
            if df['peso'].sum() > 0:
                indice = (df['precio'] * df['peso']).sum() / df['peso'].sum()
                return float(indice)
            
            return 100.0
            
        except Exception as e:
            print(f"⚠️  Error en cálculo vectorizado índice precios: {e}")
            return 100.0
    
    def _obtener_peso_bien(self, nombre_bien: str) -> float:
        """Obtiene el peso de un bien para el índice de precios"""
        # Cache de pesos para evitar recálculos
        if nombre_bien not in self._cache_precios:
            try:
                from src.config.ConfigEconomica import ConfigEconomica
                categorias_map = getattr(ConfigEconomica, 'CATEGORIAS_BIENES_MAP', {})
                categoria = categorias_map.get(nombre_bien, 'servicios')
                
                if categoria == 'alimentos_basicos':
                    peso = 3.0
                elif categoria == 'alimentos_lujo':
                    peso = 1.5
                else:
                    peso = 1.0
                
                self._cache_precios[nombre_bien] = peso
            except:
                self._cache_precios[nombre_bien] = 1.0
        
        return self._cache_precios[nombre_bien]
    
    def procesar_agentes_paralelo(self, agentes: List[Any], funcion_ciclo,
                                 ciclo: int, mercado: Any) -> List[Any]:
        """
        Procesamiento paralelo de ciclos de agentes independientes
        
        Args:
            agentes: Lista de agentes (consumidores/empresas)
            funcion_ciclo: Función de ciclo a aplicar
            ciclo: Número de ciclo actual
            mercado: Instancia del mercado
            
        Returns:
            Lista de resultados del procesamiento
        """
        if not self.usar_paralelismo or len(agentes) < 50:
            # Para pocos agentes, el paralelismo no vale la pena
            return self._procesar_agentes_secuencial(agentes, funcion_ciclo, ciclo, mercado)
        
        try:
            # Dividir agentes en chunks para procesamiento paralelo
            chunk_size = max(1, len(agentes) // self.num_workers)
            chunks = [agentes[i:i + chunk_size] for i in range(0, len(agentes), chunk_size)]
            
            # Usar multiprocessing para procesar chunks
            with mp.Pool(processes=self.num_workers) as pool:
                func_parcial = partial(self._procesar_chunk_agentes, 
                                     funcion_ciclo=funcion_ciclo, 
                                     ciclo=ciclo, 
                                     mercado=mercado)
                resultados = pool.map(func_parcial, chunks)
            
            # Combinar resultados
            resultado_final = []
            for chunk_resultado in resultados:
                resultado_final.extend(chunk_resultado)
            
            return resultado_final
            
        except Exception as e:
            print(f"⚠️  Error en procesamiento paralelo: {e}")
            # Fallback a procesamiento secuencial
            return self._procesar_agentes_secuencial(agentes, funcion_ciclo, ciclo, mercado)
    
    def _procesar_agentes_secuencial(self, agentes: List[Any], funcion_ciclo,
                                   ciclo: int, mercado: Any) -> List[Any]:
        """Procesamiento secuencial tradicional (fallback)"""
        resultados = []
        for agente in agentes:
            try:
                resultado = funcion_ciclo(agente, ciclo, mercado)
                resultados.append(resultado)
            except Exception as e:
                print(f"Error procesando agente {getattr(agente, 'nombre', 'Desconocido')}: {e}")
                resultados.append(None)
        return resultados
    
    def _procesar_chunk_agentes(self, chunk_agentes: List[Any], funcion_ciclo, 
                              ciclo: int, mercado: Any) -> List[Any]:
        """Procesa un chunk de agentes en un worker"""
        resultados = []
        for agente in chunk_agentes:
            try:
                # Nota: Esto requiere que funcion_ciclo sea serializable
                # En la práctica, usaremos métodos estáticos o funciones globales
                resultado = agente.ciclo_persona(ciclo, mercado)
                resultados.append(resultado)
            except Exception as e:
                print(f"Error en chunk procesando {getattr(agente, 'nombre', 'Desconocido')}: {e}")
                resultados.append(None)
        return resultados
    
    def calcular_estadisticas_vectorizadas(self, mercado: Any) -> Dict[str, float]:
        """
        Cálculo vectorizado de estadísticas del mercado
        
        Args:
            mercado: Instancia del mercado
            
        Returns:
            Diccionario con estadísticas calculadas
        """
        stats = {}
        
        try:
            # PIB usando vectorización
            transacciones = getattr(mercado, 'transacciones_ciclo_actual', [])
            empresas = mercado.getEmpresas()
            gobierno = getattr(mercado, 'gobierno', None)
            
            stats['pib'] = self.calcular_pib_vectorizado(transacciones, empresas, gobierno)
            
            # Índice de precios vectorizado
            stats['indice_precios'] = self.calcular_indice_precios_vectorizado(empresas)
            
            # Estadísticas rápidas de agentes
            consumidores = mercado.getConsumidores()
            stats['num_consumidores'] = len(consumidores)
            stats['num_empresas'] = len(empresas)
            
            # Estadísticas de empleo vectorizadas
            if consumidores:
                empleados = np.array([getattr(c, 'empleado', False) for c in consumidores])
                stats['tasa_empleo'] = float(np.mean(empleados))
                stats['desempleo'] = 1.0 - stats['tasa_empleo']
            else:
                stats['tasa_empleo'] = 0.0
                stats['desempleo'] = 1.0
            
            # Estadísticas de dinero vectorizadas
            if empresas:
                dineros_empresas = np.array([getattr(e, 'dinero', 0) for e in empresas])
                stats['dinero_empresas_total'] = float(np.sum(dineros_empresas))
                stats['dinero_empresas_promedio'] = float(np.mean(dineros_empresas))
            
            if consumidores:
                dineros_consumidores = np.array([getattr(c, 'dinero', 0) for c in consumidores])
                stats['dinero_consumidores_total'] = float(np.sum(dineros_consumidores))
                stats['dinero_consumidores_promedio'] = float(np.mean(dineros_consumidores))
            
        except Exception as e:
            print(f"⚠️  Error en estadísticas vectorizadas: {e}")
            # Estadísticas mínimas de fallback
            stats = {
                'pib': 0.0,
                'indice_precios': 100.0,
                'num_consumidores': 0,
                'num_empresas': 0,
                'tasa_empleo': 0.0,
                'desempleo': 1.0
            }
        
        return stats
    
    def optimizar_matching_orderbook(self, ordenes_compra: List[Dict],
                                   ordenes_venta: List[Dict]) -> List[Dict]:
        """
        Matching optimizado del order book usando pandas
        
        Args:
            ordenes_compra: Lista de órdenes de compra
            ordenes_venta: Lista de órdenes de venta
            
        Returns:
            Lista de trades ejecutados
        """
        try:
            if not ordenes_compra or not ordenes_venta:
                return []
            
            # Convertir a DataFrames para operaciones vectorizadas
            df_compra = pd.DataFrame(ordenes_compra)
            df_venta = pd.DataFrame(ordenes_venta)
            
            # Ordenar por precio (compra descendente, venta ascendente)
            df_compra = df_compra.sort_values('precio', ascending=False)
            df_venta = df_venta.sort_values('precio', ascending=True)
            
            trades = []
            
            # Matching vectorizado básico
            for _, orden_compra in df_compra.iterrows():
                ordenes_compatibles = df_venta[
                    (df_venta['precio'] <= orden_compra['precio']) &
                    (df_venta['bien'] == orden_compra['bien']) &
                    (df_venta['cantidad'] > 0)
                ]
                
                if not ordenes_compatibles.empty:
                    # Tomar la mejor orden de venta
                    mejor_venta = ordenes_compatibles.iloc[0]
                    
                    # Ejecutar trade
                    cantidad_trade = min(orden_compra['cantidad'], mejor_venta['cantidad'])
                    precio_trade = mejor_venta['precio']  # Precio del vendedor
                    
                    if cantidad_trade > 0:
                        trade = {
                            'comprador': orden_compra['agente'],
                            'vendedor': mejor_venta['agente'],
                            'bien': orden_compra['bien'],
                            'cantidad': cantidad_trade,
                            'precio': precio_trade,
                            'valor_total': cantidad_trade * precio_trade
                        }
                        trades.append(trade)
                        
                        # Actualizar cantidades restantes
                        df_compra.loc[df_compra.index == orden_compra.name, 'cantidad'] -= cantidad_trade
                        df_venta.loc[df_venta.index == mejor_venta.name, 'cantidad'] -= cantidad_trade
            
            return trades
            
        except Exception as e:
            print(f"⚠️  Error en matching vectorizado: {e}")
            return []
    
    def _calcular_pib_fallback(self, transacciones: List[Dict], empresas: List[Any],
                             gobierno: Any) -> float:
        """Cálculo de PIB tradicional como fallback"""
        pib_consumo = sum([t.get('costo_total', 0) for t in transacciones])
        
        pib_inversion = 0
        for empresa in empresas:
            if hasattr(empresa, 'dinero') and empresa.dinero > 0:
                pib_inversion += empresa.dinero * 0.05
            
            if hasattr(empresa, 'bienes') and hasattr(empresa, 'precios'):
                for bien, lista_bien in empresa.bienes.items():
                    precio = empresa.precios.get(bien, 10)
                    cantidad = len(lista_bien) if isinstance(lista_bien, list) else int(lista_bien or 0)
                    pib_inversion += cantidad * precio * 0.1
        
        pib_gasto_gobierno = 0
        if gobierno:
            pib_gasto_gobierno = getattr(gobierno, 'gasto_ciclo_actual', 0)
            if pib_gasto_gobierno == 0:
                pib_gasto_gobierno = getattr(gobierno, 'presupuesto', 0) * 0.1
        
        pib_base = pib_consumo + pib_inversion + pib_gasto_gobierno
        return pib_base * 1.8
    
    def limpiar_cache(self):
        """Limpia los caches internos para liberar memoria"""
        self._cache_precios.clear()
        self._cache_indices.clear()


# Instancia global del vectorizador (singleton)
_vectorizador_global = None

def get_vectorizador(usar_paralelismo: bool = False, num_workers: Optional[int] = None) -> VectorizadorEconomico:
    """
    Obtiene la instancia global del vectorizador económico
    
    Args:
        usar_paralelismo: Si usar procesamiento paralelo
        num_workers: Número de workers para paralelismo
        
    Returns:
        Instancia del vectorizador
    """
    global _vectorizador_global
    if _vectorizador_global is None:
        _vectorizador_global = VectorizadorEconomico(usar_paralelismo, num_workers)
    return _vectorizador_global


def reiniciar_vectorizador():
    """Reinicia el vectorizador global (útil para tests)"""
    global _vectorizador_global
    _vectorizador_global = None


# Funciones de conveniencia para usar en el código existente
def calcular_pib_optimizado(mercado: Any) -> float:
    """Función de conveniencia para cálculo optimizado de PIB"""
    vectorizador = get_vectorizador()
    transacciones = getattr(mercado, 'transacciones_ciclo_actual', [])
    empresas = mercado.getEmpresas()
    gobierno = getattr(mercado, 'gobierno', None)
    return vectorizador.calcular_pib_vectorizado(transacciones, empresas, gobierno)


def calcular_indice_precios_optimizado(mercado: Any) -> float:
    """Función de conveniencia para cálculo optimizado de índice de precios"""
    vectorizador = get_vectorizador()
    empresas = mercado.getEmpresas()
    return vectorizador.calcular_indice_precios_vectorizado(empresas)


def obtener_estadisticas_optimizadas(mercado: Any) -> Dict[str, float]:
    """Función de conveniencia para estadísticas optimizadas"""
    vectorizador = get_vectorizador()
    return vectorizador.calcular_estadisticas_vectorizadas(mercado)