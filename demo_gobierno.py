#!/usr/bin/env python3
"""
Demostración del Sistema Gubernamental con Análisis Fiscal
Muestra cómo el PIB se descompone en C+I+G+(NX) y el impacto fiscal
"""

import sys
import os

# Agregar el directorio raíz del proyecto al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.models.Mercado import Mercado
from src.models.Consumidor import Consumidor
from src.models.Empresa import Empresa

def main():
    print("🏛️ DEMOSTRACIÓN: SISTEMA GUBERNAMENTAL Y ANÁLISIS FISCAL")
    print("=" * 60)
    
    # Crear mercado de demostración
    bienes = ['alimentos', 'ropa', 'tecnologia', 'servicios', 'vivienda']
    mercado = Mercado(bienes)
    
    # Agregar agentes representativos
    print("\n📊 Configurando economía de demostración...")
    
    # Consumidores con diferentes niveles de ingreso
    for i in range(20):
        consumidor = Consumidor(f"Ciudadano{i:02d}", mercado)
        consumidor.dinero = 5000 + i * 2000  # Entre $5,000 y $43,000
        consumidor.ingreso_mensual = 2000 + i * 800  # Entre $2,000 y $17,200
        mercado.agregar_persona(consumidor)
    
    # Empresas de diferentes tamaños
    for i in range(5):
        empresa = Empresa(f"Empresa{i+1}", mercado, bienes)
        empresa.dinero = 50000 + i * 25000  # Entre $50,000 y $150,000
        mercado.agregar_persona(empresa)
    
    print(f"✅ Economía configurada: {len(mercado.getConsumidores())} consumidores, {len(mercado.getEmpresas())} empresas")
    
    # Demostrar análisis fiscal por varios ciclos
    print("\n🔄 EJECUTANDO SIMULACIÓN FISCAL (5 ciclos)")
    print("-" * 50)
    
    for ciclo in range(1, 6):
        print(f"\n📈 CICLO {ciclo}")
        
        # Simular algunas transacciones
        import random
        for _ in range(random.randint(10, 20)):
            consumidor = random.choice(mercado.getConsumidores())
            bien = random.choice(bienes)
            cantidad = random.randint(1, 3)
            precio = random.randint(50, 200)
            costo_total = cantidad * precio
            
            if consumidor.dinero >= costo_total:
                mercado.registrar_transaccion(consumidor, bien, cantidad, costo_total, ciclo)
        
        # Ejecutar estadísticas (que incluye el ciclo fiscal)
        mercado.ciclo_actual = ciclo
        mercado.registrar_estadisticas()
        
        # Obtener estadísticas fiscales
        stats_fiscales = mercado.obtener_estadisticas_fiscales()
        pib_componentes = mercado.obtener_pib_descompuesto()
        pib_actual = mercado.pib_historico[-1] if mercado.pib_historico else 0
        
        # Mostrar resultados
        print(f"  PIB Total: ${pib_actual:,.2f}")
        
        if pib_componentes:
            print(f"  📊 DESCOMPOSICIÓN PIB (C+I+G+NX):")
            for componente, valor in pib_componentes.items():
                porcentaje = (valor / pib_actual * 100) if pib_actual > 0 else 0
                print(f"    {componente.value}: ${valor:,.2f} ({porcentaje:.1f}%)")
        
        if stats_fiscales:
            print(f"  🏛️ ESTADO FISCAL:")
            print(f"    Balance Fiscal: ${stats_fiscales.get('balance_fiscal', 0):,.2f}")
            print(f"    Deuda Pública: ${stats_fiscales.get('deuda_publica', 0):,.2f}")
            print(f"    Ratio Deuda/PIB: {stats_fiscales.get('deuda_pib_ratio', 0)*100:.1f}%")
            print(f"    Política Fiscal: {stats_fiscales.get('politica_fiscal', 'N/A').upper()}")
    
    # Mostrar reporte fiscal completo
    if hasattr(mercado, 'government'):
        print("\n📋 REPORTE FISCAL COMPLETO")
        print("=" * 60)
        reporte = mercado.government.generar_reporte_fiscal()
        print(reporte)
    
    # Análisis de estabilidad fiscal
    print("\n📊 ANÁLISIS DE ESTABILIDAD FISCAL")
    print("-" * 50)
    
    if len(mercado.pib_historico) > 1:
        pib_inicial = mercado.pib_historico[0]
        pib_final = mercado.pib_historico[-1]
        crecimiento = ((pib_final - pib_inicial) / pib_inicial * 100) if pib_inicial > 0 else 0
        
        print(f"Crecimiento PIB: {crecimiento:.1f}%")
        print(f"PIB Promedio: ${sum(mercado.pib_historico) / len(mercado.pib_historico):,.2f}")
        
        # Verificar estabilidad
        variacion_max = max(mercado.pib_historico) - min(mercado.pib_historico)
        pib_promedio = sum(mercado.pib_historico) / len(mercado.pib_historico)
        volatilidad = (variacion_max / pib_promedio * 100) if pib_promedio > 0 else 0
        
        print(f"Volatilidad PIB: {volatilidad:.1f}%")
        
        if volatilidad < 30:
            print("✅ Sistema fiscal ESTABLE")
        elif volatilidad < 60:
            print("⚠️ Sistema fiscal MODERADAMENTE ESTABLE")
        else:
            print("❌ Sistema fiscal INESTABLE")
    
    # Demostrar diferentes políticas fiscales
    print("\n🎛️ DEMO: IMPACTO DE POLÍTICAS FISCALES")
    print("-" * 50)
    
    if hasattr(mercado, 'government'):
        from src.systems.government import TipoPoliticaFiscal
        
        politicas = [TipoPoliticaFiscal.EXPANSIVA, TipoPoliticaFiscal.CONTRACTIVA, TipoPoliticaFiscal.NEUTRAL]
        
        for politica in politicas:
            mercado.government.politica_fiscal = politica
            resultado = mercado.government.ejecutar_ciclo_fiscal(99)  # Ciclo especial de demo
            
            print(f"\n  🏛️ Política {politica.value.upper()}:")
            print(f"    Gasto Público: ${resultado['gasto_publico']:,.2f}")
            print(f"    Recaudación: ${resultado['recaudacion']:,.2f}")
            print(f"    Balance: ${resultado['balance_fiscal']:,.2f}")
    
    print("\n🎯 DEMOSTRACIÓN COMPLETADA")
    print("✅ El sistema governmental permite:")
    print("  - PIB descompuesto en C+I+G+(NX)")
    print("  - Balance fiscal y gestión de deuda pública")
    print("  - Política fiscal adaptativa")
    print("  - Estabilidad en escenarios baseline")
    print("  - Tests comprensivos del impacto fiscal")

if __name__ == "__main__":
    main()