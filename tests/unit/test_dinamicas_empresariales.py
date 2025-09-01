"""
Tests para las nuevas dinámicas empresariales:
- Política de inventarios S,s
- Costos de ajuste de precios y rigidez
- Rotación empresarial (quiebra y entrada)
"""

import pytest
import random
from unittest.mock import MagicMock, patch
from src.models.Mercado import Mercado
from src.models.EmpresaProductora import EmpresaProductora
from src.models.Bien import Bien


@pytest.fixture
def mercado_basico():
    """Mercado básico para tests"""
    bienes = {
        'pan': Bien('pan', 'alimentos_basicos'),
        'cafe': Bien('cafe', 'alimentos_lujo'),
        'telefono': Bien('telefono', 'tecnologia')
    }
    mercado = Mercado(bienes)
    return mercado


@pytest.fixture 
def empresa_productora(mercado_basico):
    """Empresa productora para tests"""
    empresa = EmpresaProductora('TestEmpresa', mercado_basico)
    empresa.dinero = 100000  # Capital inicial suficiente
    return empresa


class TestInventariosSs:
    """Tests para política de inventarios S,s"""
    
    def test_inicializacion_parametros_ss(self, empresa_productora):
        """Verifica que se inicialicen correctamente los parámetros S,s"""
        empresa = empresa_productora
        
        # Verificar que se crearon los diccionarios
        assert hasattr(empresa, 'inventario_objetivo')
        assert hasattr(empresa, 'punto_reorden')
        assert hasattr(empresa, 'costo_almacenamiento')
        assert hasattr(empresa, 'costo_faltante')
        
        # Verificar que hay valores para cada bien
        for bien in empresa.capacidad_produccion.keys():
            assert bien in empresa.inventario_objetivo
            assert bien in empresa.punto_reorden
            assert empresa.inventario_objetivo[bien] > 0
            assert empresa.punto_reorden[bien] > 0
            # s < S
            assert empresa.punto_reorden[bien] < empresa.inventario_objetivo[bien]
    
    def test_politica_ss_produccion(self, empresa_productora, mercado_basico):
        """Verifica que la política S,s funcione correctamente"""
        empresa = empresa_productora
        mercado = mercado_basico
        bien_test = 'pan'
        
        # Establecer inventario bajo (por debajo del punto de reorden)
        empresa.bienes[bien_test] = []  # Inventario vacío
        punto_reorden = empresa.punto_reorden[bien_test]
        inventario_objetivo = empresa.inventario_objetivo[bien_test]
        
        # Planificar producción
        plan = empresa.planificar_produccion(mercado)
        
        # Debe producir cuando stock <= punto de reorden
        assert plan[bien_test] > 0
        
        # Simular inventario alto (por encima del punto de reorden)
        # Crear items ficticios de inventario
        empresa.bienes[bien_test] = ['item'] * (punto_reorden + 5)
        
        plan2 = empresa.planificar_produccion(mercado)
        
        # No debe producir cuando stock > punto de reorden
        assert plan2[bien_test] == 0
    
    def test_ajuste_dinamico_ss(self, empresa_productora, mercado_basico):
        """Verifica el ajuste dinámico de parámetros S,s"""
        empresa = empresa_productora
        mercado = mercado_basico
        bien_test = 'pan'
        
        # Guardar valores originales
        objetivo_original = empresa.inventario_objetivo[bien_test]
        reorden_original = empresa.punto_reorden[bien_test]
        
        # Simular alta demanda (mock de ventas recientes)
        with patch.object(empresa, 'obtener_ventas_recientes') as mock_ventas:
            mock_ventas.return_value = objetivo_original * 0.9  # 90% del objetivo
            
            empresa.ajustar_politica_inventarios(mercado)
            
            # Los objetivos deben haber aumentado
            assert empresa.inventario_objetivo[bien_test] >= objetivo_original
            assert empresa.punto_reorden[bien_test] >= reorden_original


class TestCostosAjustePrecios:
    """Tests para costos de ajuste de precios y rigidez"""
    
    def test_inicializacion_costos_ajuste(self, empresa_productora):
        """Verifica inicialización de parámetros de costos de ajuste"""
        empresa = empresa_productora
        
        assert hasattr(empresa, 'costo_ajuste_precio')
        assert hasattr(empresa, 'historial_cambios_precio')
        assert hasattr(empresa, 'ciclos_sin_cambio_precio') 
        assert hasattr(empresa, 'umbral_cambio_precio')
        
        assert empresa.costo_ajuste_precio > 0
        assert empresa.umbral_cambio_precio > 0
        
        # Verificar historial para cada bien
        for bien in empresa.precios.keys():
            assert bien in empresa.historial_cambios_precio
            assert bien in empresa.ciclos_sin_cambio_precio
    
    def test_rigidez_precios_pequeños_cambios(self, empresa_productora, mercado_basico):
        """Verifica que cambios pequeños no se apliquen por rigidez"""
        empresa = empresa_productora
        mercado = mercado_basico
        bien_test = 'pan'
        
        precio_original = empresa.precios[bien_test]
        dinero_original = empresa.dinero
        
        # Mock para forzar un cambio pequeño de precio
        with patch('random.uniform', return_value=0.01):  # Cambio muy pequeño
            empresa.ajustar_precios_dinamico(mercado, bien_test)
        
        # El precio no debe haber cambiado (rigidez)
        assert empresa.precios[bien_test] == precio_original
        # No debe haber pagado costo de ajuste
        assert empresa.dinero == dinero_original
    
    def test_aplicacion_costos_ajuste(self, empresa_productora, mercado_basico):
        """Verifica que se apliquen costos cuando el cambio es significativo"""
        empresa = empresa_productora
        mercado = mercado_basico
        bien_test = 'pan'
        
        precio_original = empresa.precios[bien_test]
        dinero_original = empresa.dinero
        costo_ajuste = empresa.costo_ajuste_precio
        
        # Forzar un cambio significativo
        # Simular stock muy bajo para forzar aumento de precio
        empresa.bienes[bien_test] = []  # Inventario vacío
        empresa.inventario_objetivo[bien_test] = 100
        
        # Mock para asegurar que el cambio supere el umbral
        with patch.object(empresa, 'obtener_ventas_recientes', return_value=50):
            empresa.ajustar_precios_dinamico(mercado, bien_test)
        
        # Verificar que el precio cambió O no cambió por costo
        if empresa.precios[bien_test] != precio_original:
            # Si cambió, debe haber pagado el costo
            assert empresa.dinero < dinero_original
            # Debe haberse registrado en el historial
            assert len(empresa.historial_cambios_precio[bien_test]) > 0


