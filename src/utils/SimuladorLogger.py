"""
Sistema de Logging para el Simulador Económico
Proporciona logging detallado con diferentes niveles y rotación automática
"""

import logging
import os
import time
from datetime import datetime


class SimuladorLogger:
    """Maneja el sistema de logging del simulador económico"""

    def __init__(self, log_dir="logs", log_level=logging.INFO):
        self.log_dir = log_dir
        self.log_level = log_level
        self.logger = None
        self.setup_logging()

    def setup_logging(self):
        """Configura el sistema de logging"""
        # Crear directorio de logs si no existe
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Nombre del archivo de log con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"simulacion_{timestamp}.log"
        log_path = os.path.join(self.log_dir, log_filename)

        # Configurar logger principal
        self.logger = logging.getLogger('SimuladorEconomico')
        self.logger.setLevel(self.log_level)

        # Limpiar handlers anteriores
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Configurar formato de logging
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Handler para archivo
        file_handler = logging.FileHandler(
            log_path, mode='w', encoding='utf-8')
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Handler para consola (solo INFO y superior)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '🔧 %(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Crear loggers especializados
        self.setup_specialized_loggers(formatter)

        self.logger.info(
            f"Sistema de logging iniciado - Archivo: {log_filename}")

    def setup_specialized_loggers(self, formatter):
        """Configura loggers especializados para diferentes componentes"""
        components = ['Mercado', 'Empresa', 'Consumidor',
                      'Banco', 'Crisis', 'ML', 'Precios']

        for component in components:
            comp_logger = logging.getLogger(f'SimuladorEconomico.{component}')
            comp_logger.setLevel(self.log_level)
            comp_logger.propagate = True  # Propagar al logger padre

    def get_logger(self, component=None):
        """Obtiene un logger para un componente específico"""
        if component:
            return logging.getLogger(f'SimuladorEconomico.{component}')
        return self.logger

    def log_ciclo_inicio(self, ciclo):
        """Log del inicio de un ciclo"""
        self.logger.info(f"{'='*60}")
        self.logger.info(f"INICIO CICLO {ciclo}")
        self.logger.info(f"{'='*60}")

    def log_ciclo_fin(self, ciclo, duracion):
        """Log del fin de un ciclo"""
        self.logger.info(f"FIN CICLO {ciclo} - Duración: {duracion:.3f}s")
        self.logger.info(f"{'='*60}")

    def log_metricas_ciclo(self, ciclo, pib, inflacion, desempleo, transacciones):
        """Log de métricas principales del ciclo"""
        self.logger.info(f"MÉTRICAS CICLO {ciclo}:")
        self.logger.info(f"  💰 PIB: ${pib:,.2f}")
        self.logger.info(f"  📈 Inflación: {inflacion*100:.2f}%")
        self.logger.info(f"  👥 Desempleo: {desempleo*100:.1f}%")
        self.logger.info(f"  💼 Transacciones: {transacciones}")

    def log_prestamo(self, banco, solicitante, monto, tasa, aprobado):
        """Log de operaciones de préstamos"""
        banco_logger = self.get_logger('Banco')
        if aprobado:
            banco_logger.info(
                f"PRÉSTAMO APROBADO - {solicitante}: ${monto:,.0f} al {tasa:.1%}")
        else:
            banco_logger.debug(
                f"PRÉSTAMO RECHAZADO - {solicitante}: ${monto:,.0f}")

    def log_contratacion(self, empresa, empleado, salario):
        """Log de contrataciones"""
        mercado_logger = self.get_logger('Mercado')
        mercado_logger.info(
            f"CONTRATACIÓN - {empresa} contrató a {empleado} por ${salario:,.0f}")

    def log_crisis_estado(self, activa, ciclos_en_crisis, motivo=""):
        """Log de estado de crisis"""
        crisis_logger = self.get_logger('Crisis')
        if activa:
            crisis_logger.warning(
                f"CRISIS ACTIVA - Ciclos: {ciclos_en_crisis}")
        else:
            crisis_logger.info(f"CRISIS RESUELTA - Motivo: {motivo}")

    def log_precio_cambio(self, empresa, bien, precio_anterior, precio_nuevo):
        """Log de cambios de precios"""
        precios_logger = self.get_logger('Precios')
        cambio_pct = ((precio_nuevo / precio_anterior) - 1) * \
            100 if precio_anterior > 0 else 0
        precios_logger.debug(
            f"PRECIO {bien} - {empresa}: ${precio_anterior:.2f} → ${precio_nuevo:.2f} ({cambio_pct:+.1f}%)")

    def log_transaccion(self, consumidor, bien, cantidad, precio_total):
        """Log de transacciones"""
        mercado_logger = self.get_logger('Mercado')
        mercado_logger.debug(
            f"TRANSACCIÓN - {consumidor} compró {cantidad}x {bien} por ${precio_total:.2f}")

    def log_error_with_component(self, component, error_msg, exception=None):
        """Log de errores con componente específico"""
        error_logger = self.get_logger(component)
        if exception:
            error_logger.error(f"ERROR: {error_msg}", exc_info=True)
        else:
            error_logger.error(f"ERROR: {error_msg}")

    def log_warning(self, component, warning_msg):
        """Log de advertencias"""
        warning_logger = self.get_logger(component)
        warning_logger.warning(warning_msg)

    # === MÉTODOS SIMPLIFICADOS PARA MAIN.PY ===
    def log_inicio(self, mensaje):
        """Log de inicio de sistema"""
        self.logger.info(f"INICIO: {mensaje}")

    def log_configuracion(self, mensaje):
        """Log de configuración"""
        self.logger.info(f"CONFIG: {mensaje}")

    def log_ciclo(self, mensaje):
        """Log de ciclos"""
        self.logger.info(f"CICLO: {mensaje}")

    def log_crisis(self, mensaje):
        """Log de crisis"""
        crisis_logger = self.get_logger('Crisis')
        crisis_logger.warning(f"CRISIS: {mensaje}")

    def log_sistema(self, mensaje):
        """Log de sistema general"""
        self.logger.info(f"SISTEMA: {mensaje}")

    def log_ml(self, mensaje):
        """Log de ML"""
        ml_logger = self.get_logger('ML')
        ml_logger.info(f"ML: {mensaje}")

    def log_precios(self, mensaje):
        """Log de precios"""
        precios_logger = self.get_logger('Precios')
        precios_logger.info(f"PRECIOS: {mensaje}")

    def log_metricas(self, mensaje):
        """Log de métricas"""
        self.logger.info(f"MÉTRICAS: {mensaje}")

    def log_reporte(self, mensaje):
        """Log de reportes"""
        self.logger.info(f"REPORTE: {mensaje}")

    def log_fin(self, mensaje):
        """Log de finalización"""
        self.logger.info(f"FIN: {mensaje}")

    def log_error(self, mensaje):
        """Log de error simplificado"""
        self.logger.error(f"ERROR: {mensaje}")

    def close(self):
        """Cierra el sistema de logging"""
        if self.logger:
            for handler in self.logger.handlers:
                handler.close()
                self.logger.removeHandler(handler)


# Instancia global del logger
_simulador_logger = None


def get_simulador_logger():
    """Obtiene la instancia global del logger"""
    global _simulador_logger
    if _simulador_logger is None:
        _simulador_logger = SimuladorLogger()
    return _simulador_logger


def init_logging(log_level=logging.INFO):
    """Inicializa el sistema de logging"""
    global _simulador_logger
    _simulador_logger = SimuladorLogger(log_level=log_level)
    return _simulador_logger


def close_logging():
    """Cierra el sistema de logging"""
    global _simulador_logger
    if _simulador_logger:
        _simulador_logger.close()
        _simulador_logger = None
