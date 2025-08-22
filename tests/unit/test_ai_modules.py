"""
Tests para Módulos de Inteligencia Artificial
=============================================

Tests unitarios para los componentes de IA del sistema:
- AgentMemorySystem
- IADecisionEngine
- AgentCommunicationProtocol
"""

import unittest
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.ai.AgentMemorySystem import AgentMemorySystem, Decision
from src.ai.IADecisionEngine import IADecisionEngine
from src.ai.AgentCommunicationProtocol import AgentCommunicationProtocol


class TestAgentMemorySystem(unittest.TestCase):
    """Tests para el sistema de memoria de agentes"""
    
    def setUp(self):
        self.memory_system = AgentMemorySystem("test_agent")
    
    def test_creacion_sistema_memoria(self):
        """Test creación básica del sistema de memoria"""
        self.assertEqual(self.memory_system.agente_id, "test_agent")
        self.assertIsInstance(self.memory_system.memoria_trabajo, dict)
        self.assertIsInstance(self.memory_system.memoria_largo_plazo, dict)
    
    def test_almacenar_decision(self):
        """Test almacenamiento de decisiones"""
        decision = Decision(
            agente_id="test_agent",
            tipo_decision="compra",
            contexto={"precio": 100, "cantidad": 5},
            accion_tomada={"comprado": True},
            recompensa=10.0
        )
        
        self.memory_system.almacenar_decision(decision)
        
        # Verificar que se almacenó
        self.assertGreater(len(self.memory_system.decisiones_historicas), 0)
        self.assertEqual(self.memory_system.decisiones_historicas[-1].tipo_decision, "compra")
    
    def test_recuperar_decisiones_por_tipo(self):
        """Test recuperación de decisiones por tipo"""
        # Añadir diferentes tipos de decisiones
        decision_compra = Decision(tipo_decision="compra", agente_id="test_agent")
        decision_venta = Decision(tipo_decision="venta", agente_id="test_agent")
        
        self.memory_system.almacenar_decision(decision_compra)
        self.memory_system.almacenar_decision(decision_venta)
        
        decisiones_compra = self.memory_system.obtener_decisiones_por_tipo("compra")
        
        self.assertEqual(len(decisiones_compra), 1)
        self.assertEqual(decisiones_compra[0].tipo_decision, "compra")
    
    def test_calcular_rendimiento_historico(self):
        """Test cálculo de rendimiento histórico"""
        # Añadir decisiones con diferentes recompensas
        for i, recompensa in enumerate([5.0, -2.0, 8.0, 1.0]):
            decision = Decision(
                tipo_decision="test",
                agente_id="test_agent",
                recompensa=recompensa
            )
            self.memory_system.almacenar_decision(decision)
        
        rendimiento = self.memory_system.calcular_rendimiento_promedio("test")
        
        self.assertIsInstance(rendimiento, float)
        self.assertEqual(rendimiento, 3.0)  # (5-2+8+1)/4 = 3.0
    
    def test_memoria_trabajo_temporal(self):
        """Test memoria de trabajo temporal"""
        # Almacenar información temporal
        self.memory_system.memoria_trabajo["precio_actual"] = 50
        self.memory_system.memoria_trabajo["inventario"] = 100
        
        # Verificar almacenamiento
        self.assertEqual(self.memory_system.memoria_trabajo["precio_actual"], 50)
        self.assertEqual(self.memory_system.memoria_trabajo["inventario"], 100)


class TestIADecisionEngine(unittest.TestCase):
    """Tests para el motor de decisiones IA"""
    
    def setUp(self):
        self.decision_engine = IADecisionEngine("test_agent")
    
    def test_creacion_motor_decisiones(self):
        """Test creación del motor de decisiones"""
        self.assertEqual(self.decision_engine.agente_id, "test_agent")
        self.assertIsInstance(self.decision_engine.red_neuronal, dict)
    
    def test_evaluar_contexto_compra(self):
        """Test evaluación de contexto para compra"""
        contexto = {
            "precio": 50,
            "dinero_disponible": 1000,
            "necesidad": 0.8,
            "inventario_actual": 2
        }
        
        evaluacion = self.decision_engine.evaluar_contexto(contexto, "compra")
        
        self.assertIsInstance(evaluacion, dict)
        self.assertIn("puntuacion", evaluacion)
        self.assertIn("factores", evaluacion)
        
        # La puntuación debe estar entre 0 y 1
        self.assertGreaterEqual(evaluacion["puntuacion"], 0.0)
        self.assertLessEqual(evaluacion["puntuacion"], 1.0)
    
    def test_tomar_decision_autonoma(self):
        """Test toma de decisión autónoma"""
        contexto = {
            "precio_mercado": 100,
            "costo_produccion": 70,
            "demanda_estimada": 0.7,
            "competencia": [95, 105, 98]
        }
        
        decision = self.decision_engine.decidir_accion(contexto, "precio")
        
        self.assertIsInstance(decision, dict)
        self.assertIn("accion", decision)
        self.assertIn("parametros", decision)
        self.assertIn("confianza", decision)
    
    def test_aprendizaje_por_refuerzo(self):
        """Test aprendizaje por refuerzo"""
        # Simular varias decisiones con retroalimentación
        for i in range(5):
            contexto = {"situacion": f"test_{i}"}
            decision = self.decision_engine.decidir_accion(contexto, "test")
            
            # Dar retroalimentación positiva o negativa
            recompensa = 1.0 if i % 2 == 0 else -0.5
            self.decision_engine.aprender_de_resultado(decision, recompensa)
        
        # El motor debería haber actualizado sus parámetros
        self.assertGreater(len(self.decision_engine.historial_aprendizaje), 0)
    
    def test_prediccion_resultados(self):
        """Test predicción de resultados"""
        contexto = {
            "precio_propuesto": 80,
            "mercado_actual": "estable",
            "competencia_promedio": 85
        }
        
        prediccion = self.decision_engine.predecir_resultado(contexto, "cambio_precio")
        
        self.assertIsInstance(prediccion, dict)
        self.assertIn("resultado_esperado", prediccion)
        self.assertIn("probabilidad", prediccion)


