"""
Sistema Bancario Avanzado para la Simulación Económica
Implementa intermediación financiera, crédito y política monetaria
"""
import random
import math
import logging
from ..config.ConfigEconomica import ConfigEconomica


class Banco:
    def __init__(self, nombre, capital_inicial=1000000):
        self.nombre = nombre
        self.capital = capital_inicial
        self.depositos = {}  # {persona_id: monto}
        self.prestamos = {}  # {persona_id: {'monto': x, 'tasa': y, 'plazo': z}}
        self.reservas = capital_inicial * 0.1  # 10% en reservas
        self.tasa_depositos = 0.02  # 2% anual
        self.tasa_base_prestamos = 0.08  # 8% anual base
        self.ratio_capital = 0.08  # Ratio de capital mínimo
        self.morosidad_historica = []

        # Gestión de riesgo sistémico
        self.exposiciones_interbancarias = {}  # {nombre_banco: monto}
        self.estado = 'activo'

        # Políticas de riesgo
        self.limite_credito_individual = capital_inicial * 0.1
        self.ratio_prestamos_depositos_max = 0.9

    def evaluar_riesgo_crediticio(self, solicitante):
        """Evalúa el riesgo crediticio de un solicitante"""
        from ..models.Consumidor import Consumidor
        from ..models.Empresa import Empresa

        if isinstance(solicitante, Consumidor):
            # Factor ingreso
            factor_ingreso = min(1.0, solicitante.ingreso_mensual / 5000)

            # Factor empleo
            factor_empleo = 1.0 if solicitante.empleado else 0.3

            # Factor ahorros
            factor_ahorros = min(1.0, solicitante.ahorros / 10000)

            # Factor deuda existente
            factor_deuda = max(
                0.1, 1.0 - (solicitante.deuda / max(1, solicitante.ingreso_mensual * 12)))

            score = (factor_ingreso * 0.4 + factor_empleo * 0.3 +
                     factor_ahorros * 0.2 + factor_deuda * 0.1)

        elif isinstance(solicitante, Empresa):
            # Factor capital
            factor_capital = min(1.0, solicitante.dinero / 100000)

            # Factor ventas (basado en transacciones)
            ventas_recientes = getattr(solicitante, 'ventas_ultimos_ciclos', 0)
            factor_ventas = min(1.0, ventas_recientes / 50000)

            # Factor tiempo en mercado
            factor_experiencia = 0.8  # Simplificado

            score = (factor_capital * 0.5 + factor_ventas * 0.3 +
                     factor_experiencia * 0.2)

        else:
            score = 0.5  # Score neutral para otros tipos

        return max(0.1, min(1.0, score))

    def calcular_tasa_prestamo(self, solicitante, monto):
        """Calcula la tasa de interés para un préstamo"""
        riesgo = self.evaluar_riesgo_crediticio(solicitante)

        # Tasa base + spread por riesgo
        spread_riesgo = (1.0 - riesgo) * 0.15  # Hasta 15% adicional

        # Ajuste por monto (préstamos grandes tienen mejores tasas)
        ajuste_monto = -0.02 if monto > 100000 else 0.01

        # Ajuste por liquidez del banco
        ratio_liquidez = self.reservas / max(1, sum(self.depositos.values()))
        ajuste_liquidez = 0.03 if ratio_liquidez < 0.1 else 0

        tasa_final = (self.tasa_base_prestamos + spread_riesgo +
                      ajuste_monto + ajuste_liquidez)

        return max(0.03, min(0.25, tasa_final))  # Entre 3% y 25%

    def solicitar_prestamo(self, solicitante, monto, plazo_meses=12):
        """Procesa una solicitud de préstamo con criterios más flexibles y logging"""
        # Debug: Información de la solicitud
        nombre_solicitante = getattr(solicitante, 'nombre', 'Desconocido')

        # Verificar límites básicos pero más flexibles
        limite_flexible = self.limite_credito_individual * 3  # Triplicar límite
        if monto > limite_flexible:
            # Solo log a nivel WARNING para rechazos críticos
            logging.warning(
                f"Préstamo rechazado para {nombre_solicitante}: Monto ${monto:,.0f} excede límite ${limite_flexible:,.0f}")
            return False, f"Monto excede límite individual de ${limite_flexible:,.0f}"

        prestamos_totales = sum([p['monto'] for p in self.prestamos.values()])
        depositos_totales = sum(self.depositos.values())

        # Usar reservas si no hay suficientes depósitos
        fondos_disponibles = depositos_totales + self.reservas * 0.9
        ratio_maximo = 1.5  # Permitir aún más préstamos

        if (prestamos_totales + monto) > (fondos_disponibles * ratio_maximo):
            # Solo log a nivel WARNING para rechazos por liquidez
            logging.warning(
                f"Préstamo rechazado para {nombre_solicitante}: Insuficiente liquidez")
            return False, f"Insuficiente liquidez bancaria (${fondos_disponibles:,.0f} disponibles)"

        # Evaluar riesgo con criterios más flexibles para empresas
        riesgo = self.evaluar_riesgo_crediticio(solicitante)
        
        # CRITERIOS ULTRA FLEXIBLES para empresas productoras en dificultades
        from src.models.EmpresaProductora import EmpresaProductora
        if isinstance(solicitante, EmpresaProductora):
            # Para empresas productoras, ser mucho más permisivo
            limite_riesgo = 0.05  # Bajar de 0.15 a 0.05 (súper permisivo)
            
            # Si la empresa tiene empleados y capacidad productiva, darle una oportunidad
            if (hasattr(solicitante, 'empleados') and len(solicitante.empleados) > 0 and
                hasattr(solicitante, 'capacidad_produccion') and solicitante.capacidad_produccion):
                limite_riesgo = 0.02  # Aún más permisivo para empresas operativas
                
            # Para préstamos de emergencia pequeños (supervivencia), ser extremadamente flexible
            if monto <= 30000:  # Préstamos pequeños de supervivencia
                limite_riesgo = 0.01  # Casi automático
        else:
            limite_riesgo = 0.15  # Mantener estándar original para consumidores
            
        if riesgo < limite_riesgo:
            # Solo log a nivel WARNING para rechazos por riesgo
            logging.warning(
                f"Préstamo rechazado para {nombre_solicitante}: Riesgo muy alto ({riesgo:.2f})")
            return False, f"Riesgo crediticio alto ({riesgo:.2f})"

        # Aprobar préstamo
        tasa = self.calcular_tasa_prestamo(solicitante, monto)
        persona_id = id(solicitante)

        self.prestamos[persona_id] = {
            'monto': monto,
            'tasa_anual': tasa,
            'plazo_meses': plazo_meses,
            'cuota_mensual': self._calcular_cuota(monto, tasa, plazo_meses),
            'saldo_pendiente': monto,
            'meses_restantes': plazo_meses,
            'solicitante': solicitante
        }

        # Entregar dinero al solicitante
        solicitante.dinero += monto

        # Reducir reservas/depósitos del banco
        if self.reservas >= monto:
            self.reservas -= monto
        else:
            diferencia = monto - self.reservas
            self.reservas = 0
            # Usar parte de los depósitos si es necesario
            self.capital -= diferencia * 0.1  # Solo 10% del capital

        # Solo log INFO para aprobaciones exitosas, sin emojis
        logging.info(
            f"Préstamo aprobado para {nombre_solicitante}: ${monto:,.0f} al {tasa:.1%}")
        return True, f"Préstamo aprobado: ${monto:,.2f} al {tasa:.2%} anual"

    def _calcular_cuota(self, capital, tasa_anual, plazo_meses):
        """Calcula la cuota mensual de un préstamo"""
        tasa_mensual = tasa_anual / 12
        if tasa_mensual == 0:
            return capital / plazo_meses

        cuota = capital * (tasa_mensual * (1 + tasa_mensual)**plazo_meses) / \
            ((1 + tasa_mensual)**plazo_meses - 1)
        return cuota

    def cobrar_cuotas(self):
        """Cobra las cuotas mensuales de todos los préstamos"""
        morosos = []
        pagos_recibidos = 0

        for persona_id, prestamo in list(self.prestamos.items()):
            solicitante = prestamo['solicitante']
            cuota = prestamo['cuota_mensual']

            if solicitante.dinero >= cuota:
                # Pago exitoso
                solicitante.dinero -= cuota
                prestamo['saldo_pendiente'] -= (
                    cuota - prestamo['saldo_pendiente'] * prestamo['tasa_anual'] / 12)
                prestamo['meses_restantes'] -= 1
                pagos_recibidos += cuota

                # Préstamo completado
                if prestamo['meses_restantes'] <= 0:
                    del self.prestamos[persona_id]

            else:
                # Mora
                morosos.append(persona_id)
                prestamo['dias_mora'] = prestamo.get('dias_mora', 0) + 30

                # Quiebra por mora excesiva
                if prestamo['dias_mora'] > 180:  # 6 meses de mora
                    self.capital -= prestamo['saldo_pendiente']  # Pérdida
                    del self.prestamos[persona_id]

        self.reservas += pagos_recibidos
        morosidad_actual = len(morosos) / max(1, len(self.prestamos))
        self.morosidad_historica.append(morosidad_actual)

        return len(morosos), pagos_recibidos

    def depositar(self, persona, monto):
        """Registra un depósito"""
        persona_id = id(persona)
        if persona_id not in self.depositos:
            self.depositos[persona_id] = 0

        self.depositos[persona_id] += monto
        persona.dinero -= monto
        self.reservas += monto * 0.1  # 10% a reservas

    def retirar(self, persona, monto):
        """Procesa un retiro"""
        persona_id = id(persona)
        if persona_id in self.depositos and self.depositos[persona_id] >= monto:
            self.depositos[persona_id] -= monto
            persona.dinero += monto
            self.reservas -= monto * 0.1
            return True
        return False

    def pagar_intereses_depositos(self):
        """Paga intereses a los depositantes"""
        total_intereses = 0
        for persona_id, saldo in self.depositos.items():
            interes = saldo * (self.tasa_depositos / 12)  # Mensual
            self.depositos[persona_id] += interes
            total_intereses += interes

        self.capital -= total_intereses
        return total_intereses

    def obtener_estadisticas(self):
        """Retorna estadísticas del banco"""
        prestamos_totales = sum([p['monto'] for p in self.prestamos.values()])
        depositos_totales = sum(self.depositos.values())
        morosidad_actual = self.morosidad_historica[-1] if self.morosidad_historica else 0

        return {
            'capital': self.capital,
            'prestamos_totales': prestamos_totales,
            'depositos_totales': depositos_totales,
            'reservas': self.reservas,
            'morosidad': morosidad_actual,
            'ratio_capital': self.capital / max(1, prestamos_totales),
            'ratio_solvencia': self.calcular_ratio_solvencia(),
            'numero_prestamos': len(self.prestamos),
            'numero_depositantes': len(self.depositos)
        }

    def calcular_ratio_solvencia(self):
        """Calcula un ratio de solvencia simple"""
        pasivos = sum(self.depositos.values())
        if pasivos == 0:
            return 1.0
        return (self.capital + self.reservas) / pasivos

    def otorgar_prestamo(self, solicitante, monto, plazo_meses=12):
        """Alias para solicitar_prestamo - mantiene compatibilidad"""
        return self.solicitar_prestamo(solicitante, monto, plazo_meses)

    def recibir_deposito(self, persona, monto):
        """Alias para depositar - mantiene compatibilidad"""
        try:
            self.depositar(persona, monto)
            return True
        except Exception:
            return False


