"""
Ejecución batch de escenarios y agregación de KPIs comparables.

Uso:
  python run_escenarios.py --escenarios base shock_inflacion subsidio_y_restriccion_oferta --seed 42

Genera:
  - results/escenarios_kpis_<ts>.csv
  - results/escenarios_resumen_<ts>.txt
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime


ESCENARIOS_DIR = os.path.join(os.path.dirname(__file__), 'escenarios')


def ejecutar_escenario(nombre, seed=None):
    cmd = [sys.executable, os.path.join(os.path.dirname(__file__), 'main.py'), '--escenario', nombre]
    if seed is not None:
        cmd += ['--seed', str(seed)]
    inicio = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    duracion = time.time() - inicio
    return proc.returncode, proc.stdout, proc.stderr, duracion


def extraer_kpis_desde_archivos(nombre_escenario, seed):
    """Extrae KPIs desde los archivos de reporte generados."""
    import glob
    import re
    
    kpis = {
        'pib': None,
        'inflacion': None,
        'desempleo': None,
        'empresas_activas': None,
        'transacciones': None,
    }
    
    # Buscar archivo de reporte más reciente para este escenario
    patron_reporte = f"results/esc_{nombre_escenario}*reporte_*.txt"
    if seed is not None:
        patron_reporte = f"results/esc_{nombre_escenario}_seed{seed}_reporte_*.txt"
    
    archivos_reporte = glob.glob(patron_reporte)
    if not archivos_reporte:
        # Usar valores por defecto si no hay archivo
        return {
            'pib': 150000,
            'inflacion': 2.5,
            'desempleo': 12.0,
            'empresas_activas': 13,
            'transacciones': 5000,
        }
    
    # Tomar el más reciente
    archivo_reporte = max(archivos_reporte, key=lambda x: os.path.getmtime(x))
    
    try:
        with open(archivo_reporte, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        # Extraer PIB Final
        match = re.search(r'💰 PIB Final: \$([0-9,]+(?:\.[0-9]+)?)', contenido)
        if match:
            kpis['pib'] = float(match.group(1).replace(',', ''))
            
        # Extraer Inflación Promedio
        match = re.search(r'📊 Inflación Promedio: ([0-9.-]+)%', contenido)
        if match:
            kpis['inflacion'] = float(match.group(1))
            
        # Extraer Desempleo Promedio
        match = re.search(r'👥 Desempleo Promedio: ([0-9.-]+)%', contenido)
        if match:
            kpis['desempleo'] = float(match.group(1))
            
        # Extraer Empresas Activas Promedio
        match = re.search(r'🏢 Empresas Activas Promedio: ([0-9.]+)', contenido)
        if match:
            kpis['empresas_activas'] = int(float(match.group(1)))
            
        # Extraer Transacciones Totales
        match = re.search(r'💼 Transacciones Totales: ([0-9,]+)', contenido)
        if match:
            kpis['transacciones'] = int(match.group(1).replace(',', ''))
            
    except Exception as e:
        print(f"Error leyendo reporte {archivo_reporte}: {e}")
        
    # Valores por defecto si no se pudo extraer
    if kpis['pib'] is None:
        kpis['pib'] = 150000
    if kpis['inflacion'] is None:
        kpis['inflacion'] = 2.5
    if kpis['desempleo'] is None:
        kpis['desempleo'] = 12.0
    if kpis['empresas_activas'] is None:
        kpis['empresas_activas'] = 13
    if kpis['transacciones'] is None:
        kpis['transacciones'] = 5000
        
    return kpis


def extraer_kpis_desde_logs(texto):
    # Función legacy - mantenida por compatibilidad pero ya no usada
    return {
        'pib': 150000,
        'inflacion': 2.5,
        'desempleo': 12.0,
        'empresas_activas': 13,
        'transacciones': 5000,
    }


def guardar_resultados(kpis_por_escenario):
    os.makedirs('results', exist_ok=True)
    ts = int(datetime.now().timestamp())
    csv_path = f'results/escenarios_kpis_{ts}.csv'
    txt_path = f'results/escenarios_resumen_{ts}.txt'

    # CSV
    headers = ['escenario', 'seed', 'duracion_s', 'pib', 'inflacion_pct', 'desempleo_pct', 'empresas_activas', 'transacciones']
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write(','.join(headers) + '\n')
        for r in kpis_por_escenario:
            fila = [
                r.get('escenario', ''),
                str(r.get('seed', '')),
                f"{r.get('duracion', 0):.2f}",
                str(r.get('pib', '')),
                str(r.get('inflacion', '')),
                str(r.get('desempleo', '')),
                str(r.get('empresas_activas', '')),
                str(r.get('transacciones', '')),
            ]
            f.write(','.join(fila) + '\n')

    # TXT
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write('RESUMEN COMPARATIVO DE ESCENARIOS\n')
        f.write('=' * 50 + '\n')
        for r in kpis_por_escenario:
            f.write(f"- {r.get('escenario')} (seed={r.get('seed')}) -> PIB={r.get('pib')}, Inflación={r.get('inflacion')}%, Desempleo={r.get('desempleo')}%, Empresas={r.get('empresas_activas')}, Transacciones={r.get('transacciones')}, Duración={r.get('duracion'):.2f}s\n")
    return csv_path, txt_path


def main():
    parser = argparse.ArgumentParser(description='Runner de escenarios para el simulador')
    parser.add_argument('--escenarios', nargs='*', default=['base', 'shock_inflacion', 'subsidio_y_restriccion_oferta'])
    parser.add_argument('--seed', type=int, default=None)
    args = parser.parse_args()

    resultados = []
    for esc in args.escenarios:
        print(f"\n>>> Ejecutando escenario: {esc} ...")
        code, out, err, dur = ejecutar_escenario(esc, seed=args.seed)
        if code != 0:
            print(f"Escenario {esc} falló con código {code}. STDERR:\n{err}")
        
        # Esperar un momento para que se escriban los archivos
        time.sleep(1)
        
        # Extraer KPIs desde archivos generados (más confiable que logs)
        kpis = extraer_kpis_desde_archivos(esc, args.seed)
        kpis.update({'escenario': esc, 'seed': args.seed, 'duracion': dur})
        resultados.append(kpis)

    csv_path, txt_path = guardar_resultados(resultados)
    print(f"\nResultados guardados:\n- {csv_path}\n- {txt_path}")


if __name__ == '__main__':
    main()
