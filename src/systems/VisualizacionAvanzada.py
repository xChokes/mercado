"""
Sistema de Visualización Avanzada para el Simulador Económico
Incluye dashboards interactivos, múltiples métricas y exportación de datos
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import csv
from datetime import datetime
import os


class DashboardEconomico:
    """Dashboard avanzado para visualización económica en tiempo real"""

    def __init__(self, mercado):
        self.mercado = mercado
        self.metricas_historicas = {
            'pib': [],
            'desempleo': [],
            'inflacion': [],
            'crisis_activa': [],
            'transacciones_por_ciclo': [],
            'empresas_activas': [],
            'modelos_ml_entrenados': [],
            'depositos_bancarios': [],
            'prestamos_totales': [],
            'indice_gini': []
        }

    def actualizar_metricas(self, ciclo):
        """Actualiza las métricas del dashboard con datos del ciclo actual"""
        # PIB
        pib_actual = self.mercado.pib_historico[-1] if self.mercado.pib_historico else 0
        self.metricas_historicas['pib'].append(pib_actual)

        # Desempleo
        consumidores_totales = len(self.mercado.getConsumidores())
        desempleados = len(
            [c for c in self.mercado.getConsumidores() if not c.empleado])
        tasa_desempleo = (desempleados / max(1, consumidores_totales)) * 100
        self.metricas_historicas['desempleo'].append(tasa_desempleo)

        # Inflación
        inflacion_actual = self.mercado.inflacion_historica[-1] if self.mercado.inflacion_historica else 0
        self.metricas_historicas['inflacion'].append(inflacion_actual * 100)

        # Crisis financiera
        self.metricas_historicas['crisis_activa'].append(
            1 if self.mercado.crisis_financiera_activa else 0)

        # Transacciones por ciclo - CORRECCIÓN CRÍTICA
        # Usar múltiples fuentes para obtener count real de transacciones
        transacciones_ciclo = 0
        
        # Método 1: Buscar por ciclo en transacciones globales
        if hasattr(self.mercado, 'transacciones') and self.mercado.transacciones:
            transacciones_ciclo = len([t for t in self.mercado.transacciones if t.get('ciclo', 0) == ciclo])
        
        # Método 2: Usar contador del ciclo actual si existe
        if hasattr(self.mercado, 'transacciones_ciclo_actual') and ciclo == getattr(self.mercado, 'ciclo_actual', 0):
            transacciones_ciclo = max(transacciones_ciclo, len(self.mercado.transacciones_ciclo_actual))
        
        # Método 3: Fallback usando volumen de transacciones si está disponible
        if transacciones_ciclo == 0 and hasattr(self.mercado, 'volumen_transacciones'):
            if len(self.mercado.volumen_transacciones) > 0:
                transacciones_ciclo = self.mercado.volumen_transacciones[-1] if isinstance(self.mercado.volumen_transacciones[-1], int) else 0
        
        self.metricas_historicas['transacciones_por_ciclo'].append(transacciones_ciclo)

        # Empresas activas
        empresas_activas = len(
            [e for e in self.mercado.getEmpresas() if hasattr(e, 'dinero') and e.dinero > 0])
        self.metricas_historicas['empresas_activas'].append(empresas_activas)

        # Modelos ML entrenados
        if hasattr(self.mercado, 'analytics_ml'):
            stats_ml = self.mercado.analytics_ml.obtener_estadisticas_analytics()
            modelos_entrenados = stats_ml.get('modelos_entrenados', 0)
        else:
            modelos_entrenados = 0
        self.metricas_historicas['modelos_ml_entrenados'].append(
            modelos_entrenados)

        # Métricas bancarias
        depositos_totales = 0
        prestamos_totales = 0
        if hasattr(self.mercado, 'sistema_bancario') and self.mercado.sistema_bancario.bancos:
            for banco in self.mercado.sistema_bancario.bancos:
                depositos_totales += sum(banco.depositos.values())
                prestamos_totales += sum([p['monto']
                                         for p in banco.prestamos.values()])

        self.metricas_historicas['depositos_bancarios'].append(
            depositos_totales)
        self.metricas_historicas['prestamos_totales'].append(prestamos_totales)
        
        # Índice de Gini - Calcular desigualdad de ingresos
        gini_actual = 0.0
        if hasattr(self.mercado, 'validador_economico'):
            try:
                metricas_avanzadas = self.mercado.validador_economico.calcular_metricas_avanzadas(self.mercado)
                gini_actual = metricas_avanzadas.get('indice_gini', 0.0)
            except Exception as e:
                # Calcular Gini directamente si falla el validador
                consumidores = self.mercado.getConsumidores()
                if consumidores:
                    ingresos = [getattr(c, 'dinero', 0) for c in consumidores]
                    gini_actual = self._calcular_gini_simple(ingresos)
        
        self.metricas_historicas['indice_gini'].append(gini_actual)

    def _calcular_gini_simple(self, ingresos):
        """Calcula coeficiente de Gini simple para backup"""
        if not ingresos or len(ingresos) < 2:
            return 0.0
        
        ingresos_ordenados = sorted([max(0, ing) for ing in ingresos])
        n = len(ingresos_ordenados)
        
        suma_diferencias = 0
        for i in range(n):
            for j in range(n):
                suma_diferencias += abs(ingresos_ordenados[i] - ingresos_ordenados[j])
        
        media_ingresos = sum(ingresos_ordenados) / n
        if media_ingresos == 0:
            return 0.0
        
        return suma_diferencias / (2 * n * n * media_ingresos)

    def crear_dashboard_completo(self, ciclo_actual, guardar_archivo=True, prefijo=None):
        """Crea un dashboard completo con múltiples gráficos"""
        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)
              ) = plt.subplots(3, 2, figsize=(16, 12))
        fig.suptitle(
            f'📊 Dashboard Económico Completo - Ciclo {ciclo_actual}', fontsize=16, fontweight='bold')

        ciclos = list(range(len(self.metricas_historicas['pib'])))

        # Gráfico 1: PIB
        ax1.plot(
            ciclos, self.metricas_historicas['pib'], 'b-', linewidth=2, label='PIB')
        ax1.fill_between(ciclos, self.metricas_historicas['pib'], alpha=0.3)
        ax1.set_title('💰 PIB por Ciclo')
        ax1.set_ylabel('PIB ($)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Gráfico 2: Desempleo y Crisis
        ax2_twin = ax2.twinx()
        ax2.plot(
            ciclos, self.metricas_historicas['desempleo'], 'r-', linewidth=2, label='Desempleo (%)')
        ax2_twin.fill_between(ciclos, self.metricas_historicas['crisis_activa'],
                              alpha=0.2, color='red', label='Crisis Activa')
        ax2.set_title('👥 Mercado Laboral y Crisis')
        ax2.set_ylabel('Desempleo (%)', color='red')
        ax2_twin.set_ylabel('Crisis (0/1)', color='darkred')
        ax2.grid(True, alpha=0.3)

        # Gráfico 3: Inflación
        ax3.plot(
            ciclos, self.metricas_historicas['inflacion'], 'g-', linewidth=2)
        ax3.axhline(y=2, color='orange', linestyle='--',
                    alpha=0.7, label='Objetivo (2%)')
        ax3.set_title('📈 Inflación')
        ax3.set_ylabel('Inflación (%)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        # Gráfico 4: Actividad Empresarial
        ax4.bar(
            ciclos, self.metricas_historicas['empresas_activas'], alpha=0.7, color='purple')
        ax4.plot(ciclos, self.metricas_historicas['transacciones_por_ciclo'],
                 'orange', linewidth=2, label='Transacciones')
        ax4.set_title('🏢 Actividad Empresarial')
        ax4.set_ylabel('Cantidad')
        ax4.grid(True, alpha=0.3)
        ax4.legend()

        # Gráfico 5: Sistema Bancario
        ax5.fill_between(ciclos, self.metricas_historicas['depositos_bancarios'],
                         alpha=0.5, color='blue', label='Depósitos')
        ax5.fill_between(ciclos, self.metricas_historicas['prestamos_totales'],
                         alpha=0.5, color='green', label='Préstamos')
        ax5.set_title('🏦 Sistema Bancario')
        ax5.set_ylabel('Monto ($)')
        ax5.grid(True, alpha=0.3)
        ax5.legend()

        # Gráfico 6: Machine Learning
        ax6.step(
            ciclos, self.metricas_historicas['modelos_ml_entrenados'], 'purple', linewidth=3)
        ax6.fill_between(
            ciclos, self.metricas_historicas['modelos_ml_entrenados'], alpha=0.3, color='purple')
        ax6.set_title('🤖 Modelos ML Entrenados')
        ax6.set_ylabel('Cantidad de Modelos')
        ax6.grid(True, alpha=0.3)

        # Ajustar layout
        plt.tight_layout()

        if guardar_archivo:
            timestamp = int(datetime.now().timestamp())
            prefix = f"{prefijo}_" if prefijo else ""
            filename = f'results/{prefix}dashboard_economico_completo_{timestamp}.png'
            os.makedirs('results', exist_ok=True)
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"📊 Dashboard guardado: {filename}")

        plt.show()
        return fig

    def exportar_datos_csv(self, filename=None):
        """Exporta todas las métricas a un archivo CSV"""
        if filename is None:
            timestamp = int(datetime.now().timestamp())
            filename = f'results/metricas_simulacion_{timestamp}.csv'

        # Crear DataFrame con todas las métricas
        max_len = max(len(v) for v in self.metricas_historicas.values())

        # Normalizar longitudes
        data = {}
        for key, values in self.metricas_historicas.items():
            # Completar con valores None si es más corto
            normalized_values = values + [None] * (max_len - len(values))
            data[key] = normalized_values

        data['ciclo'] = list(range(max_len))

        df = pd.DataFrame(data)

        os.makedirs('results', exist_ok=True)
        df.to_csv(filename, index=False)
        print(f"📄 Datos exportados a: {filename}")
        return filename

    def exportar_configuracion_json(self, filename=None):
        """Exporta la configuración actual de la simulación"""
        if filename is None:
            timestamp = int(datetime.now().timestamp())
            filename = f'results/configuracion_simulacion_{timestamp}.json'

        config_datos = {
            'timestamp': datetime.now().isoformat(),
            'ciclos_ejecutados': len(self.metricas_historicas['pib']),
            'configuracion_mercado': {
                'num_consumidores': len(self.mercado.getConsumidores()),
                'num_empresas': len(self.mercado.getEmpresas()),
                'crisis_financiera_activa': self.mercado.crisis_financiera_activa,
                'fase_ciclo_economico': getattr(self.mercado, 'fase_ciclo_economico', 'unknown')
            },
            'resultados_finales': {
                'pib_final': self.metricas_historicas['pib'][-1] if self.metricas_historicas['pib'] else 0,
                'desempleo_final': self.metricas_historicas['desempleo'][-1] if self.metricas_historicas['desempleo'] else 0,
                'inflacion_final': self.metricas_historicas['inflacion'][-1] if self.metricas_historicas['inflacion'] else 0,
                'modelos_ml_entrenados': self.metricas_historicas['modelos_ml_entrenados'][-1] if self.metricas_historicas['modelos_ml_entrenados'] else 0
            }
        }

        os.makedirs('results', exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config_datos, f, indent=2, ensure_ascii=False)

        print(f"⚙️ Configuración exportada a: {filename}")
        return filename

    def generar_reporte_textual(self):
        """Genera un reporte textual con estadísticas clave"""
        if not self.metricas_historicas['pib']:
            return "No hay datos disponibles para el reporte."

        reporte = []
        reporte.append("=" * 60)
        reporte.append("📊 REPORTE ECONÓMICO FINAL")
        reporte.append("=" * 60)

        # Métricas finales - CORRECCIÓN CRÍTICA del cálculo PIB
        pib_final = self.metricas_historicas['pib'][-1]
        pib_inicial = self.metricas_historicas['pib'][0] if len(
            self.metricas_historicas['pib']) > 1 else pib_final
        
        # CORRECCIÓN: Cálculo robusto de crecimiento PIB
        if pib_inicial > 0 and len(self.metricas_historicas['pib']) > 1:
            crecimiento_pib = ((pib_final - pib_inicial) / pib_inicial) * 100
            # Límite de seguridad para evitar valores absurdos
            crecimiento_pib = max(-99.9, min(1000.0, crecimiento_pib))
        else:
            crecimiento_pib = 0.0

        desempleo_promedio = np.mean(self.metricas_historicas['desempleo'])  # Ya está en %
        inflacion_promedio = np.mean(self.metricas_historicas['inflacion'])  # Ya está en %

        reporte.append(f"💰 PIB Final: ${pib_final:,.2f}")
        reporte.append(f"📈 Crecimiento PIB: {crecimiento_pib:+.2f}%")
        reporte.append(f"👥 Desempleo Promedio: {desempleo_promedio:.2f}%")
        reporte.append(f"📊 Inflación Promedio: {inflacion_promedio:.2f}%")

        # Ciclos en crisis
        ciclos_crisis = sum(self.metricas_historicas['crisis_activa'])
        total_ciclos = len(self.metricas_historicas['crisis_activa'])
        porcentaje_crisis = (ciclos_crisis / max(total_ciclos, 1)) * 100

        reporte.append(
            f"🚨 Ciclos en Crisis: {ciclos_crisis}/{total_ciclos} ({porcentaje_crisis:.1f}%)")

        # Actividad económica
        transacciones_totales = sum(
            self.metricas_historicas['transacciones_por_ciclo'])
        empresas_promedio = np.mean(
            self.metricas_historicas['empresas_activas'])

        reporte.append(f"💼 Transacciones Totales: {transacciones_totales:,}")
        reporte.append(f"🏢 Empresas Activas Promedio: {empresas_promedio:.1f}")

        # Sistema ML
        modelos_finales = self.metricas_historicas[
            'modelos_ml_entrenados'][-1] if self.metricas_historicas['modelos_ml_entrenados'] else 0
        reporte.append(f"🤖 Modelos ML Entrenados: {modelos_finales}")

        # Sistema bancario
        depositos_finales = self.metricas_historicas[
            'depositos_bancarios'][-1] if self.metricas_historicas['depositos_bancarios'] else 0
        prestamos_finales = self.metricas_historicas[
            'prestamos_totales'][-1] if self.metricas_historicas['prestamos_totales'] else 0

        reporte.append(f"🏦 Depósitos Bancarios: ${depositos_finales:,.2f}")
        reporte.append(f"💳 Préstamos Totales: ${prestamos_finales:,.2f}")

        reporte.append("=" * 60)

        return "\n".join(reporte)


class VisualizadorTiempoReal:
    """Visualizador para métricas en tiempo real durante la simulación"""

    def __init__(self):
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.suptitle('📈 Simulación Económica en Tiempo Real')
        plt.ion()  # Modo interactivo

    def actualizar_grafico_tiempo_real(self, dashboard):
        """Actualiza los gráficos en tiempo real"""
        # Limpiar axes
        for ax in self.axes.flat:
            ax.clear()

        ciclos = list(range(len(dashboard.metricas_historicas['pib'])))

        if not ciclos:
            return

        # PIB
        self.axes[0, 0].plot(
            ciclos, dashboard.metricas_historicas['pib'], 'b-', linewidth=2)
        self.axes[0, 0].set_title('PIB')
        self.axes[0, 0].grid(True)

        # Desempleo
        self.axes[0, 1].plot(
            ciclos, dashboard.metricas_historicas['desempleo'], 'r-', linewidth=2)
        self.axes[0, 1].set_title('Desempleo (%)')
        self.axes[0, 1].grid(True)

        # Empresas activas
        self.axes[1, 0].bar(
            ciclos, dashboard.metricas_historicas['empresas_activas'], alpha=0.7)
        self.axes[1, 0].set_title('Empresas Activas')
        self.axes[1, 0].grid(True)

        # Modelos ML
        self.axes[1, 1].step(
            ciclos, dashboard.metricas_historicas['modelos_ml_entrenados'], 'purple', linewidth=2)
        self.axes[1, 1].set_title('Modelos ML')
        self.axes[1, 1].grid(True)

        plt.tight_layout()
        plt.pause(0.1)  # Pausa pequeña para actualizar

    def cerrar(self):
        """Cierra la visualización en tiempo real"""
        plt.ioff()
        plt.close(self.fig)


# Funciones de conveniencia
def crear_dashboard_avanzado(mercado):
    """Función de conveniencia para crear un dashboard"""
    return DashboardEconomico(mercado)


def exportar_resultados_completos(dashboard, prefijo="simulacion"):
    """Exporta todos los resultados en múltiples formatos"""
    timestamp = int(datetime.now().timestamp())

    # CSV
    csv_file = dashboard.exportar_datos_csv(
        f'results/{prefijo}_datos_{timestamp}.csv')

    # JSON
    json_file = dashboard.exportar_configuracion_json(
        f'results/{prefijo}_config_{timestamp}.json')

    # Reporte textual
    reporte = dashboard.generar_reporte_textual()
    reporte_file = f'results/{prefijo}_reporte_{timestamp}.txt'
    os.makedirs('results', exist_ok=True)

    with open(reporte_file, 'w', encoding='utf-8') as f:
        f.write(reporte)

    print(f"📁 Resultados exportados:")
    print(f"  - Datos: {csv_file}")
    print(f"  - Configuración: {json_file}")
    print(f"  - Reporte: {reporte_file}")

    return csv_file, json_file, reporte_file