class SistemaBancario:
    """Coordinador del sistema bancario nacional"""

    def __init__(self, mercado):
        self.mercado = mercado
        self.bancos = []
        self.banco_central = BancoCentral(mercado)

        # Crear bancos comerciales
        for i in range(3):  # 3 bancos principales
            nombre = f"Banco{i+1}"
            capital = random.randint(2000000, 5000000)
            banco = Banco(nombre, capital)
            self.bancos.append(banco)

        # Establecer exposiciones interbancarias iniciales
        for banco in self.bancos:
            for otro in self.bancos:
                if banco is not otro and random.random() < 0.3:
                    monto = banco.capital * 0.05
                    banco.exposiciones_interbancarias[otro.nombre] = monto

    def ciclo_bancario(self):
        """Ejecuta el ciclo de todos los bancos"""
        # Ciclo del banco central
        self.banco_central.ciclo_banco_central()

        # Actualizar tasas de todos los bancos basado en banco central
        tasa_referencia = self.banco_central.tasa_referencia
        for banco in self.bancos:
            banco.tasa_base_prestamos = tasa_referencia + 0.03  # Spread de 3%

        # Operaciones bancarias
        total_morosos = 0
        total_pagos = 0

        for banco in self.bancos:
            morosos, pagos = banco.cobrar_cuotas()
            total_morosos += morosos
            total_pagos += pagos

            # Pagar intereses a depositantes
            banco.pagar_intereses_depositos()

        # Evaluar solvencia y eventos de default
        bancos_en_default = []
        for banco in list(self.bancos):
            if banco.calcular_ratio_solvencia() < banco.ratio_capital or banco.capital < 0:
                bancos_en_default.append(banco)
                self.bancos.remove(banco)
                banco.estado = 'default'

                # Propagar pérdidas por exposiciones interbancarias
                for otro in self.bancos:
                    perdida = otro.exposiciones_interbancarias.pop(
                        banco.nombre, 0)
                    if perdida > 0:
                        otro.capital -= perdida

        return {
            'morosos_totales': total_morosos,
            'pagos_totales': total_pagos,
            'bancos_activos': len(self.bancos),
            'bancos_en_default': [b.nombre for b in bancos_en_default]
        }

    def obtener_banco_optimal(self, persona, tipo_operacion='prestamo'):
        """Encuentra el mejor banco para una operación"""
        if tipo_operacion == 'prestamo':
            # Banco con menor tasa para préstamos
            mejor_banco = min(self.bancos, key=lambda b: b.tasa_base_prestamos)
        else:  # depósito
            # Banco con mayor tasa para depósitos
            mejor_banco = max(self.bancos, key=lambda b: b.tasa_depositos)

        return mejor_banco

    def obtener_estadisticas_sistema(self):
        """Estadísticas consolidadas del sistema bancario"""
        stats = {
            'capital_total': sum([b.capital for b in self.bancos]),
            'prestamos_totales': sum([sum([p['monto'] for p in b.prestamos.values()]) for b in self.bancos]),
            'depositos_totales': sum([sum(b.depositos.values()) for b in self.bancos]),
            'tasa_referencia': self.banco_central.tasa_referencia,
            'bancos_operando': len(self.bancos),
            'exposiciones_interbancarias': sum([sum(b.exposiciones_interbancarias.values()) for b in self.bancos])
        }
        return stats


