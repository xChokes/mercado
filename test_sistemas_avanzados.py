"""
Test de funcionalidad de los nuevos sistemas implementados
"""
import sys
import traceback
from main_avanzado import *
from PsicologiaEconomica import inicializar_perfiles_psicologicos


def test_sistema_bancario():
    """Test del sistema bancario"""
    print("🧪 Probando Sistema Bancario...")
    try:
        bienes = crear_bienes_avanzados()
        mercado = Mercado(bienes)

        # Crear un consumidor de prueba
        consumidor = Consumidor("TestConsumidor", mercado)
        consumidor.dinero = 50000
        consumidor.empleado = True
        consumidor.ingreso_mensual = 5000
        mercado.agregar_persona(consumidor)

        # Test préstamo
        banco = mercado.sistema_bancario.bancos[0]
        exito, mensaje = banco.solicitar_prestamo(consumidor, 20000)

        print(f"   ✅ Préstamo: {exito} - {mensaje}")

        # Test depósito
        banco.depositar(consumidor, 10000)
        print(f"   ✅ Depósito realizado correctamente")

        # Test ciclo bancario
        stats = mercado.sistema_bancario.ciclo_bancario()
        print(f"   ✅ Ciclo bancario ejecutado: {stats}")

        return True
    except Exception as e:
        print(f"   ❌ Error en sistema bancario: {e}")
        return False


def test_sectores_economicos():
    """Test del sistema de sectores económicos"""
    print("🧪 Probando Sectores Económicos...")
    try:
        bienes = crear_bienes_avanzados()
        mercado = Mercado(bienes)

        # Crear empresas de prueba
        empresa1 = EmpresaProductora("TestAgro", mercado)
        empresa2 = EmpresaProductora("TestTech", mercado)
        mercado.agregar_persona(empresa1)
        mercado.agregar_persona(empresa2)

        # Asignar a sectores
        mercado.economia_sectorial.asignar_empresas_a_sectores()

        # Test ciclo sectorial
        mercado.economia_sectorial.ciclo_economico_sectorial()

        # Test estadísticas
        stats = mercado.economia_sectorial.obtener_estadisticas_sectoriales()
        print(f"   ✅ Estadísticas sectoriales: {len(stats)} sectores")

        return True
    except Exception as e:
        print(f"   ❌ Error en sectores económicos: {e}")
        return False


def test_psicologia_economica():
    """Test del sistema de psicología económica"""
    print("🧪 Probando Psicología Económica...")
    try:
        bienes = crear_bienes_avanzados()
        mercado = Mercado(bienes)

        # Crear consumidores de prueba
        for i in range(5):
            consumidor = Consumidor(f"TestCons{i}", mercado)
            mercado.agregar_persona(consumidor)

        # Inicializar perfiles psicológicos
        mercado.sistema_psicologia = inicializar_perfiles_psicologicos(mercado)

        # Test ciclo psicología
        mercado.sistema_psicologia.ciclo_psicologia_economica()

        # Test estadísticas
        stats = mercado.sistema_psicologia.obtener_estadisticas_psicologicas()
        print(
            f"   ✅ Psicología económica: Confianza {stats.get('indice_confianza', 0):.2f}")

        return True
    except Exception as e:
        print(f"   ❌ Error en psicología económica: {e}")
        traceback.print_exc()
        return False


def test_sistema_innovacion():
    """Test del sistema de innovación"""
    print("🧪 Probando Sistema de Innovación...")
    try:
        bienes = crear_bienes_avanzados()
        mercado = Mercado(bienes)

        # Crear empresa de prueba
        empresa = EmpresaProductora("TestInnovatora", mercado)
        empresa.dinero = 500000
        mercado.agregar_persona(empresa)

        # Test inversión en I+D
        innovacion, mensaje = mercado.sistema_innovacion.empresa_invierte_id(
            empresa, 100000)
        print(f"   ✅ I+D: {mensaje}")

        # Test ciclo de innovación
        mercado.sistema_innovacion.ciclo_innovacion()

        # Test estadísticas
        stats = mercado.sistema_innovacion.obtener_estadisticas_innovacion()
        print(
            f"   ✅ Innovación: {stats['tecnologias_disponibles']} tecnologías disponibles")

        return True
    except Exception as e:
        print(f"   ❌ Error en sistema de innovación: {e}")
        return False


def test_integracion_completa():
    """Test de integración de todos los sistemas"""
    print("🧪 Probando Integración Completa...")
    try:
        bienes = crear_bienes_avanzados()
        mercado = Mercado(bienes)
        configurar_economia_avanzada(mercado)

        # Ejecutar algunos ciclos
        for i in range(3):
            mercado.ejecutar_ciclo(i)

        # Verificar estadísticas completas
        stats = mercado.obtener_estadisticas_completas()

        required_keys = ['sistema_bancario',
                         'sectores_economicos', 'innovacion']
        all_present = all(key in stats for key in required_keys)

        print(f"   ✅ Integración completa: {all_present}")
        print(
            f"   📊 PIB registrado: ${stats['pib_historico'][-1] if stats['pib_historico'] else 0:,.2f}")

        return all_present
    except Exception as e:
        print(f"   ❌ Error en integración: {e}")
        traceback.print_exc()
        return False


def ejecutar_tests():
    """Ejecuta todos los tests"""
    print("🔬 EJECUTANDO TESTS DE SISTEMAS AVANZADOS")
    print("=" * 50)

    tests = [
        ("Sistema Bancario", test_sistema_bancario),
        ("Sectores Económicos", test_sectores_economicos),
        ("Psicología Económica", test_psicologia_economica),
        ("Sistema de Innovación", test_sistema_innovacion),
        ("Integración Completa", test_integracion_completa)
    ]

    resultados = {}

    for nombre, test_func in tests:
        print(f"\n{nombre}:")
        try:
            resultado = test_func()
            resultados[nombre] = resultado
        except Exception as e:
            print(f"   ❌ Error crítico: {e}")
            resultados[nombre] = False

    # Resumen
    print(f"\n📋 RESUMEN DE TESTS:")
    print("-" * 30)

    exitosos = sum(resultados.values())
    total = len(resultados)

    for nombre, resultado in resultados.items():
        status = "✅ PASS" if resultado else "❌ FAIL"
        print(f"   {nombre}: {status}")

    print(f"\n🎯 Resultado final: {exitosos}/{total} tests exitosos")

    if exitosos == total:
        print("🎉 ¡Todos los sistemas funcionan correctamente!")
        return True
    else:
        print("⚠️  Algunos sistemas requieren atención")
        return False


if __name__ == "__main__":
    ejecutar_tests()
