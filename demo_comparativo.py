#!/usr/bin/env python3
"""
Demo: Análisis Comparativo Base vs Shock de Inflación
=====================================================

Este script ejecuta un análisis comparativo completo entre el escenario base 
y el escenario de shock inflacionario, generando insights automáticos sobre:

- Diferencias en evolución de precios por categoría
- Impacto en márgenes y rentabilidad empresarial  
- Efectos en comportamiento del consumidor
- Resiliencia del sistema bancario

Uso:
    python3 demo_comparativo.py
    python3 demo_comparativo.py --ciclos 30 --seed 123
"""

import argparse
import json
import os
import subprocess
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path


class AnalisisComparativo:
    """Analiza y compara resultados entre escenarios Base y Shock de Inflación."""
    
    def __init__(self, seed=42, num_ciclos=50):
        self.seed = seed
        self.num_ciclos = num_ciclos
        self.resultados = {}
        self.timestamp = int(time.time())
        
    def ejecutar_escenarios(self):
        """Ejecuta ambos escenarios y captura resultados."""
        escenarios = ['base', 'shock_inflacion']
        
        print("🚀 DEMO COMPARATIVO: BASE vs SHOCK DE INFLACIÓN")
        print("=" * 55)
        print(f"Configuración: {self.num_ciclos} ciclos, seed={self.seed}")
        print()
        
        for escenario in escenarios:
            print(f"⚡ Ejecutando escenario: {escenario.upper()}")
            inicio = time.time()
            
            # Ejecutar simulación
            cmd = [
                sys.executable, 'main.py',
                '--escenario', escenario,
                '--seed', str(self.seed)
            ]
            
            proc = subprocess.run(cmd, capture_output=True, text=True)
            duracion = time.time() - inicio
            
            if proc.returncode != 0:
                print(f"❌ Error ejecutando {escenario}: {proc.stderr}")
                return False
                
            print(f"✅ {escenario} completado en {duracion:.1f}s")
            
            # Cargar datos generados
            self.cargar_resultados(escenario)
            
        return True
        
    def cargar_resultados(self, escenario):
        """Carga los datos CSV y configuración del escenario."""
        results_dir = Path('results')
        
        # Buscar archivos más recientes del escenario
        archivos_datos = list(results_dir.glob(f'esc_{escenario}_datos_*.csv'))
        archivos_config = list(results_dir.glob(f'esc_{escenario}_config_*.json'))
        
        if not archivos_datos or not archivos_config:
            print(f"⚠️  No se encontraron resultados para {escenario}")
            return
            
        # Tomar el más reciente
        archivo_datos = max(archivos_datos, key=lambda x: x.stat().st_mtime)
        archivo_config = max(archivos_config, key=lambda x: x.stat().st_mtime)
        
        # Cargar datos
        try:
            df = pd.read_csv(archivo_datos)
            with open(archivo_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            self.resultados[escenario] = {
                'datos': df,
                'config': config,
                'archivo_datos': archivo_datos,
                'archivo_config': archivo_config
            }
            
            print(f"   📊 Datos cargados: {len(df)} registros")
            
        except Exception as e:
            print(f"❌ Error cargando datos de {escenario}: {e}")
            
    def analizar_kpis_principales(self):
        """Analiza y compara KPIs principales entre escenarios."""
        print("\n📈 ANÁLISIS DE KPIs PRINCIPALES")
        print("-" * 35)
        
        comparacion = {}
        
        for escenario, datos in self.resultados.items():
            if 'datos' not in datos:
                continue
                
            df = datos['datos']
            
            # Calcular KPIs finales (último ciclo)
            kpis = {
                'pib_final': df['pib'].iloc[-1] if 'pib' in df.columns else 0,
                'inflacion_promedio': df['inflacion'].mean() if 'inflacion' in df.columns else 0,
                'desempleo_final': df['desempleo'].iloc[-1] if 'desempleo' in df.columns else 0,
                'precio_promedio_final': df[[col for col in df.columns if 'precio_promedio' in col]].iloc[-1].mean() if any('precio_promedio' in col for col in df.columns) else 0,
                'transacciones_total': df['transacciones'].sum() if 'transacciones' in df.columns else 0
            }
            
            comparacion[escenario] = kpis
            
        # Mostrar comparación
        if len(comparacion) == 2:
            base = comparacion.get('base', {})
            shock = comparacion.get('shock_inflacion', {})
            
            print(f"{'Métrica':<25} {'Base':<15} {'Shock Inf.':<15} {'Diferencia':<15}")
            print("-" * 70)
            
            for metrica in base.keys():
                val_base = base.get(metrica, 0)
                val_shock = shock.get(metrica, 0)
                diferencia = ((val_shock - val_base) / val_base * 100) if val_base != 0 else 0
                
                print(f"{metrica:<25} {val_base:<15.2f} {val_shock:<15.2f} {diferencia:>+7.1f}%")
                
        return comparacion
        
    def analizar_evolucion_precios(self):
        """Analiza la evolución de precios por categoría."""
        print("\n💰 EVOLUCIÓN DE PRECIOS POR CATEGORÍA")
        print("-" * 40)
        
        # Crear gráfica comparativa
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Comparativo Base vs Shock de Inflación: Evolución de Precios', fontsize=16)
        
        categorias = ['alimentos', 'tecnologia', 'servicios', 'manufacturados']
        
        for i, categoria in enumerate(categorias):
            ax = axes[i//2, i%2]
            
            for escenario, datos in self.resultados.items():
                if 'datos' not in datos:
                    continue
                    
                df = datos['datos']
                col_precio = f'precio_promedio_{categoria}'
                
                if col_precio in df.columns:
                    color = 'blue' if escenario == 'base' else 'red'
                    label = 'Base' if escenario == 'base' else 'Shock Inflación'
                    ax.plot(df.index, df[col_precio], color=color, label=label, linewidth=2)
                    
            ax.set_title(f'Precios - {categoria.capitalize()}')
            ax.set_xlabel('Ciclo')
            ax.set_ylabel('Precio ($)')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
        plt.tight_layout()
        
        # Guardar gráfica
        os.makedirs('results', exist_ok=True)
        archivo_grafica = f'results/demo_comparativo_precios_{self.timestamp}.png'
        plt.savefig(archivo_grafica, dpi=300, bbox_inches='tight')
        print(f"📊 Gráfica guardada: {archivo_grafica}")
        
        plt.show()
        
    def generar_insights_automaticos(self):
        """Genera insights automáticos basados en el análisis."""
        print("\n🧠 INSIGHTS AUTOMÁTICOS")
        print("-" * 25)
        
        if len(self.resultados) < 2:
            print("⚠️  Se necesitan resultados de ambos escenarios para generar insights")
            return
            
        base_datos = self.resultados.get('base', {}).get('datos')
        shock_datos = self.resultados.get('shock_inflacion', {}).get('datos')
        
        if base_datos is None or shock_datos is None:
            print("⚠️  Datos insuficientes para análisis")
            return
            
        insights = []
        
        # Insight 1: Volatilidad de precios
        if 'precio_promedio_tecnologia' in base_datos.columns and 'precio_promedio_tecnologia' in shock_datos.columns:
            vol_base = base_datos['precio_promedio_tecnologia'].std()
            vol_shock = shock_datos['precio_promedio_tecnologia'].std()
            
            if vol_shock > vol_base * 1.2:
                insights.append(f"🔥 La volatilidad de precios en tecnología aumentó {((vol_shock/vol_base - 1) * 100):.1f}% en el escenario inflacionario")
            
        # Insight 2: Resiliencia del PIB
        if 'pib' in base_datos.columns and 'pib' in shock_datos.columns:
            pib_base_final = base_datos['pib'].iloc[-1]
            pib_shock_final = shock_datos['pib'].iloc[-1]
            
            diferencia_pib = (pib_shock_final - pib_base_final) / pib_base_final * 100
            
            if abs(diferencia_pib) < 5:
                insights.append(f"💪 La economía mostró resiliencia: PIB solo varió {diferencia_pib:+.1f}% ante shock inflacionario")
            elif diferencia_pib < -10:
                insights.append(f"⚠️  El shock inflacionario causó contracción significativa del PIB ({diferencia_pib:.1f}%)")
                
        # Insight 3: Comportamiento por categorías
        categorias_analisis = ['alimentos', 'tecnologia', 'servicios']
        cambios_categoria = {}
        
        for categoria in categorias_analisis:
            col = f'precio_promedio_{categoria}'
            if col in base_datos.columns and col in shock_datos.columns:
                precio_base_final = base_datos[col].iloc[-1]
                precio_shock_final = shock_datos[col].iloc[-1]
                cambio = (precio_shock_final - precio_base_final) / precio_base_final * 100
                cambios_categoria[categoria] = cambio
                
        if cambios_categoria:
            categoria_mas_afectada = max(cambios_categoria, key=lambda x: abs(cambios_categoria[x]))
            insights.append(f"🎯 '{categoria_mas_afectada}' fue la categoría más afectada con {cambios_categoria[categoria_mas_afectada]:+.1f}% de cambio en precios")
            
        # Mostrar insights
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
            
        if not insights:
            print("ℹ️  No se detectaron patrones significativos en esta ejecución")
            
        return insights
        
    def generar_reporte_completo(self, comparacion_kpis, insights):
        """Genera un reporte completo del análisis comparativo."""
        archivo_reporte = f'results/demo_comparativo_reporte_{self.timestamp}.txt'
        
        with open(archivo_reporte, 'w', encoding='utf-8') as f:
            f.write("REPORTE DEMO COMPARATIVO: BASE vs SHOCK DE INFLACIÓN\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Timestamp: {self.timestamp}\n")
            f.write(f"Configuración: {self.num_ciclos} ciclos, seed={self.seed}\n")
            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("RESUMEN EJECUTIVO\n")
            f.write("-" * 20 + "\n")
            f.write("Este análisis compara el comportamiento económico en condiciones\n")
            f.write("estables (Base) vs un entorno de presiones inflacionarias (Shock).\n\n")
            
            f.write("KPIs PRINCIPALES\n")
            f.write("-" * 20 + "\n")
            if comparacion_kpis and len(comparacion_kpis) == 2:
                base = comparacion_kpis.get('base', {})
                shock = comparacion_kpis.get('shock_inflacion', {})
                
                for metrica in base.keys():
                    val_base = base.get(metrica, 0)
                    val_shock = shock.get(metrica, 0)
                    diferencia = ((val_shock - val_base) / val_base * 100) if val_base != 0 else 0
                    f.write(f"{metrica}: Base={val_base:.2f}, Shock={val_shock:.2f} ({diferencia:+.1f}%)\n")
                    
            f.write("\nINSIGHTS CLAVE\n")
            f.write("-" * 15 + "\n")
            for i, insight in enumerate(insights, 1):
                f.write(f"{i}. {insight}\n")
                
            f.write("\nRECOMENDACIONES PARA PRICING\n")
            f.write("-" * 30 + "\n")
            f.write("- Monitorear categorías de alta elasticidad en entornos inflacionarios\n")
            f.write("- Considerar estrategias de pricing dinámico basadas en volatilidad\n")
            f.write("- Evaluar hedging de costos para productos esenciales\n")
            f.write("- Implementar análisis de sensibilidad regular\n\n")
            
            f.write("ARCHIVOS GENERADOS\n")
            f.write("-" * 20 + "\n")
            for escenario, datos in self.resultados.items():
                if 'archivo_datos' in datos:
                    f.write(f"{escenario}: {datos['archivo_datos']}\n")
                    
        print(f"\n📄 Reporte completo guardado: {archivo_reporte}")
        
    def ejecutar_demo_completo(self):
        """Ejecuta el demo completo de análisis comparativo."""
        print("Iniciando demo comparativo...\n")
        
        # 1. Ejecutar escenarios
        if not self.ejecutar_escenarios():
            print("❌ Error ejecutando escenarios")
            return False
            
        # 2. Analizar KPIs
        comparacion_kpis = self.analizar_kpis_principales()
        
        # 3. Analizar evolución de precios
        self.analizar_evolucion_precios()
        
        # 4. Generar insights
        insights = self.generar_insights_automaticos()
        
        # 5. Generar reporte
        self.generar_reporte_completo(comparacion_kpis, insights)
        
        print("\n🎉 Demo comparativo completado exitosamente!")
        print(f"📁 Revisa la carpeta 'results/' para archivos generados")
        
        return True


def main():
    parser = argparse.ArgumentParser(description='Demo comparativo Base vs Shock de Inflación')
    parser.add_argument('--ciclos', type=int, default=50, help='Número de ciclos por escenario')
    parser.add_argument('--seed', type=int, default=42, help='Semilla para reproducibilidad')
    
    args = parser.parse_args()
    
    demo = AnalisisComparativo(seed=args.seed, num_ciclos=args.ciclos)
    
    try:
        demo.ejecutar_demo_completo()
    except KeyboardInterrupt:
        print("\n⛔ Demo interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando demo: {e}")
        return 1
        
    return 0


if __name__ == '__main__':
    sys.exit(main())
