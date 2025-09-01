"""
Sistema de Reporte de Rendimiento para Simulador de Mercado
===========================================================

Genera reportes detallados de rendimiento, métricas de optimización
y recomendaciones para mejorar la velocidad de simulación.
"""

import json
import time
import os
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class ReporterRendimiento:
    """Clase para generar reportes completos de rendimiento"""
    
    def __init__(self, output_dir: str = "results/perf"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Métricas de seguimiento
        self.metricas_ciclo = []
        self.tiempos_secciones = {}
        self.contadores_operaciones = {}
        
    def iniciar_seguimiento(self, nombre_simulacion: str = "default"):
        """Inicia el seguimiento de rendimiento para una simulación"""
        self.nombre_simulacion = nombre_simulacion
        self.tiempo_inicio = time.time()
        self.metricas_ciclo = []
        self.tiempos_secciones = {}
        self.contadores_operaciones = {}
        
        print(f"📊 Iniciando seguimiento de rendimiento: {nombre_simulacion}")
    
    def registrar_tiempo_ciclo(self, ciclo: int, tiempo_ciclo: float, 
                              metricas_adicionales: Optional[Dict] = None):
        """Registra métricas de tiempo para un ciclo específico"""
        metrica = {
            'ciclo': ciclo,
            'tiempo': tiempo_ciclo,
            'timestamp': time.time()
        }
        
        if metricas_adicionales:
            metrica.update(metricas_adicionales)
        
        self.metricas_ciclo.append(metrica)
    
    def registrar_tiempo_seccion(self, seccion: str, tiempo: float):
        """Registra tiempo de una sección específica del código"""
        if seccion not in self.tiempos_secciones:
            self.tiempos_secciones[seccion] = []
        self.tiempos_secciones[seccion].append(tiempo)
    
    def incrementar_contador(self, operacion: str, cantidad: int = 1):
        """Incrementa contador de operaciones específicas"""
        if operacion not in self.contadores_operaciones:
            self.contadores_operaciones[operacion] = 0
        self.contadores_operaciones[operacion] += cantidad
    
    def finalizar_seguimiento(self) -> Dict[str, Any]:
        """Finaliza seguimiento y retorna resumen de métricas"""
        tiempo_total = time.time() - self.tiempo_inicio
        
        resumen = {
            'nombre_simulacion': self.nombre_simulacion,
            'timestamp': self.timestamp,
            'tiempo_total': tiempo_total,
            'num_ciclos': len(self.metricas_ciclo),
            'tiempo_promedio_ciclo': np.mean([m['tiempo'] for m in self.metricas_ciclo]) if self.metricas_ciclo else 0,
            'ciclos_por_segundo': len(self.metricas_ciclo) / tiempo_total if tiempo_total > 0 else 0,
            'metricas_ciclo': self.metricas_ciclo,
            'tiempos_secciones': self.tiempos_secciones,
            'contadores_operaciones': self.contadores_operaciones
        }
        
        print(f"📊 Seguimiento finalizado: {tiempo_total:.2f}s total, {resumen['ciclos_por_segundo']:.2f} ciclos/s")
        return resumen
    
    def generar_reporte_completo(self, resumen_metricas: Dict[str, Any],
                               comparar_con: Optional[str] = None) -> str:
        """Genera reporte completo de rendimiento"""
        
        # Archivo principal de reporte
        reporte_file = self.output_dir / f"performance_report_{self.timestamp}.md"
        
        with open(reporte_file, 'w', encoding='utf-8') as f:
            f.write(f"# Reporte de Rendimiento - {resumen_metricas['nombre_simulacion']}\n\n")
            f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Timestamp:** {self.timestamp}\n\n")
            
            # Resumen ejecutivo
            f.write("## 📈 Resumen Ejecutivo\n\n")
            f.write(f"- **Tiempo Total:** {resumen_metricas['tiempo_total']:.2f} segundos\n")
            f.write(f"- **Ciclos Ejecutados:** {resumen_metricas['num_ciclos']}\n")
            f.write(f"- **Tiempo Promedio por Ciclo:** {resumen_metricas['tiempo_promedio_ciclo']:.3f} segundos\n")
            f.write(f"- **Velocidad:** {resumen_metricas['ciclos_por_segundo']:.2f} ciclos/segundo\n")
            
            # Calcular métricas de eficiencia
            eficiencia = self._calcular_metricas_eficiencia(resumen_metricas)
            f.write(f"- **Eficiencia Estimada:** {eficiencia['score_eficiencia']:.1f}/10\n\n")
            
            # Análisis por secciones
            if resumen_metricas['tiempos_secciones']:
                f.write("## ⏱️ Análisis por Secciones\n\n")
                self._escribir_analisis_secciones(f, resumen_metricas['tiempos_secciones'])
            
            # Análisis de cuellos de botella
            f.write("## 🚧 Cuellos de Botella Identificados\n\n")
            cuellos_botella = self._identificar_cuellos_botella(resumen_metricas)
            for cuello in cuellos_botella:
                f.write(f"- **{cuello['seccion']}:** {cuello['descripcion']}\n")
                f.write(f"  - Tiempo total: {cuello['tiempo_total']:.2f}s\n")
                f.write(f"  - Porcentaje del total: {cuello['porcentaje']:.1f}%\n\n")
            
            # Recomendaciones
            f.write("## 💡 Recomendaciones de Optimización\n\n")
            recomendaciones = self._generar_recomendaciones(resumen_metricas)
            for i, rec in enumerate(recomendaciones, 1):
                f.write(f"{i}. **{rec['titulo']}**\n")
                f.write(f"   - {rec['descripcion']}\n")
                f.write(f"   - Impacto estimado: {rec['impacto_estimado']}\n\n")
            
            # Comparación con baseline si se proporciona
            if comparar_con:
                f.write("## ⚖️ Comparación con Baseline\n\n")
                self._escribir_comparacion_baseline(f, resumen_metricas, comparar_con)
            
            # Archivos generados
            f.write("## 📁 Archivos Generados\n\n")
            archivos = self._generar_archivos_datos(resumen_metricas)
            for archivo in archivos:
                f.write(f"- `{archivo}`\n")
        
        print(f"📄 Reporte completo generado: {reporte_file}")
        return str(reporte_file)
    
    def _calcular_metricas_eficiencia(self, resumen: Dict[str, Any]) -> Dict[str, float]:
        """Calcula métricas de eficiencia del rendimiento"""
        # Score basado en ciclos por segundo
        cps = resumen['ciclos_por_segundo']
        
        # Referencias de rendimiento (estimadas)
        if cps >= 5.0:  # Muy rápido
            score_velocidad = 10
        elif cps >= 2.0:  # Rápido
            score_velocidad = 8
        elif cps >= 1.0:  # Normal
            score_velocidad = 6
        elif cps >= 0.5:  # Lento
            score_velocidad = 4
        else:  # Muy lento
            score_velocidad = 2
        
        # Score basado en consistencia de tiempos
        if resumen['metricas_ciclo']:
            tiempos = [m['tiempo'] for m in resumen['metricas_ciclo']]
            coef_variacion = np.std(tiempos) / np.mean(tiempos) if np.mean(tiempos) > 0 else 1
            
            if coef_variacion <= 0.1:  # Muy consistente
                score_consistencia = 10
            elif coef_variacion <= 0.2:  # Consistente
                score_consistencia = 8
            elif coef_variacion <= 0.3:  # Moderadamente consistente
                score_consistencia = 6
            else:  # Inconsistente
                score_consistencia = 4
        else:
            score_consistencia = 5
        
        # Score de eficiencia general
        score_eficiencia = (score_velocidad + score_consistencia) / 2
        
        return {
            'score_eficiencia': score_eficiencia,
            'score_velocidad': score_velocidad,
            'score_consistencia': score_consistencia,
            'ciclos_por_segundo': cps
        }
    
    def _escribir_analisis_secciones(self, f, tiempos_secciones: Dict[str, List[float]]):
        """Escribe análisis detallado por secciones"""
        # Calcular estadísticas por sección
        stats_secciones = []
        tiempo_total_secciones = 0
        
        for seccion, tiempos in tiempos_secciones.items():
            if tiempos:
                tiempo_promedio = np.mean(tiempos)
                tiempo_total = np.sum(tiempos)
                tiempo_total_secciones += tiempo_total
                
                stats_secciones.append({
                    'seccion': seccion,
                    'tiempo_total': tiempo_total,
                    'tiempo_promedio': tiempo_promedio,
                    'num_llamadas': len(tiempos),
                    'tiempo_maximo': np.max(tiempos),
                    'tiempo_minimo': np.min(tiempos)
                })
        
        # Ordenar por tiempo total descendente
        stats_secciones.sort(key=lambda x: x['tiempo_total'], reverse=True)
        
        # Escribir tabla
        f.write("| Sección | Tiempo Total | % Total | Tiempo Promedio | Llamadas |\n")
        f.write("|---------|--------------|---------|-----------------|----------|\n")
        
        for stat in stats_secciones:
            porcentaje = (stat['tiempo_total'] / tiempo_total_secciones * 100) if tiempo_total_secciones > 0 else 0
            f.write(f"| {stat['seccion']} | {stat['tiempo_total']:.3f}s | {porcentaje:.1f}% | "
                   f"{stat['tiempo_promedio']:.3f}s | {stat['num_llamadas']} |\n")
        
        f.write("\n")
    
    def _identificar_cuellos_botella(self, resumen: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifica los principales cuellos de botella"""
        cuellos_botella = []
        
        # Analizar tiempos por sección
        if resumen['tiempos_secciones']:
            tiempo_total_secciones = sum(sum(tiempos) for tiempos in resumen['tiempos_secciones'].values())
            
            for seccion, tiempos in resumen['tiempos_secciones'].items():
                if tiempos:
                    tiempo_total = sum(tiempos)
                    porcentaje = (tiempo_total / tiempo_total_secciones * 100) if tiempo_total_secciones > 0 else 0
                    
                    # Considerar cuello de botella si usa >15% del tiempo
                    if porcentaje > 15:
                        descripcion = f"Sección que consume {porcentaje:.1f}% del tiempo total"
                        
                        if len(tiempos) > 1:
                            promedio = np.mean(tiempos)
                            std = np.std(tiempos)
                            if std / promedio > 0.3:  # Alta variabilidad
                                descripcion += " con alta variabilidad en tiempos"
                        
                        cuellos_botella.append({
                            'seccion': seccion,
                            'tiempo_total': tiempo_total,
                            'porcentaje': porcentaje,
                            'descripcion': descripcion
                        })
        
        # Analizar tiempo promedio por ciclo
        if resumen['tiempo_promedio_ciclo'] > 2.0:  # Ciclos muy lentos
            cuellos_botella.append({
                'seccion': 'Ciclo General',
                'tiempo_total': resumen['tiempo_total'],
                'porcentaje': 100.0,
                'descripcion': f"Ciclos muy lentos ({resumen['tiempo_promedio_ciclo']:.2f}s promedio)"
            })
        
        return sorted(cuellos_botella, key=lambda x: x['porcentaje'], reverse=True)
    
    def _generar_recomendaciones(self, resumen: Dict[str, Any]) -> List[Dict[str, str]]:
        """Genera recomendaciones específicas de optimización"""
        recomendaciones = []
        
        # Recomendaciones basadas en velocidad general
        cps = resumen['ciclos_por_segundo']
        if cps < 1.0:
            recomendaciones.append({
                'titulo': 'Optimización General de Velocidad',
                'descripcion': 'La simulación es lenta. Considerar vectorización de cálculos con NumPy/pandas',
                'impacto_estimado': 'Alto (20-40% mejora)'
            })
        
        # Recomendaciones basadas en secciones lentas
        if resumen['tiempos_secciones']:
            tiempo_total_secciones = sum(sum(tiempos) for tiempos in resumen['tiempos_secciones'].values())
            
            for seccion, tiempos in resumen['tiempos_secciones'].items():
                if tiempos:
                    tiempo_total = sum(tiempos)
                    porcentaje = (tiempo_total / tiempo_total_secciones * 100) if tiempo_total_secciones > 0 else 0
                    
                    if porcentaje > 20:
                        if 'mercado' in seccion.lower() or 'pib' in seccion.lower():
                            recomendaciones.append({
                                'titulo': f'Vectorizar {seccion}',
                                'descripcion': 'Usar operaciones vectorizadas para cálculos económicos',
                                'impacto_estimado': 'Alto (30-50% mejora en esta sección)'
                            })
                        elif 'persona' in seccion.lower() or 'agente' in seccion.lower():
                            recomendaciones.append({
                                'titulo': f'Paralelizar {seccion}',
                                'descripcion': 'Procesar agentes en paralelo usando multiprocessing',
                                'impacto_estimado': 'Medio (15-25% mejora en esta sección)'
                            })
        
        # Recomendaciones específicas por operaciones
        if resumen['contadores_operaciones']:
            for operacion, count in resumen['contadores_operaciones'].items():
                if count > 10000:  # Muchas operaciones
                    recomendaciones.append({
                        'titulo': f'Optimizar {operacion}',
                        'descripcion': f'Se ejecutaron {count} operaciones. Considerar caché o batch processing',
                        'impacto_estimado': 'Medio (10-20% mejora)'
                    })
        
        # Recomendaciones de memoria si se detectan problemas
        tiempo_promedio = resumen['tiempo_promedio_ciclo']
        if tiempo_promedio > 1.5:
            recomendaciones.append({
                'titulo': 'Optimización de Memoria',
                'descripcion': 'Ciclos lentos pueden indicar garbage collection frecuente. Revisar uso de memoria',
                'impacto_estimado': 'Medio (15-25% mejora)'
            })
        
        # Recomendación de configuración si hay muchos agentes
        num_ciclos = resumen['num_ciclos']
        if tiempo_promedio > 2.0 and num_ciclos > 30:
            recomendaciones.append({
                'titulo': 'Configuración de Simulación',
                'descripcion': 'Considerar reducir número de agentes o ciclos para desarrollo/testing',
                'impacto_estimado': 'Alto (proporcional a la reducción)'
            })
        
        return recomendaciones
    
    def _escribir_comparacion_baseline(self, f, resumen: Dict[str, Any], baseline_path: str):
        """Escribe comparación con baseline"""
        try:
            # Cargar datos de baseline
            with open(baseline_path, 'r') as baseline_file:
                baseline = json.load(baseline_file)
            
            # Comparar métricas clave
            mejora_tiempo = ((baseline['tiempo_total'] - resumen['tiempo_total']) / 
                           baseline['tiempo_total'] * 100) if baseline['tiempo_total'] > 0 else 0
            
            mejora_cps = ((resumen['ciclos_por_segundo'] - baseline['ciclos_por_segundo']) / 
                         baseline['ciclos_por_segundo'] * 100) if baseline['ciclos_por_segundo'] > 0 else 0
            
            f.write(f"- **Baseline:** {baseline.get('timestamp', 'Desconocido')}\n")
            f.write(f"- **Tiempo Total:** {resumen['tiempo_total']:.2f}s vs {baseline['tiempo_total']:.2f}s\n")
            f.write(f"- **Mejora en Tiempo:** {mejora_tiempo:+.1f}%\n")
            f.write(f"- **Velocidad:** {resumen['ciclos_por_segundo']:.2f} vs {baseline['ciclos_por_segundo']:.2f} ciclos/s\n")
            f.write(f"- **Mejora en Velocidad:** {mejora_cps:+.1f}%\n\n")
            
            # Evaluación de la mejora
            if mejora_tiempo >= 20:
                f.write("✅ **Excelente mejora de rendimiento alcanzada**\n\n")
            elif mejora_tiempo >= 10:
                f.write("🟡 **Buena mejora de rendimiento**\n\n")
            elif mejora_tiempo >= 0:
                f.write("🟡 **Mejora marginal de rendimiento**\n\n")
            else:
                f.write("❌ **Degradación de rendimiento detectada**\n\n")
                
        except Exception as e:
            f.write(f"⚠️ Error al cargar baseline: {e}\n\n")
    
    def _generar_archivos_datos(self, resumen: Dict[str, Any]) -> List[str]:
        """Genera archivos de datos adicionales"""
        archivos_generados = []
        
        # 1. CSV con métricas por ciclo
        if resumen['metricas_ciclo']:
            csv_file = self.output_dir / f"metricas_ciclo_{self.timestamp}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=resumen['metricas_ciclo'][0].keys())
                writer.writeheader()
                writer.writerows(resumen['metricas_ciclo'])
            archivos_generados.append(csv_file.name)
        
        # 2. JSON con resumen completo
        json_file = self.output_dir / f"resumen_completo_{self.timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(resumen, f, indent=2, ensure_ascii=False, default=str)
        archivos_generados.append(json_file.name)
        
        # 3. Gráfico de tiempos por ciclo
        if resumen['metricas_ciclo']:
            self._generar_graficos_rendimiento(resumen)
            archivos_generados.append(f"graficos_rendimiento_{self.timestamp}.png")
        
        return archivos_generados
    
    def _generar_graficos_rendimiento(self, resumen: Dict[str, Any]):
        """Genera gráficos de análisis de rendimiento"""
        plt.style.use('default')
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Tiempo por ciclo
        ciclos = [m['ciclo'] for m in resumen['metricas_ciclo']]
        tiempos = [m['tiempo'] for m in resumen['metricas_ciclo']]
        
        ax1.plot(ciclos, tiempos, 'b-', alpha=0.7, linewidth=1)
        ax1.axhline(y=np.mean(tiempos), color='r', linestyle='--', alpha=0.7, label=f'Promedio: {np.mean(tiempos):.3f}s')
        ax1.set_title('Tiempo por Ciclo')
        ax1.set_xlabel('Ciclo')
        ax1.set_ylabel('Tiempo (segundos)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Histograma de tiempos
        ax2.hist(tiempos, bins=20, alpha=0.7, color='green', edgecolor='black')
        ax2.axvline(x=np.mean(tiempos), color='r', linestyle='--', alpha=0.7, label=f'Promedio: {np.mean(tiempos):.3f}s')
        ax2.set_title('Distribución de Tiempos por Ciclo')
        ax2.set_xlabel('Tiempo (segundos)')
        ax2.set_ylabel('Frecuencia')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Tiempos por sección
        if resumen['tiempos_secciones']:
            secciones = list(resumen['tiempos_secciones'].keys())
            tiempos_totales = [sum(resumen['tiempos_secciones'][s]) for s in secciones]
            
            # Mostrar solo las 8 secciones más costosas
            if len(secciones) > 8:
                indices_top = np.argsort(tiempos_totales)[-8:]
                secciones = [secciones[i] for i in indices_top]
                tiempos_totales = [tiempos_totales[i] for i in indices_top]
            
            ax3.barh(range(len(secciones)), tiempos_totales, color='orange', alpha=0.7)
            ax3.set_yticks(range(len(secciones)))
            ax3.set_yticklabels([s[:20] + '...' if len(s) > 20 else s for s in secciones])
            ax3.set_title('Tiempo Total por Sección')
            ax3.set_xlabel('Tiempo Total (segundos)')
            ax3.grid(True, alpha=0.3)
        
        # 4. Velocidad de simulación
        ciclos_por_segundo = [1/t if t > 0 else 0 for t in tiempos]
        ax4.plot(ciclos, ciclos_por_segundo, 'purple', alpha=0.7, linewidth=1)
        ax4.axhline(y=np.mean(ciclos_por_segundo), color='r', linestyle='--', alpha=0.7, 
                   label=f'Promedio: {np.mean(ciclos_por_segundo):.2f} c/s')
        ax4.set_title('Velocidad de Simulación')
        ax4.set_xlabel('Ciclo')
        ax4.set_ylabel('Ciclos/segundo')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar gráfico
        chart_file = self.output_dir / f"graficos_rendimiento_{self.timestamp}.png"
        plt.savefig(chart_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 Gráficos de rendimiento guardados: {chart_file}")


# Decorator para medir tiempo de funciones automáticamente
def medir_tiempo(seccion: str):
    """Decorator para medir tiempo de ejecución de funciones"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            inicio = time.time()
            try:
                resultado = func(*args, **kwargs)
                return resultado
            finally:
                tiempo_transcurrido = time.time() - inicio
                # Intentar registrar en el reporter global si existe
                try:
                    from .ReporterRendimiento import _reporter_global
                    if _reporter_global:
                        _reporter_global.registrar_tiempo_seccion(seccion, tiempo_transcurrido)
                except:
                    pass  # No hay reporter global activo
        return wrapper
    return decorator


# Instancia global del reporter (opcional)
_reporter_global = None

def get_reporter_global() -> Optional[ReporterRendimiento]:
    """Obtiene la instancia global del reporter"""
    return _reporter_global

def set_reporter_global(reporter: ReporterRendimiento):
    """Establece la instancia global del reporter"""
    global _reporter_global
    _reporter_global = reporter

def clear_reporter_global():
    """Limpia la instancia global del reporter"""
    global _reporter_global
    _reporter_global = None