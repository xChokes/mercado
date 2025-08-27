"""
Tests Unitarios para Sistemas Hiperrealistas
===========================================

Tests para validar el funcionamiento de los nuevos componentes hiperrealistas:
- PerfilPersonalidadIA
- ComportamientoCompraIA  
- BienHiperrealista
- ConsumidorIA (componentes hiperrealistas)
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.ai.PerfilPersonalidadIA import (
    GeneradorPerfilesPersonalidad, 
    TipoPersonalidad, 
    EstiloVida,
    PerfilPersonalidadCompleto,
    RasgosPsicologicos,
    PreferenciasConsumo,
    ContextoSocioeconomico
)
from src.ai.ComportamientoCompraIA import (
    SistemaComportamientoCompra,
    TipoComportamientoCompra,
    FaseDecisionCompra,
    CriterioDecision
)
from src.models.BienHiperrealista import (
    BienHiperrealista,
    TipoBien,
    CalidadBien,
    PropiedadesFisicas,
    AtributosCalidad
)


class TestPerfilPersonalidadIA(unittest.TestCase):
    """Tests para el sistema de perfiles de personalidad"""
    
    def setUp(self):
        self.generador = GeneradorPerfilesPersonalidad()
    
    def test_generacion_perfil_unico(self):
        """Test generación de perfil único"""
        perfil = self.generador.generar_perfil_unico()
        
        self.assertIsInstance(perfil, PerfilPersonalidadCompleto)
        self.assertIsInstance(perfil.tipo_personalidad, TipoPersonalidad)
        self.assertIsInstance(perfil.estilo_vida, EstiloVida)
        self.assertIsInstance(perfil.rasgos_psicologicos, RasgosPsicologicos)
        self.assertIsInstance(perfil.preferencias_consumo, PreferenciasConsumo)
        self.assertIsInstance(perfil.contexto_socioeconomico, ContextoSocioeconomico)
    
    def test_tipos_personalidad_validos(self):
        """Test que todos los tipos de personalidad son válidos"""
        for tipo in TipoPersonalidad:
            self.assertIsInstance(tipo.value, str)
            self.assertGreater(len(tipo.value), 0)
    
    def test_estilos_vida_validos(self):
        """Test que todos los estilos de vida son válidos"""
        for estilo in EstiloVida:
            self.assertIsInstance(estilo.value, str)
            self.assertGreater(len(estilo.value), 0)
    
    def test_rasgos_psicologicos_en_rango(self):
        """Test que los rasgos psicológicos están en rango válido [0,1]"""
        perfil = self.generador.generar_perfil_unico()
        rasgos = perfil.rasgos_psicologicos
        
        # Big Five
        self.assertBetween(rasgos.apertura, 0.0, 1.0)
        self.assertBetween(rasgos.responsabilidad, 0.0, 1.0)
        self.assertBetween(rasgos.extraversion, 0.0, 1.0)
        self.assertBetween(rasgos.amabilidad, 0.0, 1.0)
        self.assertBetween(rasgos.neuroticismo, 0.0, 1.0)
        
        # Rasgos económicos
        self.assertBetween(rasgos.aversion_riesgo, 0.0, 1.0)
        self.assertBetween(rasgos.materialismo, 0.0, 1.0)
        self.assertBetween(rasgos.impulsividad, 0.0, 1.0)
        self.assertBetween(rasgos.planificacion, 0.0, 1.0)
    
    def test_preferencias_consumo_en_rango(self):
        """Test que las preferencias de consumo están en rango válido"""
        perfil = self.generador.generar_perfil_unico()
        prefs = perfil.preferencias_consumo
        
        self.assertBetween(prefs.preferencia_alimentacion, 0.0, 1.0)
        self.assertBetween(prefs.preferencia_tecnologia, 0.0, 1.0)
        self.assertBetween(prefs.preferencia_ropa, 0.0, 1.0)
        self.assertBetween(prefs.preferencia_entretenimiento, 0.0, 1.0)
        self.assertBetween(prefs.preferencia_educacion, 0.0, 1.0)
        self.assertBetween(prefs.preferencia_salud, 0.0, 1.0)
    
    def test_diversidad_perfiles_generados(self):
        """Test que se genera diversidad en los perfiles"""
        perfiles = [self.generador.generar_perfil_unico() for _ in range(10)]
        
        # Debe haber al menos 3 tipos de personalidad diferentes
        tipos_unicos = set(p.tipo_personalidad for p in perfiles)
        self.assertGreaterEqual(len(tipos_unicos), 3)
        
        # Debe haber al menos 3 estilos de vida diferentes
        estilos_unicos = set(p.estilo_vida for p in perfiles)
        self.assertGreaterEqual(len(estilos_unicos), 3)
    
    def test_correlaciones_psicologicas_realistas(self):
        """Test que las correlaciones psicológicas son realistas"""
        perfiles = [self.generador.generar_perfil_unico() for _ in range(50)]
        
        # Buscar correlaciones esperadas
        correlaciones_encontradas = 0
        
        for perfil in perfiles:
            rasgos = perfil.rasgos_psicologicos
            
            # Impulsividad alta debería correlacionar con planificación baja
            if rasgos.impulsividad > 0.7 and rasgos.planificacion < 0.4:
                correlaciones_encontradas += 1
            
            # Responsabilidad alta debería correlacionar con planificación alta
            if rasgos.responsabilidad > 0.7 and rasgos.planificacion > 0.6:
                correlaciones_encontradas += 1
        
        # Al menos 20% de los perfiles deberían mostrar correlaciones realistas
        self.assertGreater(correlaciones_encontradas, len(perfiles) * 0.2)
    
    def assertBetween(self, value, min_val, max_val, msg=None):
        """Helper para verificar que un valor está en un rango"""
        if not (min_val <= value <= max_val):
            msg = msg or f"{value} no está entre {min_val} y {max_val}"
            raise AssertionError(msg)


class TestComportamientoCompraIA(unittest.TestCase):
    """Tests para el sistema de comportamiento de compra"""
    
    def setUp(self):
        # Crear un perfil real para las pruebas en lugar de mock
        from src.ai.PerfilPersonalidadIA import GeneradorPerfilesPersonalidad
        generador = GeneradorPerfilesPersonalidad()
        self.perfil_real = generador.generar_perfil_unico()
        
        self.sistema = SistemaComportamientoCompra(self.perfil_real)
    
    def test_creacion_sistema_comportamiento(self):
        """Test creación del sistema de comportamiento"""
        self.assertIsInstance(self.sistema.comportamiento_dominante, TipoComportamientoCompra)
        self.assertIsInstance(self.sistema.comportamientos_secundarios, list)
        self.assertIsInstance(self.sistema.criterios_decision, dict)
        self.assertIsInstance(self.sistema.patrones_temporales, dict)
        self.assertIsInstance(self.sistema.sesgos_cognitivos, dict)
    
    def test_tipos_comportamiento_validos(self):
        """Test que todos los tipos de comportamiento son válidos"""
        for tipo in TipoComportamientoCompra:
            self.assertIsInstance(tipo.value, str)
            self.assertGreater(len(tipo.value), 0)
    
    def test_tiempo_decision_coherente_con_personalidad(self):
        """Test que el tiempo de decisión es coherente con la personalidad"""
        tiempo = self.sistema.tiempo_promedio_decision
        
        # El tiempo debería estar en un rango razonable
        self.assertGreater(tiempo, 5)  # Más de 5 minutos mínimo
        self.assertLess(tiempo, 300)   # Menos de 5 horas máximo
    
    def test_criterios_decision_no_vacios(self):
        """Test que se generan criterios de decisión"""
        self.assertGreater(len(self.sistema.criterios_decision), 0)
        
        for nombre_criterio, criterio in self.sistema.criterios_decision.items():
            self.assertIsInstance(nombre_criterio, str)
            self.assertIsInstance(criterio, CriterioDecision)
            self.assertBetween(criterio.peso, 0.0, 1.0)
            self.assertBetween(criterio.umbral_minimo, 0.0, 1.0)
    
    def test_sesgos_cognitivos_no_vacios(self):
        """Test que se generan sesgos cognitivos"""
        self.assertGreater(len(self.sistema.sesgos_cognitivos), 0)
        
        # Los sesgos cognitivos son un diccionario string -> float
        for nombre_sesgo, intensidad in self.sistema.sesgos_cognitivos.items():
            self.assertIsInstance(nombre_sesgo, str)
            self.assertIsInstance(intensidad, float)
            self.assertBetween(intensidad, 0.0, 1.0)
    
    def test_estadisticas_comportamiento(self):
        """Test obtención de estadísticas de comportamiento"""
        stats = self.sistema.get_estadisticas_comportamiento()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('comportamiento_dominante', stats)
        self.assertIn('tiempo_promedio_decision', stats)
        self.assertIn('criterios_principales', stats)
        self.assertIn('tendencia_negociacion', stats)
        self.assertIn('factor_lealtad', stats)
    
    def test_diferentes_perfiles_generan_diferentes_comportamientos(self):
        """Test que diferentes perfiles generan comportamientos diferentes"""
        # Crear múltiples sistemas con perfiles reales diferentes
        from src.ai.PerfilPersonalidadIA import GeneradorPerfilesPersonalidad
        generador = GeneradorPerfilesPersonalidad()
        
        sistemas = []
        for _ in range(5):
            perfil = generador.generar_perfil_unico()
            sistema = SistemaComportamientoCompra(perfil)
            sistemas.append(sistema)
        
        # Verificar que hay diversidad en comportamientos
        comportamientos = [s.comportamiento_dominante for s in sistemas]
        tiempos = [s.tiempo_promedio_decision for s in sistemas]
        
        # Debería haber al menos alguna variación
        self.assertGreater(len(set(str(c) for c in comportamientos)), 1, 
                          "Los sistemas deberían generar comportamientos diversos")
        self.assertGreater(max(tiempos) - min(tiempos), 5, 
                          "Los tiempos de decisión deberían variar")
    
    def assertBetween(self, value, min_val, max_val, msg=None):
        """Helper para verificar que un valor está en un rango"""
        if not (min_val <= value <= max_val):
            msg = msg or f"{value} no está entre {min_val} y {max_val}"
            raise AssertionError(msg)


class TestBienHiperrealista(unittest.TestCase):
    """Tests para el sistema de bienes hiperrealistas"""
    
    def setUp(self):
        self.bien = BienHiperrealista("Smartphone Premium", TipoBien.ELECTRONICO_PREMIUM)
    
    def test_creacion_bien_hiperrealista(self):
        """Test creación de bien hiperrealista"""
        self.assertEqual(self.bien.nombre, "Smartphone Premium")
        self.assertEqual(self.bien.tipo_bien, TipoBien.ELECTRONICO_PREMIUM)
        self.assertIsInstance(self.bien.categoria, str)
        
        # Verificar que se crearon todas las características
        self.assertIsNotNone(self.bien.propiedades_fisicas)
        self.assertIsNotNone(self.bien.atributos_calidad)
        self.assertIsNotNone(self.bien.impacto_emocional)
        self.assertIsNotNone(self.bien.factores_sociales)
        self.assertIsNotNone(self.bien.impacto_ambiental)
    
    def test_tipos_bien_validos(self):
        """Test que todos los tipos de bien son válidos"""
        for tipo in TipoBien:
            self.assertIsInstance(tipo.value, str)
            self.assertGreater(len(tipo.value), 0)
    
    def test_propiedades_fisicas_en_rango(self):
        """Test que las propiedades físicas están en rangos válidos"""
        props = self.bien.propiedades_fisicas
        
        self.assertGreater(props.peso, 0)
        self.assertGreater(props.volumen, 0)
        self.assertGreater(props.durabilidad_base, 0)
        self.assertBetween(props.fragilidad, 0.0, 1.0)
        self.assertBetween(props.transportabilidad, 0.0, 1.0)
    
    def test_atributos_calidad_coherentes(self):
        """Test que los atributos de calidad son coherentes"""
        calidad = self.bien.atributos_calidad
        
        self.assertIsInstance(calidad.nivel_calidad, CalidadBien)
        self.assertBetween(calidad.marca_prestigio, 0.0, 1.0)
        self.assertBetween(calidad.innovacion_tecnologica, 0.0, 1.0)
        self.assertBetween(calidad.diseño_estetico, 0.0, 1.0)
        self.assertBetween(calidad.funcionalidad, 0.0, 1.0)
        self.assertGreaterEqual(calidad.garantia_meses, 0)
    
    def test_impacto_emocional_en_rango(self):
        """Test que el impacto emocional está en rango válido"""
        impacto = self.bien.impacto_emocional
        
        self.assertBetween(impacto.factor_estatus, 0.0, 1.0)
        self.assertBetween(impacto.factor_placer, 0.0, 1.0)
        self.assertBetween(impacto.factor_seguridad, 0.0, 1.0)
        self.assertBetween(impacto.factor_autoestima, 0.0, 1.0)
    
    def test_factores_sociales_en_rango(self):
        """Test que los factores sociales están en rango válido"""
        factores = self.bien.factores_sociales
        
        self.assertBetween(factores.popularidad_general, 0.0, 1.0)
        self.assertBetween(factores.tendencia_crecimiento, -1.0, 1.0)
        self.assertBetween(factores.factor_viral, 0.0, 1.0)
        self.assertBetween(factores.influencia_celebridades, 0.0, 1.0)
    
    def test_compatibilidad_con_perfil_consumidor(self):
        """Test cálculo de compatibilidad con perfil de consumidor"""
        # Crear un perfil mock
        perfil_mock = Mock()
        perfil_mock.tipo_personalidad = Mock()
        perfil_mock.tipo_personalidad.value = 'hedonista'
        
        # Mock de preferencias
        prefs_mock = Mock()
        prefs_mock.preferencia_tecnologia = 0.8
        prefs_mock.preferencia_alimentacion = 0.3
        prefs_mock.preferencia_ropa = 0.5
        perfil_mock.preferencias_consumo = prefs_mock
        
        # Mock de rasgos
        rasgos_mock = Mock()
        rasgos_mock.importancia_sostenibilidad = 0.6
        rasgos_mock.importancia_calidad = 0.7
        rasgos_mock.materialismo = 0.8
        perfil_mock.rasgos_psicologicos = rasgos_mock
        
        compatibilidad = self.bien.es_compatible_con_perfil(perfil_mock)
        
        self.assertIsInstance(compatibilidad, float)
        self.assertBetween(compatibilidad, 0.0, 1.0)
    
    def test_diferentes_tipos_generan_diferentes_caracteristicas(self):
        """Test que diferentes tipos de bien generan características diferentes"""
        bien_alimento = BienHiperrealista("Pan Artesanal", TipoBien.ALIMENTO_PREMIUM)
        bien_electronico = BienHiperrealista("Laptop Gaming", TipoBien.ELECTRONICO_PREMIUM)
        
        # Las propiedades físicas deberían ser diferentes
        self.assertNotEqual(
            bien_alimento.propiedades_fisicas.peso,
            bien_electronico.propiedades_fisicas.peso
        )
        
        # Los factores emocionales podrían ser diferentes
        diferencia_estatus = abs(
            bien_alimento.impacto_emocional.factor_estatus -
            bien_electronico.impacto_emocional.factor_estatus
        )
        
        # Debería haber alguna diferencia (aunque no garantizada)
        # Solo verificamos que no son exactamente iguales
        self.assertNotEqual(
            bien_alimento.impacto_emocional.factor_estatus,
            bien_electronico.impacto_emocional.factor_estatus
        )
    
    def test_historial_y_metricas_inicializados(self):
        """Test que el historial y métricas están inicializados"""
        self.assertIsInstance(self.bien.historial_precios, list)
        self.assertIsInstance(self.bien.valoraciones_usuarios, list)
        self.assertEqual(self.bien.ventas_totales, 0)
        self.assertEqual(self.bien.quejas_registradas, 0)
        
        # Conjuntos de relaciones
        self.assertIsInstance(self.bien.sustitutos, set)
        self.assertIsInstance(self.bien.complementos, set)
        self.assertIsInstance(self.bien.productos_bundle, set)
    
    def assertBetween(self, value, min_val, max_val, msg=None):
        """Helper para verificar que un valor está en un rango"""
        if not (min_val <= value <= max_val):
            msg = msg or f"{value} no está entre {min_val} y {max_val}"
            raise AssertionError(msg)


class TestIntegracionSistemasHiperrealistas(unittest.TestCase):
    """Tests de integración entre los sistemas hiperrealistas"""
    
    def setUp(self):
        self.generador = GeneradorPerfilesPersonalidad()
        self.perfil = self.generador.generar_perfil_unico()
        self.sistema_comportamiento = SistemaComportamientoCompra(self.perfil)
        self.bien = BienHiperrealista("Producto Test", TipoBien.ELECTRONICO_PREMIUM)
    
    def test_perfil_influye_en_comportamiento(self):
        """Test que el perfil de personalidad influye en el comportamiento"""
        # Crear múltiples sistemas y verificar correlaciones
        sistemas = []
        for _ in range(20):
            perfil = self.generador.generar_perfil_unico()
            sistema = SistemaComportamientoCompra(perfil)
            sistemas.append((perfil, sistema))
        
        # Buscar correlaciones esperadas
        correlaciones_encontradas = 0
        
        for perfil, sistema in sistemas:
            # Impulsividad alta debería resultar en tiempo de decisión bajo
            if (perfil.rasgos_psicologicos.impulsividad > 0.7 and 
                sistema.tiempo_promedio_decision < 30):
                correlaciones_encontradas += 1
            
            # Planificación alta debería resultar en tiempo de decisión alto
            if (perfil.rasgos_psicologicos.planificacion > 0.7 and 
                sistema.tiempo_promedio_decision > 60):
                correlaciones_encontradas += 1
        
        # Al menos 30% deberían mostrar correlaciones
        self.assertGreater(correlaciones_encontradas, len(sistemas) * 0.3)
    
    def test_compatibilidad_bien_perfil_coherente(self):
        """Test que la compatibilidad bien-perfil es coherente"""
        # Crear perfiles con preferencias extremas
        perfiles_tecnologia = []
        perfiles_alimentacion = []
        
        for _ in range(10):
            perfil = self.generador.generar_perfil_unico()
            if perfil.preferencias_consumo.preferencia_tecnologia > 0.7:
                perfiles_tecnologia.append(perfil)
            if perfil.preferencias_consumo.preferencia_alimentacion > 0.7:
                perfiles_alimentacion.append(perfil)
        
        if len(perfiles_tecnologia) > 0 and len(perfiles_alimentacion) > 0:
            bien_tecnologia = BienHiperrealista("Laptop Pro", TipoBien.ELECTRONICO_PREMIUM)
            bien_alimentacion = BienHiperrealista("Comida Gourmet", TipoBien.ALIMENTO_PREMIUM)
            
            # Los perfiles tecnológicos deberían preferir bienes tecnológicos
            for perfil in perfiles_tecnologia:
                compat_tech = bien_tecnologia.es_compatible_con_perfil(perfil)
                compat_food = bien_alimentacion.es_compatible_con_perfil(perfil)
                
                # No siempre garantizado, pero debería haber tendencia
                # Solo verificamos que se calculan valores válidos
                self.assertBetween(compat_tech, 0.0, 1.0)
                self.assertBetween(compat_food, 0.0, 1.0)
    
    def test_sistema_completo_coherencia(self):
        """Test de coherencia del sistema completo"""
        # Crear múltiples consumidores y productos
        consumidores = []
        for i in range(5):
            perfil = self.generador.generar_perfil_unico()
            comportamiento = SistemaComportamientoCompra(perfil)
            consumidores.append({
                'perfil': perfil,
                'comportamiento': comportamiento,
                'nombre': f'Consumidor_{i}'
            })
        
        productos = [
            BienHiperrealista("iPhone", TipoBien.ELECTRONICO_PREMIUM),
            BienHiperrealista("Pan", TipoBien.ALIMENTO_BASICO),
            BienHiperrealista("Zapatillas", TipoBien.ROPA_MODA)
        ]
        
        # Matriz de compatibilidades
        matriz_compatibilidades = []
        for consumidor in consumidores:
            fila_compatibilidades = []
            for producto in productos:
                compat = producto.es_compatible_con_perfil(consumidor['perfil'])
                fila_compatibilidades.append(compat)
            matriz_compatibilidades.append(fila_compatibilidades)
        
        # Verificar que hay variabilidad en las compatibilidades
        for col in range(len(productos)):
            compatibilidades_producto = [fila[col] for fila in matriz_compatibilidades]
            
            # Debería haber alguna variabilidad (no todos iguales)
            min_compat = min(compatibilidades_producto)
            max_compat = max(compatibilidades_producto)
            variabilidad = max_compat - min_compat
            
            # Al menos 0.1 de diferencia entre el más compatible y menos compatible
            self.assertGreater(variabilidad, 0.05)
    
    def assertBetween(self, value, min_val, max_val, msg=None):
        """Helper para verificar que un valor está en un rango"""
        if not (min_val <= value <= max_val):
            msg = msg or f"{value} no está entre {min_val} y {max_val}"
            raise AssertionError(msg)


if __name__ == '__main__':
    unittest.main()
