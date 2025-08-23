"""
Protocolo de Comunicación entre Agentes IA
==========================================

Este módulo implementa un sistema avanzado de comunicación que permite
a los agentes IA intercambiar información, negociar, formar alianzas
y coordinarse en el mercado.
"""

import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from collections import deque, defaultdict
from enum import Enum
from datetime import datetime, timedelta
import threading
import queue
import numpy as np


class TipoMensaje(Enum):
    """Tipos de mensajes entre agentes"""
    INFORMACION_MERCADO = "info_mercado"
    PROPUESTA_PRECIO = "propuesta_precio"
    NEGOCIACION = "negociacion"
    ACEPTAR_OFERTA = "aceptar_oferta"
    RECHAZAR_OFERTA = "rechazar_oferta"
    CONTRA_OFERTA = "contra_oferta"
    SOLICITUD_ALIANZA = "solicitud_alianza"
    CONFIRMAR_ALIANZA = "confirmar_alianza"
    DISOLVER_ALIANZA = "disolver_alianza"
    SEÑAL_MERCADO = "señal_mercado"
    ALERTA_RIESGO = "alerta_riesgo"
    COMPARTIR_CONOCIMIENTO = "compartir_conocimiento"
    COORDINACION_COMPRA = "coordinacion_compra"
    ADVERTENCIA_COMPETENCIA = "advertencia_competencia"


class PrioridadMensaje(Enum):
    """Prioridad de los mensajes"""
    BAJA = 1
    NORMAL = 2
    ALTA = 3
    CRITICA = 4


@dataclass
class Mensaje:
    """Representa un mensaje entre agentes"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    remitente: str = ""
    destinatario: str = ""  # Puede ser específico o "ALL" para broadcast
    tipo: TipoMensaje = TipoMensaje.INFORMACION_MERCADO
    contenido: Dict[str, Any] = field(default_factory=dict)
    prioridad: PrioridadMensaje = PrioridadMensaje.NORMAL
    timestamp: datetime = field(default_factory=datetime.now)
    expiracion: Optional[datetime] = None
    requiere_respuesta: bool = False
    respuesta_a: Optional[str] = None
    canal: str = "general"


@dataclass
class Negociacion:
    """Representa una negociación activa entre agentes"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    participantes: List[str] = field(default_factory=list)
    bien: str = ""
    cantidad: float = 0
    precio_inicial: float = 0
    precio_actual: float = 0
    precio_minimo: float = 0
    precio_maximo: float = 0
    rondas_negociacion: int = 0
    max_rondas: int = 10
    iniciada_en: datetime = field(default_factory=datetime.now)
    estado: str = "activa"  # 'activa', 'cerrada', 'cancelada'
    historial_ofertas: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Alianza:
    """Representa una alianza entre agentes"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str = ""
    miembros: List[str] = field(default_factory=list)
    tipo: str = ""  # 'compra_conjunta', 'defensa_precios', 'informacion', etc.
    objetivo: str = ""
    duracion_dias: int = 30
    creada_en: datetime = field(default_factory=datetime.now)
    activa: bool = True
    beneficios_compartidos: Dict[str, float] = field(default_factory=dict)
    reglas: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SeñalMercado:
    """Señal de mercado emitida por agentes"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    emisor: str = ""
    tipo_señal: str = ""  # 'precio_alto', 'demanda_baja', 'oportunidad', etc.
    bien: str = ""
    intensidad: float = 0.0  # 0.0 a 1.0
    confianza: float = 0.0   # 0.0 a 1.0
    datos_soporte: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    alcance: str = "local"  # 'local', 'sectorial', 'global'