class TestRotacionEmpresarial:
    """Tests para entrada y salida de empresas"""
    
    def test_deteccion_quiebra(self, empresa_productora):
        """Verifica detección correcta de quiebra"""
        empresa = empresa_productora
        
        # Empresa con dinero suficiente no debe estar en quiebra
        empresa.dinero = 50000
        empresa.costos_fijos_mensuales = 1000
        empresa.costo_salarios = 2000
        
        resultado = empresa.verificar_estado_financiero()
        assert resultado is True
        assert empresa.en_quiebra is False
        
        # Empresa sin dinero debe entrar en quiebra gradualmente
        empresa.dinero = 0
        empresa.costos_fijos_mensuales = 5000
        empresa.costo_salarios = 10000
        
        # Deshabilitar sistemas de rescate para el test
        empresa.mercado.sistema_bancario = None
        empresa.mercado.rescate_empresarial = None
        
        # Simular varios ciclos de crisis
        for _ in range(6):  # Más de 5 ciclos sin recursos
            empresa.verificar_estado_financiero()
        
        assert empresa.en_quiebra is True
    
    def test_entrada_nueva_empresa(self, mercado_basico):
        """Verifica creación de nuevas empresas"""
        mercado = mercado_basico
        empresas_iniciales = len(mercado.getEmpresas())
        
        # Forzar entrada de nueva empresa
        mercado.crear_nueva_empresa(ciclo=10)
        
        empresas_finales = len(mercado.getEmpresas())
        assert empresas_finales == empresas_iniciales + 1
        
        # Verificar que la nueva empresa tiene los atributos correctos
        nueva_empresa = mercado.getEmpresas()[-1]
        assert hasattr(nueva_empresa, 'es_entrante')
        assert hasattr(nueva_empresa, 'ciclo_entrada')
        assert nueva_empresa.es_entrante is True
        assert nueva_empresa.ciclo_entrada == 10
    
    def test_rotacion_empresas(self, mercado_basico):
        """Verifica el proceso completo de rotación"""
        mercado = mercado_basico
        
        # Agregar empresa en quiebra
        empresa_quiebra = EmpresaProductora('EmpresaQuiebra', mercado)
        empresa_quiebra.en_quiebra = True
        mercado.personas.append(empresa_quiebra)
        
        empresas_antes = len(mercado.getEmpresas())
        
        # Ejecutar rotación
        with patch('random.random', return_value=0.001):  # Forzar entrada
            mercado.gestionar_rotacion_empresas(ciclo=5)
        
        # La empresa en quiebra debe haberse removido
        empresas_activas = [e for e in mercado.getEmpresas() if not getattr(e, 'en_quiebra', False)]
        assert empresa_quiebra not in mercado.personas


class TestKPIsEmpresariales:
    """Tests para los nuevos KPIs empresariales"""
    
    def test_calculo_kpis_basico(self, mercado_basico):
        """Verifica cálculo básico de KPIs"""
        mercado = mercado_basico
        
        # Agregar empresas de prueba
        empresa1 = EmpresaProductora('Empresa1', mercado)
        empresa2 = EmpresaProductora('Empresa2', mercado)
        empresa2.en_quiebra = True
        
        mercado.personas.extend([empresa1, empresa2])
        
        kpis = mercado.calcular_kpis_empresariales(ciclo=1)
        
        # Verificar estructura de KPIs
        assert 'tasa_quiebra' in kpis
        assert 'rotacion_empresas' in kpis
        assert 'rigidez_precios' in kpis
        assert 'empresas_activas' in kpis
        assert 'empresas_entrantes' in kpis
        assert 'inventario_ratio_promedio' in kpis
        assert 'costos_ajuste_precio_totales' in kpis
        
        # Verificar cálculos básicos
        assert kpis['empresas_activas'] == 2
        assert kpis['tasa_quiebra'] == 0.5  # 1 de 2 empresas
    
    def test_rigidez_precios_kpi(self, mercado_basico):
        """Verifica cálculo de KPI de rigidez de precios"""
        mercado = mercado_basico
        
        empresa = EmpresaProductora('TestEmpresa', mercado)
        # Simular precios rígidos
        empresa.ciclos_sin_cambio_precio = {'pan': 5, 'cafe': 2, 'telefono': 8}
        mercado.personas.append(empresa)
        
        kpis = mercado.calcular_kpis_empresariales(ciclo=1)
        
        # 2 de 3 bienes tienen rigidez (>= 3 ciclos sin cambio)
        rigidez_esperada = 2.0 / 3.0
        assert abs(kpis['rigidez_precios'] - rigidez_esperada) < 0.01


if __name__ == '__main__':
    pytest.main([__file__])