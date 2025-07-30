#!/usr/bin/env python3
"""
Script para probar las visualizaciones de la simulación económica
"""
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt
import numpy as np
import time

def crear_grafico_ejemplo():
    """Crea un gráfico de ejemplo para probar"""
    
    # Datos simulados
    ciclos = list(range(0, 11))
    pib = [100000 - i*5000 + np.random.randint(-2000, 2000) for i in ciclos]
    desempleo = [5 + i*2 + np.random.uniform(-1, 1) for i in ciclos]
    inflacion = [2 + np.random.uniform(-0.5, 0.5) for _ in ciclos]
    
    # Crear figura con subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('📊 ANÁLISIS ECONÓMICO - SIMULACIÓN DE PRUEBA', fontsize=16, fontweight='bold')
    
    # PIB
    ax1.plot(ciclos, pib, 'b-', linewidth=2, marker='o')
    ax1.set_title('📈 PIB a lo largo del tiempo')
    ax1.set_xlabel('Ciclos')
    ax1.set_ylabel('PIB ($)')
    ax1.grid(True, alpha=0.3)
    
    # Desempleo
    ax2.plot(ciclos, desempleo, 'r-', linewidth=2, marker='s')
    ax2.set_title('👥 Tasa de Desempleo')
    ax2.set_xlabel('Ciclos')
    ax2.set_ylabel('Desempleo (%)')
    ax2.grid(True, alpha=0.3)
    
    # Inflación
    ax3.plot(ciclos, inflacion, 'g-', linewidth=2, marker='^')
    ax3.set_title('💰 Inflación')
    ax3.set_xlabel('Ciclos')
    ax3.set_ylabel('Inflación (%)')
    ax3.grid(True, alpha=0.3)
    
    # Distribución de empresas
    empresas = ['Productora1', 'Productora2', 'Comercial1', 'Comercial2', 'Comercial3']
    capitales = [250000, 180000, 120000, 95000, 87000]
    ax4.bar(empresas, capitales, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
    ax4.set_title('🏢 Capital por Empresa')
    ax4.set_ylabel('Capital ($)')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Guardar gráfico
    timestamp = int(time.time())
    filename = f'economia_test_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado como: {filename}")
    
    return filename

if __name__ == "__main__":
    print("🔬 Generando gráfico de prueba...")
    archivo = crear_grafico_ejemplo()
    print(f"📊 Visualización guardada exitosamente: {archivo}")