class BancoCentral:
    """Banco Central con política monetaria"""

    def __init__(self, mercado):
        self.mercado = mercado
        self.tasa_referencia = 0.05  # 5% base
        self.meta_inflacion = 0.02  # 2% anual
        self.reservas_internacionales = 10000000
        self.base_monetaria = 50000000

    def ciclo_banco_central(self):
        """Ejecuta política monetaria"""
        # Obtener inflación actual
        if len(self.mercado.inflacion_historica) > 0:
            inflacion_actual = self.mercado.inflacion_historica[-1]

            # Regla de Taylor simplificada
            diferencia_inflacion = inflacion_actual - self.meta_inflacion
            diferencia_pib = 0  # Simplificado por ahora

            # Ajustar tasa de referencia
            ajuste = 1.5 * diferencia_inflacion + 0.5 * diferencia_pib
            nueva_tasa = self.tasa_referencia + ajuste * 0.1  # Suavizado

            # Límites de tasa
            self.tasa_referencia = max(0.001, min(0.15, nueva_tasa))

    def intervenir_en_crisis(self, sistema_bancario, monto_total: float = 1000000):
        """Inyecta liquidez a los bancos durante una crisis"""
        if self.reservas_internacionales <= 0 or not sistema_bancario.bancos:
            return 0

        apoyo_por_banco = monto_total / len(sistema_bancario.bancos)
        apoyo_por_banco = min(
            apoyo_por_banco, self.reservas_internacionales / len(sistema_bancario.bancos))

        for banco in sistema_bancario.bancos:
            banco.reservas += apoyo_por_banco
            banco.capital += apoyo_por_banco * 0.1

        self.reservas_internacionales -= apoyo_por_banco * \
            len(sistema_bancario.bancos)
        return apoyo_por_banco * len(sistema_bancario.bancos)
