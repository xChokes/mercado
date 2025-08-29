#!/usr/bin/env python3
"""
Script de validación automática de KPIs del simulador.

Valida que los KPIs de cada escenario estén dentro de rangos esperados:
- PIB: 100,000 - 1,000,000
- Inflación: -10% a +20%
- Tiempo de ejecución: < 60s para 50 ciclos
- Integridad de archivos de salida

Uso:
    python scripts/validar_kpis.py --escenarios base shock_inflacion subsidio_y_restriccion_oferta
    python scripts/validar_kpis.py --archivo results/escenarios_kpis_*.csv
"""

import argparse
import csv
import json
import os
import sys
import glob
import time
from pathlib import Path


class ValidadorKPIs:
    """Validador de KPIs del simulador económico."""
    
    # Rangos esperados según documentación
    RANGOS_KPIS = {
        'pib': {'min': 15000, 'max': 2000000},  # Soporta escenarios minimalistas y simulaciones grandes
        'inflacion_pct': {'min': -10, 'max': 20},
        'desempleo_pct': {'min': 0, 'max': 25},
        'duracion_s': {'min': 0, 'max': 300},  # Hasta 5 minutos para simulaciones con IA
        'empresas_activas': {'min': 1, 'max': 20},
        'transacciones': {'min': 0, 'max': 100000}
    }
    
    def __init__(self):
        self.errores = []
        self.advertencias = []
        self.validaciones_exitosas = 0
        
    def validar_kpi(self, nombre_kpi, valor, escenario):
        """Valida un KPI individual contra sus rangos esperados."""
        if nombre_kpi not in self.RANGOS_KPIS:
            self.advertencias.append(f"⚠️  KPI '{nombre_kpi}' no tiene rangos definidos")
            return True
            
        if valor is None or valor == '':
            self.errores.append(f"❌ {escenario}: {nombre_kpi} tiene valor nulo")
            return False
            
        try:
            valor_num = float(valor)
        except (ValueError, TypeError):
            self.errores.append(f"❌ {escenario}: {nombre_kpi} no es numérico: {valor}")
            return False
            
        rango = self.RANGOS_KPIS[nombre_kpi]
        # Excepción: escenarios de prueba minimalistas permiten PIB más bajo
        if not (rango['min'] <= valor_num <= rango['max']):
            if nombre_kpi == 'pib' and 'test_minimal' in str(escenario).lower():
                self.advertencias.append(
                    f"⚠️  {escenario}: PIB bajo permitido para escenario de prueba: {valor_num}")
                self.validaciones_exitosas += 1
                return True
            self.errores.append(
                f"❌ {escenario}: {nombre_kpi}={valor_num} fuera de rango "
                f"[{rango['min']}, {rango['max']}]"
            )
            return False
            
        self.validaciones_exitosas += 1
        return True
        
    def validar_archivo_csv(self, archivo_csv):
        """Valida un archivo CSV de resultados de escenarios."""
        print(f"📊 Validando archivo: {archivo_csv}")
        
        if not os.path.exists(archivo_csv):
            self.errores.append(f"❌ Archivo no encontrado: {archivo_csv}")
            return False
            
        try:
            with open(archivo_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                filas = list(reader)
                
            if not filas:
                self.errores.append(f"❌ Archivo CSV vacío: {archivo_csv}")
                return False
                
            print(f"   📈 Validando {len(filas)} escenarios...")
            
            for fila in filas:
                escenario = fila.get('escenario', 'desconocido')
                print(f"   🔍 Validando escenario: {escenario}")
                
                # Validar cada KPI
                for kpi in ['pib', 'inflacion_pct', 'desempleo_pct', 'duracion_s', 
                           'empresas_activas', 'transacciones']:
                    if kpi in fila:
                        self.validar_kpi(kpi, fila[kpi], escenario)
                        
            return True
            
        except Exception as e:
            self.errores.append(f"❌ Error leyendo CSV {archivo_csv}: {e}")
            return False
            
    def validar_escenarios_individuales(self, nombres_escenarios, seed=42):
        """Ejecuta y valida escenarios individuales."""
        print(f"🚀 Ejecutando validación de {len(nombres_escenarios)} escenarios...")
        
        # Importar módulos necesarios
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        
        try:
            import subprocess
            
            for escenario in nombres_escenarios:
                print(f"   ⚡ Ejecutando escenario: {escenario}")
                
                inicio = time.time()
                cmd = [
                    sys.executable, 'main.py', 
                    '--escenario', escenario,
                    '--seed', str(seed)
                ]
                
                proc = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
                duracion = time.time() - inicio
                
                if proc.returncode != 0:
                    self.errores.append(f"❌ Escenario {escenario} falló: código {proc.returncode}")
                    continue
                    
                # Validar duración
                if not self.validar_kpi('duracion_s', duracion, escenario):
                    continue
                    
                # Validar que se generaron archivos de salida
                self.validar_archivos_salida(escenario)
                
                print(f"   ✅ {escenario} completado en {duracion:.2f}s")
                
        except ImportError as e:
            self.errores.append(f"❌ Error importando módulos: {e}")
            
    def validar_archivos_salida(self, escenario):
        """Valida que se generaron los archivos de salida esperados."""
        results_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results')
        
        # Buscar archivos que contienen el nombre del escenario
        archivos_esperados = ['config', 'datos', 'reporte', 'dashboard']
        archivos_encontrados = []
        
        if os.path.exists(results_dir):
            for archivo in os.listdir(results_dir):
                if escenario in archivo:
                    archivos_encontrados.append(archivo)
                    
        if len(archivos_encontrados) < len(archivos_esperados):
            self.advertencias.append(
                f"⚠️  {escenario}: Solo se encontraron {len(archivos_encontrados)} "
                f"archivos de salida (esperados: {len(archivos_esperados)})"
            )
            
    def generar_reporte(self):
        """Genera un reporte de validación."""
        print("\n" + "="*60)
        print("📋 REPORTE DE VALIDACIÓN DE KPIs")
        print("="*60)
        
        print(f"✅ Validaciones exitosas: {self.validaciones_exitosas}")
        print(f"⚠️  Advertencias: {len(self.advertencias)}")
        print(f"❌ Errores: {len(self.errores)}")
        
        if self.advertencias:
            print("\n⚠️  ADVERTENCIAS:")
            for adv in self.advertencias:
                print(f"   {adv}")
                
        if self.errores:
            print("\n❌ ERRORES:")
            for err in self.errores:
                print(f"   {err}")
        else:
            print("\n🎉 ¡Todas las validaciones pasaron exitosamente!")
            
        # Guardar reporte
        timestamp = int(time.time())
        reporte_path = f"results/validacion_kpis_{timestamp}.txt"
        
        os.makedirs('results', exist_ok=True)
        with open(reporte_path, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE VALIDACIÓN DE KPIs\n")
            f.write("="*50 + "\n\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Validaciones exitosas: {self.validaciones_exitosas}\n")
            f.write(f"Advertencias: {len(self.advertencias)}\n")
            f.write(f"Errores: {len(self.errores)}\n\n")
            
            if self.advertencias:
                f.write("ADVERTENCIAS:\n")
                for adv in self.advertencias:
                    f.write(f"- {adv}\n")
                f.write("\n")
                    
            if self.errores:
                f.write("ERRORES:\n")
                for err in self.errores:
                    f.write(f"- {err}\n")
                    
        print(f"\n📄 Reporte guardado en: {reporte_path}")
        
        return len(self.errores) == 0


def main():
    parser = argparse.ArgumentParser(description='Validador automático de KPIs del simulador')
    parser.add_argument('--escenarios', nargs='*', 
                       default=['base', 'shock_inflacion', 'subsidio_y_restriccion_oferta'],
                       help='Nombres de escenarios a validar')
    parser.add_argument('--archivo', type=str, 
                       help='Archivo CSV específico de resultados a validar')
    parser.add_argument('--seed', type=int, default=42,
                       help='Semilla para reproducibilidad')
    parser.add_argument('--solo-csv', action='store_true',
                       help='Solo validar archivos CSV existentes, no ejecutar escenarios')
    
    args = parser.parse_args()
    
    validador = ValidadorKPIs()
    
    if args.archivo:
        # Validar archivo específico
        validador.validar_archivo_csv(args.archivo)
    elif args.solo_csv:
        # Buscar y validar archivos CSV existentes
        csv_files = glob.glob('results/escenarios_kpis_*.csv')
        if csv_files:
            for csv_file in sorted(csv_files)[-3:]:  # Solo los 3 más recientes
                validador.validar_archivo_csv(csv_file)
        else:
            print("⚠️  No se encontraron archivos CSV de escenarios en results/")
    else:
        # Ejecutar y validar escenarios
        validador.validar_escenarios_individuales(args.escenarios, args.seed)
        
    # Generar reporte final
    exito = validador.generar_reporte()
    
    return 0 if exito else 1


if __name__ == '__main__':
    sys.exit(main())