class AgentCommunicationProtocol:
    """
    Protocolo principal de comunicación entre agentes IA
    """
    
    def __init__(self, agente_id: str):
        self.agente_id = agente_id
        
        # Colas de mensajes
        self.mensajes_entrantes = queue.PriorityQueue()
        self.mensajes_salientes = queue.Queue()
        self.mensajes_broadcast = deque(maxlen=1000)
        # Alias de compatibilidad para tests (lista simple)
        self.mensajes_pendientes = []
        # Alias para canales
        self.canales_comunicacion = {}
            
        # Estado de comunicaciones
        self.negociaciones_activas = {}
        self.alianzas_activas = {}
        self.contactos_conocidos = []
        self.reputacion_agentes = {}
            
        # Señales de mercado
        self.señales_mercado = deque(maxlen=500)
        self.suscripciones_señales = defaultdict(list)
            
        # Configuración
        self.max_negociaciones_simultaneas = 5
        self.max_alianzas_simultaneas = 3
        self.timeout_respuesta = 300  # 5 minutos
        
        # Métricas
        self.mensajes_enviados = 0
        self.mensajes_recibidos = 0
        self.negociaciones_exitosas = 0
        self.alianzas_formadas = 0
        
        # Handlers de mensajes
        self.handlers_mensaje = {
                TipoMensaje.PROPUESTA_PRECIO: self._handle_propuesta_precio,
                TipoMensaje.NEGOCIACION: self._handle_negociacion,
                TipoMensaje.SOLICITUD_ALIANZA: self._handle_solicitud_alianza,
                TipoMensaje.SEÑAL_MERCADO: self._handle_señal_mercado,
                TipoMensaje.INFORMACION_MERCADO: self._handle_informacion_mercado,
                TipoMensaje.COORDINACION_COMPRA: self._handle_coordinacion_compra
            }
            
        # Hilo de procesamiento de mensajes
        self.procesando = True
        self.hilo_procesamiento = threading.Thread(target=self._procesar_mensajes)
        self.hilo_procesamiento.daemon = True
        self.hilo_procesamiento.start()

    # --- API mínima requerida por tests unitarios ---
    def establecer_canal(self, agente_id: str, info_canal: Dict[str, Any]) -> bool:
        """Crea o actualiza un canal de comunicación simple con un agente."""
        self.canales_comunicacion[agente_id] = info_canal.copy()
        return True

    def enviar_mensaje(self, *args, **kwargs):
        """Compatibilidad: acepta un dict o la firma avanzada (destinatario, tipo, contenido, prioridad, requiere_respuesta, canal)."""
        # Caso 1: un solo dict
        if len(args) == 1 and isinstance(args[0], dict):
            msg = args[0].copy()
            msg.setdefault("timestamp", datetime.now().isoformat())
            self.mensajes_pendientes.append(msg)
            self.mensajes_enviados += 1
            return True
        
        # Caso 2: firma avanzada
        destinatario = args[0] if len(args) > 0 else kwargs.get('destinatario')
        tipo = args[1] if len(args) > 1 else kwargs.get('tipo', TipoMensaje.INFORMACION_MERCADO)
        contenido = args[2] if len(args) > 2 else kwargs.get('contenido', {})
        prioridad = args[3] if len(args) > 3 else kwargs.get('prioridad', PrioridadMensaje.NORMAL)
        requiere_respuesta = args[4] if len(args) > 4 else kwargs.get('requiere_respuesta', False)
        canal = args[5] if len(args) > 5 else kwargs.get('canal', 'general')
        
        # Construcción del mensaje avanzado
        mensaje = Mensaje(
            remitente=self.agente_id,
            destinatario=destinatario,
            tipo=tipo,
            contenido=contenido,
            prioridad=prioridad,
            requiere_respuesta=requiere_respuesta,
            canal=canal
        )
        
        # Configurar expiración basada en tipo de mensaje
        if tipo == TipoMensaje.NEGOCIACION:
            mensaje.expiracion = datetime.now() + timedelta(minutes=30)
        elif tipo == TipoMensaje.SEÑAL_MERCADO:
            mensaje.expiracion = datetime.now() + timedelta(minutes=5)
        
        self.mensajes_salientes.put(mensaje)
        self.mensajes_enviados += 1
        
        return mensaje.id

    def obtener_mensajes_pendientes(self) -> List[Dict[str, Any]]:
        """Devuelve y limpia la lista de mensajes pendientes simple."""
        msgs = list(self.mensajes_pendientes)
        self.mensajes_pendientes.clear()
        return msgs

    def procesar_mensajes_por_prioridad(self) -> List[Dict[str, Any]]:
        """Ordena mensajes_pendientes por prioridad: alta > media > baja."""
        prioridad_map = {"critica": 3, "alta": 2, "media": 1, "baja": 0}
        ordenados = sorted(self.mensajes_pendientes, key=lambda m: prioridad_map.get(m.get("prioridad", "media"), 1), reverse=True)
        self.mensajes_pendientes = []
        return ordenados

    def filtrar_mensajes_validos(self) -> List[Dict[str, Any]]:
        """Filtra mensajes que parezcan spam de forma simple."""
        def es_spam(m: Dict[str, Any]) -> bool:
            remitente = str(m.get("remitente", ""))
            contenido = str(m.get("contenido", ""))
            return "spam" in remitente or "imposible" in contenido.lower()
        validos = [m for m in self.mensajes_pendientes if not es_spam(m)]
        self.mensajes_pendientes = validos.copy()
        return validos
    
    # (El método enviar_mensaje avanzado ha sido unificado en la versión con *args)
    
    def enviar_señal_mercado(self, tipo_señal: str, bien: str, intensidad: float,
                            datos_soporte: Dict[str, Any] = None, alcance: str = "local") -> str:
        """Envía una señal de mercado a otros agentes"""
        señal = SeñalMercado(
            emisor=self.agente_id,
            tipo_señal=tipo_señal,
            bien=bien,
            intensidad=intensidad,
            confianza=self._calcular_confianza_señal(datos_soporte or {}),
            datos_soporte=datos_soporte or {},
            alcance=alcance
        )
        
        self.señales_mercado.append(señal)
        
        # Notificar a agentes suscritos
        mensaje_señal = {
            'señal': {
                'id': señal.id,
                'tipo_señal': señal.tipo_señal,
                'bien': señal.bien,
                'intensidad': señal.intensidad,
                'confianza': señal.confianza,
                'datos_soporte': señal.datos_soporte,
                'alcance': señal.alcance
            }
        }
        
        return self.enviar_mensaje(
            "ALL", 
            TipoMensaje.SEÑAL_MERCADO, 
            mensaje_señal,
            prioridad=PrioridadMensaje.ALTA,
            canal="señales_mercado"
        )
    
    def negociar_precio(self, agente_objetivo: str, bien: str, cantidad: float,
                       precio_inicial: float, precio_minimo: float, precio_maximo: float) -> str:
        """Inicia una negociación de precio con otro agente"""
        if len(self.negociaciones_activas) >= self.max_negociaciones_simultaneas:
            return None
        
        negociacion = Negociacion(
            participantes=[self.agente_id, agente_objetivo],
            bien=bien,
            cantidad=cantidad,
            precio_inicial=precio_inicial,
            precio_actual=precio_inicial,
            precio_minimo=precio_minimo,
            precio_maximo=precio_maximo
        )
        
        self.negociaciones_activas[negociacion.id] = negociacion
        
        # Enviar propuesta inicial
        contenido_negociacion = {
            'negociacion_id': negociacion.id,
            'bien': bien,
            'cantidad': cantidad,
            'precio_propuesto': precio_inicial,
            'tipo_propuesta': 'inicial'
        }
        
        self.enviar_mensaje(
            agente_objetivo,
            TipoMensaje.NEGOCIACION,
            contenido_negociacion,
            prioridad=PrioridadMensaje.ALTA,
            requiere_respuesta=True
        )
        
        return negociacion.id
    
    def formar_alianza_temporal(self, agentes_objetivo: List[str], tipo_alianza: str,
                               objetivo: str, duracion_dias: int = 30) -> str:
        """Forma una alianza temporal con otros agentes"""
        if len(self.alianzas_activas) >= self.max_alianzas_simultaneas:
            return None
        
        alianza = Alianza(
            nombre=f"Alianza_{tipo_alianza}_{int(time.time())}",
            miembros=[self.agente_id] + agentes_objetivo,
            tipo=tipo_alianza,
            objetivo=objetivo,
            duracion_dias=duracion_dias
        )
        
        # Definir reglas básicas según tipo de alianza
        if tipo_alianza == "compra_conjunta":
            alianza.reglas = {
                'reparto_beneficios': 'proporcional',
                'decision_compra': 'mayoria',
                'transparencia_precios': True
            }
        elif tipo_alianza == "defensa_precios":
            alianza.reglas = {
                'precio_minimo_acordado': 0,
                'notificacion_cambios': True,
                'penalizacion_dumping': 0.1
            }
        
        self.alianzas_activas[alianza.id] = alianza
        
        # Enviar solicitudes de alianza
        contenido_alianza = {
            'alianza_id': alianza.id,
            'tipo': tipo_alianza,
            'objetivo': objetivo,
            'duracion_dias': duracion_dias,
            'reglas': alianza.reglas,
            'miembros_propuestos': alianza.miembros
        }
        
        for agente in agentes_objetivo:
            self.enviar_mensaje(
                agente,
                TipoMensaje.SOLICITUD_ALIANZA,
                contenido_alianza,
                prioridad=PrioridadMensaje.ALTA,
                requiere_respuesta=True
            )
        
        return alianza.id
    
    def recibir_mensaje(self, mensaje: Mensaje):
        """Recibe un mensaje de otro agente"""
        # Verificar si el mensaje no ha expirado
        if mensaje.expiracion and datetime.now() > mensaje.expiracion:
            return
        
        # Agregar a cola con prioridad
        prioridad_num = mensaje.prioridad.value
        self.mensajes_entrantes.put((prioridad_num, mensaje.timestamp, mensaje))
        self.mensajes_recibidos += 1
        
        # Actualizar reputación del remitente
        if mensaje.remitente in self.reputacion_agentes:
            # Incrementar ligeramente por comunicación activa
            self.reputacion_agentes[mensaje.remitente] += 0.01
        else:
            self.reputacion_agentes[mensaje.remitente] = 0.5  # Neutral inicial
        
        # Agregar a contactos conocidos
        if mensaje.remitente not in self.contactos_conocidos:
            self.contactos_conocidos.append(mensaje.remitente)
    
    def _procesar_mensajes(self):
        """Hilo que procesa mensajes entrantes"""
        while self.procesando:
            try:
                # Procesar mensaje con timeout
                prioridad, timestamp, mensaje = self.mensajes_entrantes.get(timeout=1.0)
                
                # Procesar según tipo de mensaje
                if mensaje.tipo in self.handlers_mensaje:
                    try:
                        self.handlers_mensaje[mensaje.tipo](mensaje)
                    except Exception as e:
                        print(f"Error procesando mensaje {mensaje.tipo}: {e}")
                
                self.mensajes_entrantes.task_done()
                
            except queue.Empty:
                # Timeout - revisar negociaciones y alianzas expiradas
                self._limpiar_comunicaciones_expiradas()
                continue
            except Exception as e:
                print(f"Error en procesamiento de mensajes: {e}")
    
    def _handle_propuesta_precio(self, mensaje: Mensaje):
        """Maneja propuestas de precio"""
        contenido = mensaje.contenido
        precio_propuesto = contenido.get('precio_propuesto', 0)
        bien = contenido.get('bien', '')
        cantidad = contenido.get('cantidad', 0)
        
        # Evaluar propuesta usando IA del agente
        decision_respuesta = self._evaluar_propuesta_precio(
            mensaje.remitente, bien, cantidad, precio_propuesto
        )
        
        if decision_respuesta['aceptar']:
            self.enviar_mensaje(
                mensaje.remitente,
                TipoMensaje.ACEPTAR_OFERTA,
                {
                    'propuesta_original': mensaje.id,
                    'precio_aceptado': precio_propuesto,
                    'bien': bien,
                    'cantidad': cantidad
                },
                prioridad=PrioridadMensaje.ALTA
            )
        elif decision_respuesta['contra_oferta']:
            self.enviar_mensaje(
                mensaje.remitente,
                TipoMensaje.CONTRA_OFERTA,
                {
                    'propuesta_original': mensaje.id,
                    'precio_propuesto': decision_respuesta['nuevo_precio'],
                    'bien': bien,
                    'cantidad': cantidad,
                    'razon': decision_respuesta.get('razon', '')
                },
                prioridad=PrioridadMensaje.ALTA
            )
        else:
            self.enviar_mensaje(
                mensaje.remitente,
                TipoMensaje.RECHAZAR_OFERTA,
                {
                    'propuesta_original': mensaje.id,
                    'razon': decision_respuesta.get('razon', 'No aceptable')
                },
                prioridad=PrioridadMensaje.NORMAL
            )
    
    def _handle_negociacion(self, mensaje: Mensaje):
        """Maneja mensajes de negociación"""
        contenido = mensaje.contenido
        negociacion_id = contenido.get('negociacion_id')
        
        if negociacion_id and negociacion_id in self.negociaciones_activas:
            negociacion = self.negociaciones_activas[negociacion_id]
            negociacion.rondas_negociacion += 1
            
            # Registrar oferta en historial
            oferta = {
                'remitente': mensaje.remitente,
                'precio': contenido.get('precio_propuesto'),
                'timestamp': mensaje.timestamp,
                'tipo': contenido.get('tipo_propuesta', 'normal')
            }
            negociacion.historial_ofertas.append(oferta)
            
            # Evaluar si continuar negociación
            if negociacion.rondas_negociacion >= negociacion.max_rondas:
                # Cerrar negociación por límite de rondas
                negociacion.estado = "cancelada"
                self._enviar_cierre_negociacion(negociacion_id, "limite_rondas")
            else:
                # Continuar negociación con nueva propuesta
                respuesta_negociacion = self._generar_respuesta_negociacion(negociacion, contenido)
                if respuesta_negociacion:
                    self.enviar_mensaje(
                        mensaje.remitente,
                        TipoMensaje.NEGOCIACION,
                        respuesta_negociacion,
                        prioridad=PrioridadMensaje.ALTA
                    )
    
    def _handle_solicitud_alianza(self, mensaje: Mensaje):
        """Maneja solicitudes de alianza"""
        contenido = mensaje.contenido
        alianza_id = contenido.get('alianza_id')
        tipo_alianza = contenido.get('tipo')
        objetivo = contenido.get('objetivo')
        
        # Evaluar si aceptar la alianza
        decision_alianza = self._evaluar_solicitud_alianza(
            mensaje.remitente, tipo_alianza, objetivo, contenido
        )
        
        if decision_alianza['aceptar']:
            # Crear alianza local
            alianza = Alianza(
                id=alianza_id,
                nombre=contenido.get('nombre', f"Alianza_{tipo_alianza}"),
                miembros=contenido.get('miembros_propuestos', []),
                tipo=tipo_alianza,
                objetivo=objetivo,
                duracion_dias=contenido.get('duracion_dias', 30),
                reglas=contenido.get('reglas', {})
            )
            self.alianzas_activas[alianza_id] = alianza
            self.alianzas_formadas += 1
            
            # Confirmar alianza
            self.enviar_mensaje(
                mensaje.remitente,
                TipoMensaje.CONFIRMAR_ALIANZA,
                {
                    'alianza_id': alianza_id,
                    'aceptada': True,
                    'condiciones_adicionales': decision_alianza.get('condiciones', {})
                },
                prioridad=PrioridadMensaje.ALTA
            )
        else:
            self.enviar_mensaje(
                mensaje.remitente,
                TipoMensaje.CONFIRMAR_ALIANZA,
                {
                    'alianza_id': alianza_id,
                    'aceptada': False,
                    'razon': decision_alianza.get('razon', 'No beneficiosa')
                },
                prioridad=PrioridadMensaje.NORMAL
            )
    
    def _handle_señal_mercado(self, mensaje: Mensaje):
        """Maneja señales de mercado"""
        señal_data = mensaje.contenido.get('señal', {})
        
        # Crear objeto señal
        señal = SeñalMercado(
            id=señal_data.get('id'),
            emisor=mensaje.remitente,
            tipo_señal=señal_data.get('tipo_señal'),
            bien=señal_data.get('bien'),
            intensidad=señal_data.get('intensidad', 0),
            confianza=señal_data.get('confianza', 0),
            datos_soporte=señal_data.get('datos_soporte', {}),
            alcance=señal_data.get('alcance', 'local')
        )
        
        # Validar señal basándose en reputación del emisor
        reputacion_emisor = self.reputacion_agentes.get(mensaje.remitente, 0.5)
        señal.confianza *= reputacion_emisor
        
        # Agregar a historial de señales
        self.señales_mercado.append(señal)
        
        # Procesar señal para decisiones propias
        self._procesar_señal_mercado(señal)
    
    def _handle_informacion_mercado(self, mensaje: Mensaje):
        """Maneja información general del mercado"""
        info = mensaje.contenido
        
        # Actualizar conocimiento del mercado basándose en información recibida
        # (Esto se integraría con el sistema de memoria del agente)
        pass
    
    def _handle_coordinacion_compra(self, mensaje: Mensaje):
        """Maneja propuestas de coordinación de compra"""
        contenido = mensaje.contenido
        bien = contenido.get('bien')
        cantidad_total = contenido.get('cantidad_total')
        precio_objetivo = contenido.get('precio_objetivo')
        participantes = contenido.get('participantes', [])
        
        # Evaluar participación en compra coordinada
        decision = self._evaluar_coordinacion_compra(bien, cantidad_total, precio_objetivo, participantes)
        
        if decision['participar']:
            self.enviar_mensaje(
                mensaje.remitente,
                TipoMensaje.COORDINACION_COMPRA,
                {
                    'participar': True,
                    'cantidad_comprometida': decision['cantidad'],
                    'condiciones': decision.get('condiciones', {})
                },
                prioridad=PrioridadMensaje.ALTA
            )
    
    def _evaluar_propuesta_precio(self, remitente: str, bien: str, cantidad: float, 
                                precio: float) -> Dict[str, Any]:
        """Evalúa una propuesta de precio (placeholder - se integraría con IA del agente)"""
        # Esta función sería implementada por cada tipo de agente específico
        # Aquí una lógica básica de placeholder
        
        # Evaluar basándose en reputación del remitente
        reputacion = self.reputacion_agentes.get(remitente, 0.5)
        
        if precio > 100 and reputacion < 0.3:  # Precio alto, reputación baja
            return {'aceptar': False, 'contra_oferta': True, 'nuevo_precio': precio * 0.8}
        elif precio < 50:  # Precio bajo
            return {'aceptar': True}
        else:
            return {'aceptar': False, 'contra_oferta': False, 'razon': 'Precio no competitivo'}
    
    def _evaluar_solicitud_alianza(self, remitente: str, tipo: str, objetivo: str,
                                 contenido: Dict[str, Any]) -> Dict[str, Any]:
        """Evalúa una solicitud de alianza"""
        reputacion = self.reputacion_agentes.get(remitente, 0.5)
        
        # Evaluar beneficios potenciales
        if tipo == "compra_conjunta" and reputacion > 0.6:
            return {'aceptar': True, 'condiciones': {'transparencia_total': True}}
        elif tipo == "informacion" and reputacion > 0.4:
            return {'aceptar': True}
        else:
            return {'aceptar': False, 'razon': 'No alineada con estrategia actual'}
    
    def _evaluar_coordinacion_compra(self, bien: str, cantidad: float, precio: float,
                                   participantes: List[str]) -> Dict[str, Any]:
        """Evalúa participación en compra coordinada"""
        # Evaluar si el precio es atractivo y los participantes son confiables
        reputacion_promedio = np.mean([
            self.reputacion_agentes.get(p, 0.5) for p in participantes
        ]) if participantes else 0.5
        
        if precio < 50 and reputacion_promedio > 0.5:
            return {'participar': True, 'cantidad': cantidad / len(participantes)}
        else:
            return {'participar': False}
    
    def _calcular_confianza_señal(self, datos_soporte: Dict[str, Any]) -> float:
        """Calcula el nivel de confianza de una señal basándose en datos de soporte"""
        confianza_base = 0.5
        
        # Incrementar confianza basándose en cantidad de datos
        if 'observaciones' in datos_soporte:
            confianza_base += min(0.3, len(datos_soporte['observaciones']) * 0.05)
        
        if 'fuentes_multiples' in datos_soporte:
            confianza_base += 0.2
        
        return min(1.0, confianza_base)
    
    def _procesar_señal_mercado(self, señal: SeñalMercado):
        """Procesa una señal de mercado para tomar decisiones"""
        # Esta lógica se integraría con el motor de decisiones IA del agente
        if señal.tipo_señal == "precio_alto" and señal.confianza > 0.7:
            # Considerar venta si tenemos el bien
            pass
        elif señal.tipo_señal == "demanda_baja" and señal.confianza > 0.6:
            # Considerar reducir producción
            pass
    
    def _generar_respuesta_negociacion(self, negociacion: Negociacion, 
                                     contenido: Dict[str, Any]) -> Dict[str, Any]:
        """Genera una respuesta a una negociación"""
        precio_propuesto = contenido.get('precio_propuesto', 0)
        precio_actual = negociacion.precio_actual
        
        # Lógica simple de negociación - moverse hacia el precio medio
        if precio_propuesto > precio_actual:
            nuevo_precio = (precio_propuesto + precio_actual) / 2
        else:
            nuevo_precio = precio_actual * 0.95  # Reducir ligeramente
        
        # Verificar límites
        nuevo_precio = max(negociacion.precio_minimo, 
                          min(negociacion.precio_maximo, nuevo_precio))
        
        negociacion.precio_actual = nuevo_precio
        
        return {
            'negociacion_id': negociacion.id,
            'precio_propuesto': nuevo_precio,
            'tipo_propuesta': 'contra_oferta',
            'bien': negociacion.bien,
            'cantidad': negociacion.cantidad
        }
    
    def _enviar_cierre_negociacion(self, negociacion_id: str, razon: str):
        """Envía mensaje de cierre de negociación"""
        if negociacion_id in self.negociaciones_activas:
            negociacion = self.negociaciones_activas[negociacion_id]
            for participante in negociacion.participantes:
                if participante != self.agente_id:
                    self.enviar_mensaje(
                        participante,
                        TipoMensaje.INFORMACION_MERCADO,
                        {
                            'tipo': 'cierre_negociacion',
                            'negociacion_id': negociacion_id,
                            'razon': razon,
                            'estado_final': negociacion.estado
                        }
                    )
    
    def _limpiar_comunicaciones_expiradas(self):
        """Limpia negociaciones y alianzas expiradas"""
        ahora = datetime.now()
        
        # Limpiar negociaciones expiradas (más de 1 hora)
        negociaciones_expiradas = []
        for neg_id, negociacion in self.negociaciones_activas.items():
            if (ahora - negociacion.iniciada_en).total_seconds() > 3600:
                negociaciones_expiradas.append(neg_id)
        
        for neg_id in negociaciones_expiradas:
            del self.negociaciones_activas[neg_id]
        
        # Limpiar alianzas expiradas
        alianzas_expiradas = []
        for alianza_id, alianza in self.alianzas_activas.items():
            if (ahora - alianza.creada_en).days > alianza.duracion_dias:
                alianzas_expiradas.append(alianza_id)
        
        for alianza_id in alianzas_expiradas:
            del self.alianzas_activas[alianza_id]
    
    def get_estadisticas_comunicacion(self) -> Dict[str, Any]:
        """Obtiene estadísticas de comunicación"""
        return {
            'agente_id': self.agente_id,
            'mensajes_enviados': self.mensajes_enviados,
            'mensajes_recibidos': self.mensajes_recibidos,
            'negociaciones_activas': len(self.negociaciones_activas),
            'negociaciones_exitosas': self.negociaciones_exitosas,
            'alianzas_activas': len(self.alianzas_activas),
            'alianzas_formadas': self.alianzas_formadas,
            'contactos_conocidos': len(self.contactos_conocidos),
            'señales_recientes': len(self.señales_mercado),
            'reputacion_promedio': (
                np.mean(list(self.reputacion_agentes.values())) 
                if self.reputacion_agentes else 0.5
            )
        }
    
    def finalizar(self):
        """Finaliza el protocolo de comunicación"""
        self.procesando = False
        if self.hilo_procesamiento.is_alive():
            self.hilo_procesamiento.join(timeout=1.0)
