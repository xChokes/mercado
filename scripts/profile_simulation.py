#!/usr/bin/env python3
"""
Script de Perfilado de Rendimiento para Simulador de Mercado
===========================================================

Herramienta para analizar el rendimiento del simulador y identificar
cuellos de botella usando cProfile y line_profiler.

Uso:
    python3 scripts/profile_simulation.py --mode basic
    python3 scripts/profile_simulation.py --mode detailed --cycles 30
    python3 scripts/profile_simulation.py --mode compare --baseline

Requiere: pip install line_profiler memory_profiler
"""

import os
import sys
import time
import cProfile
import pstats
import argparse
import json
from pathlib import Path
from datetime import datetime
from io import StringIO

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    # Importaciones principales del simulador
    from src.config.ConfiguradorSimulacion import ConfiguradorSimulacion
    from main import ejecutar_simulacion_completa
    import numpy as np
    import pandas as pd
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Asegúrese de que todas las dependencias estén instaladas")
    sys.exit(1)


class ProfilerSimulacion:
    """Clase principal para perfilar la simulación"""
    
    def __init__(self, output_dir="results/perf"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def profile_basic(self, num_cycles=50, num_consumers=250):
        """Perfil básico usando cProfile"""
        print(f"🔬 INICIANDO PERFIL BÁSICO: {num_cycles} ciclos, {num_consumers} consumidores")
        
        # Configurar simulación
        config = ConfiguradorSimulacion()
        config_dict = config.config
        config_dict['simulacion']['num_ciclos'] = num_cycles
        config_dict['simulacion']['num_consumidores'] = num_consumers
        
        # Archivo de salida del perfil
        profile_file = self.output_dir / f"profile_basic_{self.timestamp}.prof"
        
        # Ejecutar con profiling
        pr = cProfile.Profile()
        start_time = time.time()
        
        pr.enable()
        try:
            mercado = ejecutar_simulacion_completa(config, f"profile_{self.timestamp}")
        except Exception as e:
            print(f"❌ Error durante simulación: {e}")
            return None
        finally:
            pr.disable()
        
        total_time = time.time() - start_time
        
        # Guardar estadísticas del perfil
        pr.dump_stats(str(profile_file))
        
        # Generar reporte de texto
        self._generar_reporte_basico(profile_file, total_time, num_cycles, num_consumers)
        
        return {
            'total_time': total_time,
            'profile_file': str(profile_file),
            'cycles': num_cycles,
            'consumers': num_consumers
        }
    
    def _generar_reporte_basico(self, profile_file, total_time, cycles, consumers):
        """Genera reporte textual del perfil básico"""
        report_file = self.output_dir / f"report_basic_{self.timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE RENDIMIENTO BÁSICO\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Timestamp: {self.timestamp}\n")
            f.write(f"Ciclos: {cycles}\n")
            f.write(f"Consumidores: {consumers}\n")
            f.write(f"Tiempo total: {total_time:.2f} segundos\n")
            f.write(f"Tiempo por ciclo: {total_time/cycles:.3f} segundos\n")
            f.write(f"Rendimiento: {cycles/total_time:.2f} ciclos/segundo\n\n")
            
            # Analizar estadísticas del perfil
            stats = pstats.Stats(str(profile_file))
            
            # Redirigir salida a string
            s = StringIO()
            stats.print_stats(30)  # Top 30 funciones
            stats_output = s.getvalue()
            s.close()
            
            f.write("TOP 30 FUNCIONES MÁS COSTOSAS:\n")
            f.write("-" * 40 + "\n")
            f.write(stats_output)
            
            # Funciones relacionadas con el mercado
            f.write("\n\nFUNCIONES DEL MERCADO:\n")
            f.write("-" * 30 + "\n")
            s = StringIO()
            old_stdout = sys.stdout
            sys.stdout = s
            stats.print_stats("Mercado")
            sys.stdout = old_stdout
            f.write(s.getvalue())
            
            # Funciones de personas/agentes
            f.write("\n\nFUNCIONES DE AGENTES:\n")
            f.write("-" * 25 + "\n")
            s = StringIO()
            old_stdout = sys.stdout
            sys.stdout = s
            stats.print_stats("Persona|Consumidor|Empresa")
            sys.stdout = old_stdout
            f.write(s.getvalue())
        
        print(f"📄 Reporte básico guardado en: {report_file}")
    
    def profile_detailed(self, num_cycles=30):
        """Perfil detallado con line_profiler (si está disponible)"""
        print(f"🔍 INICIANDO PERFIL DETALLADO: {num_cycles} ciclos")
        
        try:
            import line_profiler
        except ImportError:
            print("⚠️  line_profiler no disponible. Usando perfil básico extendido.")
            return self.profile_basic(num_cycles, 150)  # Simulación más pequeña
        
        # Configurar simulación
        config = ConfiguradorSimulacion()
        config_dict = config.config
        config_dict['simulacion']['num_ciclos'] = num_cycles
        config_dict['simulacion']['num_consumidores'] = 150  # Menos agentes para análisis detallado
        
        # Archivo de salida
        profile_file = self.output_dir / f"profile_detailed_{self.timestamp}.txt"
        
        # Nota: line_profiler requiere decoradores @profile, por lo que hacemos
        # un análisis híbrido con cProfile y mediciones manuales
        start_time = time.time()
        
        # Mediciones detalladas por sección
        timing_results = {}
        
        pr = cProfile.Profile()
        pr.enable()
        
        try:
            mercado = ejecutar_simulacion_completa(config, f"detailed_{self.timestamp}")
        except Exception as e:
            print(f"❌ Error durante simulación detallada: {e}")
            return None
        finally:
            pr.disable()
        
        total_time = time.time() - start_time
        
        # Generar reporte detallado
        self._generar_reporte_detallado(pr, profile_file, total_time, num_cycles)
        
        return {
            'total_time': total_time,
            'profile_file': str(profile_file),
            'cycles': num_cycles
        }
    
    def _generar_reporte_detallado(self, profiler, output_file, total_time, cycles):
        """Genera reporte detallado del rendimiento"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE RENDIMIENTO DETALLADO\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Timestamp: {self.timestamp}\n")
            f.write(f"Ciclos: {cycles}\n")
            f.write(f"Tiempo total: {total_time:.2f} segundos\n\n")
            
            # Estadísticas detalladas
            stats = pstats.Stats(profiler)
            
            # Análisis por módulos
            f.write("ANÁLISIS POR MÓDULOS:\n")
            f.write("-" * 40 + "\n")
            
            modulos_interes = [
                ("Mercado", "Mercado"),
                ("Agentes", "Consumidor|Empresa|Persona"),
                ("Sistemas", "Sistema|Banking|AI"),
                ("Config", "Config"),
                ("Utils", "utils|logging")
            ]
            
            for nombre, patron in modulos_interes:
                f.write(f"\n{nombre}:\n")
                f.write("-" * len(nombre) + "\n")
                s = StringIO()
                old_stdout = sys.stdout
                sys.stdout = s
                stats.print_stats(patron)
                sys.stdout = old_stdout
                output = s.getvalue()
                if output.strip():
                    f.write(output)
                else:
                    f.write("No se encontraron funciones relevantes\n")
        
        print(f"📄 Reporte detallado guardado en: {output_file}")
    
    def profile_memory(self, num_cycles=20):
        """Perfil de uso de memoria"""
        print(f"💾 INICIANDO PERFIL DE MEMORIA: {num_cycles} ciclos")
        
        try:
            from memory_profiler import profile as memory_profile
            import psutil
        except ImportError:
            print("⚠️  memory_profiler o psutil no disponibles. Saltando análisis de memoria.")
            return None
        
        process = psutil.Process(os.getpid())
        memoria_inicial = process.memory_info().rss / 1024 / 1024  # MB
        
        # Configurar simulación pequeña para análisis de memoria
        config = ConfiguradorSimulacion()
        config_dict = config.config
        config_dict['simulacion']['num_ciclos'] = num_cycles
        config_dict['simulacion']['num_consumidores'] = 100
        
        start_time = time.time()
        
        try:
            mercado = ejecutar_simulacion_completa(config, f"memory_{self.timestamp}")
        except Exception as e:
            print(f"❌ Error durante análisis de memoria: {e}")
            return None
        
        total_time = time.time() - start_time
        memoria_final = process.memory_info().rss / 1024 / 1024  # MB
        memoria_usada = memoria_final - memoria_inicial
        
        # Generar reporte de memoria
        memory_report = {
            'timestamp': self.timestamp,
            'cycles': num_cycles,
            'total_time': total_time,
            'memoria_inicial_mb': memoria_inicial,
            'memoria_final_mb': memoria_final,
            'memoria_usada_mb': memoria_usada,
            'memoria_por_ciclo_mb': memoria_usada / num_cycles if num_cycles > 0 else 0
        }
        
        report_file = self.output_dir / f"memory_report_{self.timestamp}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(memory_report, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Memoria inicial: {memoria_inicial:.1f} MB")
        print(f"💾 Memoria final: {memoria_final:.1f} MB")
        print(f"💾 Memoria usada: {memoria_usada:.1f} MB")
        print(f"📄 Reporte de memoria guardado en: {report_file}")
        
        return memory_report
    
    def compare_performance(self, baseline_file=None):
        """Compara rendimiento con una línea base"""
        print("⚖️  INICIANDO COMPARACIÓN DE RENDIMIENTO")
        
        # Ejecutar perfil actual
        current_results = self.profile_basic(50, 250)
        
        if not current_results:
            print("❌ Error en perfil actual")
            return None
        
        # Buscar archivo de línea base
        if not baseline_file:
            # Buscar el archivo de perfil más reciente (excluyendo el actual)
            profile_files = list(self.output_dir.glob("profile_basic_*.prof"))
            profile_files = [f for f in profile_files if self.timestamp not in f.name]
            
            if not profile_files:
                print("⚠️  No se encontró línea base. Guardando perfil actual como referencia.")
                return current_results
            
            baseline_file = max(profile_files, key=lambda f: f.stat().st_mtime)
        
        print(f"📊 Comparando con línea base: {baseline_file}")
        
        # Generar reporte de comparación
        self._generar_reporte_comparacion(current_results, baseline_file)
        
        return current_results
    
    def _generar_reporte_comparacion(self, current_results, baseline_file):
        """Genera reporte de comparación de rendimiento"""
        comparison_file = self.output_dir / f"comparison_{self.timestamp}.txt"
        
        # Analizar archivo de línea base
        baseline_stats = pstats.Stats(str(baseline_file))
        current_stats = pstats.Stats(current_results['profile_file'])
        
        with open(comparison_file, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE COMPARACIÓN DE RENDIMIENTO\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Perfil actual: {self.timestamp}\n")
            f.write(f"Línea base: {baseline_file.name}\n")
            f.write(f"Tiempo actual: {current_results['total_time']:.2f}s\n")
            
            # Intentar extraer tiempo de línea base del nombre del archivo
            # (esto es una aproximación, idealmente se guardaría en metadatos)
            f.write(f"\nCiclos: {current_results['cycles']}\n")
            f.write(f"Consumidores: {current_results['consumers']}\n\n")
            
            f.write("FUNCIONES CON MAYOR CAMBIO:\n")
            f.write("-" * 40 + "\n")
            
            # Comparar funciones principales
            # (Análisis simplificado - en producción se haría más sofisticado)
            f.write("Comparación de funciones principales disponible en los archivos de perfil individuales.\n")
            f.write("Use herramientas como snakeviz o gprof2dot para visualización avanzada.\n")
        
        print(f"📄 Reporte de comparación guardado en: {comparison_file}")
    
    def generar_reporte_consolidado(self):
        """Genera un reporte consolidado de todos los perfiles"""
        print("📋 GENERANDO REPORTE CONSOLIDADO")
        
        consolidado_file = self.output_dir / f"consolidated_report_{self.timestamp}.md"
        
        # Buscar todos los reportes generados en esta sesión
        reportes = list(self.output_dir.glob(f"*{self.timestamp}*"))
        
        with open(consolidado_file, 'w', encoding='utf-8') as f:
            f.write(f"# Reporte Consolidado de Rendimiento\n\n")
            f.write(f"**Timestamp:** {self.timestamp}\n")
            f.write(f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Archivos Generados\n\n")
            for reporte in sorted(reportes):
                f.write(f"- `{reporte.name}`\n")
            
            f.write("\n## Guía de Interpretación\n\n")
            f.write("### Archivos de Perfil (.prof)\n")
            f.write("Usar con `python -m pstats archivo.prof` o herramientas como snakeviz:\n")
            f.write("```bash\n")
            f.write("pip install snakeviz\n")
            f.write("snakeviz results/perf/profile_basic_*.prof\n")
            f.write("```\n\n")
            
            f.write("### Reportes de Texto (.txt)\n")
            f.write("Contienen análisis legibles de las funciones más costosas.\n\n")
            
            f.write("### Reportes de Memoria (.json)\n")
            f.write("Información sobre uso de memoria durante la simulación.\n\n")
            
            f.write("## Recomendaciones de Optimización\n\n")
            f.write("1. **Funciones más costosas:** Revisar funciones con mayor tiempo acumulado\n")
            f.write("2. **Bucles internos:** Identificar bucles con muchas llamadas\n")
            f.write("3. **Vectorización:** Considerar NumPy/pandas para operaciones matemáticas\n")
            f.write("4. **Caché:** Implementar caché para cálculos repetitivos\n")
            f.write("5. **Concurrencia:** Evaluar paralelización de agentes independientes\n")
        
        print(f"📋 Reporte consolidado guardado en: {consolidado_file}")


def main():
    parser = argparse.ArgumentParser(description="Profiler para Simulador de Mercado")
    parser.add_argument('--mode', choices=['basic', 'detailed', 'memory', 'compare', 'all'], 
                        default='basic', help='Modo de perfilado')
    parser.add_argument('--cycles', type=int, default=50, help='Número de ciclos')
    parser.add_argument('--consumers', type=int, default=250, help='Número de consumidores')
    parser.add_argument('--baseline', type=str, help='Archivo de línea base para comparación')
    parser.add_argument('--output-dir', type=str, default='results/perf', help='Directorio de salida')
    
    args = parser.parse_args()
    
    profiler = ProfilerSimulacion(args.output_dir)
    
    print("🚀 INICIANDO ANÁLISIS DE RENDIMIENTO")
    print("=" * 50)
    
    try:
        if args.mode == 'basic' or args.mode == 'all':
            profiler.profile_basic(args.cycles, args.consumers)
        
        if args.mode == 'detailed' or args.mode == 'all':
            profiler.profile_detailed(min(args.cycles, 30))
        
        if args.mode == 'memory' or args.mode == 'all':
            profiler.profile_memory(min(args.cycles, 20))
        
        if args.mode == 'compare':
            profiler.compare_performance(args.baseline)
        
        if args.mode == 'all':
            profiler.generar_reporte_consolidado()
        
        print("\n✅ ANÁLISIS DE RENDIMIENTO COMPLETADO")
        print(f"📁 Resultados en: {profiler.output_dir}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Análisis interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante análisis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()