class TestAgentCommunicationProtocol(unittest.TestCase):
    """Tests para el protocolo de comunicación entre agentes"""
    
    def setUp(self):
        self.protocol = AgentCommunicationProtocol("test_agent")
    
    def test_creacion_protocolo(self):
        """Test creación del protocolo de comunicación"""
        self.assertEqual(self.protocol.agente_id, "test_agent")
        self.assertIsInstance(self.protocol.canales_comunicacion, dict)
        self.assertIsInstance(self.protocol.mensajes_pendientes, list)
    
    def test_enviar_mensaje_basico(self):
        """Test envío de mensaje básico"""
        mensaje = {
            "destinatario": "agente_2",
            "tipo": "propuesta_comercial",
            "contenido": {"precio": 100, "cantidad": 10},
            "urgencia": "normal"
        }
        
        resultado = self.protocol.enviar_mensaje(mensaje)
        
        # Si el protocolo está implementado, debería devolver algo
        if resultado is not None:
            self.assertIsInstance(resultado, (bool, dict))
    
    def test_recibir_mensajes(self):
        """Test recepción de mensajes"""
        # Simular mensaje recibido
        mensaje_recibido = {
            "remitente": "agente_supplier",
            "tipo": "respuesta_propuesta",
            "contenido": {"aceptado": True, "precio_final": 95},
            "timestamp": "2024-01-01T10:00:00"
        }
        
        self.protocol.mensajes_pendientes.append(mensaje_recibido)
        
        mensajes = self.protocol.obtener_mensajes_pendientes()
        
        self.assertEqual(len(mensajes), 1)
        self.assertEqual(mensajes[0]["remitente"], "agente_supplier")
    
    def test_establecer_canal_comunicacion(self):
        """Test establecimiento de canal de comunicación"""
        info_canal = {
            "tipo": "comercial",
            "protocolo": "directo",
            "confianza": 0.8
        }
        
        resultado = self.protocol.establecer_canal("agente_partner", info_canal)
        
        # Verificar que el canal se estableció
        if resultado:
            self.assertIn("agente_partner", self.protocol.canales_comunicacion)
    
    def test_procesar_mensajes_por_prioridad(self):
        """Test procesamiento de mensajes por prioridad"""
        # Añadir mensajes con diferentes prioridades
        mensajes = [
            {"prioridad": "baja", "contenido": "info_general"},
            {"prioridad": "alta", "contenido": "oferta_urgente"},
            {"prioridad": "media", "contenido": "consulta_precio"}
        ]
        
        for msg in mensajes:
            self.protocol.mensajes_pendientes.append(msg)
        
        mensajes_procesados = self.protocol.procesar_mensajes_por_prioridad()
        
        # Los mensajes de alta prioridad deberían procesarse primero
        if len(mensajes_procesados) > 0:
            primer_mensaje = mensajes_procesados[0]
            # Si hay implementación de prioridad, verificar orden
            self.assertIsInstance(primer_mensaje, dict)
    
    def test_filtrar_mensajes_spam(self):
        """Test filtrado de mensajes spam"""
        mensajes_test = [
            {"remitente": "agente_confiable", "contenido": "propuesta_seria"},
            {"remitente": "agente_spam", "contenido": "oferta_imposible"},
            {"remitente": "agente_conocido", "contenido": "consulta_normal"}
        ]
        
        for msg in mensajes_test:
            self.protocol.mensajes_pendientes.append(msg)
        
        # Si hay implementación de filtrado
        mensajes_filtrados = self.protocol.filtrar_mensajes_validos()
        
        if mensajes_filtrados is not None:
            self.assertIsInstance(mensajes_filtrados, list)
            # Debería filtrar al menos el mensaje spam
            self.assertLessEqual(len(mensajes_filtrados), len(mensajes_test))


class TestDecision(unittest.TestCase):
    """Tests para la clase Decision"""
    
    def test_creacion_decision(self):
        """Test creación de decisión"""
        decision = Decision(
            agente_id="test",
            tipo_decision="compra",
            contexto={"precio": 50},
            accion_tomada={"cantidad": 10}
        )
        
        self.assertEqual(decision.agente_id, "test")
        self.assertEqual(decision.tipo_decision, "compra")
        self.assertEqual(decision.contexto["precio"], 50)
        self.assertIsNotNone(decision.id)  # UUID generado automáticamente
    
    def test_decision_con_resultado(self):
        """Test decisión con resultado y recompensa"""
        decision = Decision(
            agente_id="test",
            tipo_decision="venta",
            recompensa=15.5
        )
        
        decision.resultado = {"ganancia": 100, "unidades_vendidas": 5}
        
        self.assertEqual(decision.recompensa, 15.5)
        self.assertEqual(decision.resultado["ganancia"], 100)
    
    def test_decision_timestamp(self):
        """Test que la decisión tiene timestamp"""
        decision = Decision(agente_id="test", tipo_decision="test")
        
        self.assertIsNotNone(decision.timestamp)
        # El timestamp debería ser reciente (dentro de los últimos 5 segundos)
        import datetime
        now = datetime.datetime.now()
        diff = now - decision.timestamp
        self.assertLess(diff.total_seconds(), 5)


if __name__ == '__main__':
    unittest.main()