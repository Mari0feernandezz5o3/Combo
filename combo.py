#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CREADOR DE COMBOS - Script optimizado para Termux/Android
by: 🤖Mario fernandez🤖
"""

import os
import sys
import random
import time
import shutil
from datetime import datetime
import string

# Intentar importar colorama con fallback
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORES_DISPONIBLES = True
except ImportError:
    COLORES_DISPONIBLES = False
    # Definir colores dummy
    class Fore:
        RED = ''; GREEN = ''; YELLOW = ''; BLUE = ''; MAGENTA = ''; CYAN = ''; WHITE = ''; RESET = ''
    class Back:
        RED = ''; GREEN = ''; YELLOW = ''; BLUE = ''; MAGENTA = ''; CYAN = ''; WHITE = ''; RESET = ''
    class Style:
        BRIGHT = ''; DIM = ''; NORMAL = ''; RESET_ALL = ''

# Listas de nombres y apellidos latinos (fallback)
NOMBRES_LATINOS = [
    'Juan', 'María', 'José', 'Ana', 'Carlos', 'Luis', 'Martha', 'Pedro', 'Paula', 'Jorge',
    'Rosa', 'Miguel', 'Elena', 'Pablo', 'Diana', 'Andrés', 'Laura', 'Diego', 'Sofía', 'David',
    'Cristina', 'Fernando', 'Patricia', 'Gabriel', 'Carmen', 'Antonio', 'Isabel', 'Manuel', 'Teresa', 'Francisco',
    'Raquel', 'Ricardo', 'Verónica', 'Héctor', 'Sandra', 'Ángel', 'Gloria', 'Javier', 'Susana', 'Rafael',
    'Daniela', 'Alejandro', 'Carolina', 'Sergio', 'Andrea', 'Eduardo', 'Paola', 'Roberto', 'Natalia', 'Mario',
    'Silvia', 'Oscar', 'Lorena', 'César', 'Monica', 'Victor', 'Alejandra', 'Raúl', 'Adriana', 'Arturo',
    'Elisa', 'Alberto', 'Gabriela', 'Ernesto', 'Mariana', 'Felipe', 'Liliana', 'Jesús', 'Angélica', 'Alfredo',
    'Claudia', 'Guillermo', 'Erika', 'Armando', 'Ivonne', 'Ramiro', 'Dolores', 'Alfonso', 'Marisol', 'Enrique',
    'Karina', 'Emilio', 'Esther', 'Rodolfo', 'Consuelo', 'Israel', 'Tatiana', 'Emmanuel', 'Esperanza', 'Esteban',
    'Leticia', 'Hugo', 'Irene', 'Lorenzo', 'Magdalena', 'Nelson', 'Miriam', 'Ruben', 'Olga', 'Salvador'
]

APELLIDOS_LATINOS = [
    'García', 'Martínez', 'López', 'González', 'Rodríguez', 'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores',
    'Rivera', 'Morales', 'Ortiz', 'Cruz', 'Reyes', 'Gutiérrez', 'Mendoza', 'Molina', 'Vega', 'Guzmán',
    'Fernández', 'Jiménez', 'Romero', 'Álvarez', 'Hernández', 'Díaz', 'Moreno', 'Muñoz', 'Álvarez', 'Ruiz',
    'Domínguez', 'Vázquez', 'Ramos', 'Guerra', 'Méndez', 'Castillo', 'Flores', 'Rojas', 'Ponce', 'Soto',
    'Gómez', 'Ortega', 'Núñez', 'Palacios', 'Rosales', 'Cabrera', 'Herrera', 'Villanueva', 'Campos', 'Silva',
    'Valdez', 'Ríos', 'Ocampo', 'Contreras', 'Nava', 'Vargas', 'Castro', 'Serrano', 'Zúñiga', 'Nieto',
    'Medina', 'Aguilar', 'Ramírez', 'Reyna', 'Valenzuela', 'Salazar', 'Lara', 'Delgado', 'Luna', 'Guerrero',
    'Rangel', 'Padilla', 'Meza', 'Gallegos', 'Villarreal', 'Galindo', 'Rascón', 'Zamora', 'Carbajal', 'Navarro',
    'Santos', 'Pineda', 'Escobar', 'Maldonado', 'Zavala', 'Espinoza', 'Granados', 'Valle', 'Bernal', 'Salas'
]

# Caracteres para contraseñas seguras
CARACTERES = string.ascii_letters + string.digits + "!@#$%&*"

class GeneradorCombos:
    def __init__(self):
        self.ruta_base = '/storage/emulated/0/Combo'
        self.ruta_fallback = './Combos'
        self.ruta_actual = self.ruta_base if os.path.exists('/storage/emulated/0') else self.ruta_fallback
        self.crear_directorio()
        
    def crear_directorio(self):
        """Crear directorio de combos si no existe"""
        try:
            os.makedirs(self.ruta_actual, exist_ok=True)
        except Exception:
            self.ruta_actual = self.ruta_fallback
            os.makedirs(self.ruta_actual, exist_ok=True)
    
    def colorear(self, texto, color=Fore.WHITE):
        """Aplicar color al texto si está disponible"""
        if COLORES_DISPONIBLES:
            return f"{color}{texto}{Style.RESET_ALL}"
        return texto
    
    def mostrar_banner(self):
        """Mostrar banner personalizado"""
        os.system('clear' if os.name == 'posix' else 'cls')
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        banner = f"""
{Fore.CYAN if COLORES_DISPONIBLES else ''}╔══════════════════════════════════════════════════════════════╗
║ {Fore.RED if COLORES_DISPONIBLES else ''}🔥 CREADOR DE COMBOS 🔥{Fore.CYAN if COLORES_DISPONIBLES else ''} ║
║ {Fore.YELLOW if COLORES_DISPONIBLES else ''}by: 🤖Mario fernandez🤖{Fore.CYAN if COLORES_DISPONIBLES else ''} ║
║ {Fore.GREEN if COLORES_DISPONIBLES else ''}SCRIPT OPTIMIZADO PARA TERMUX/ANDROID{Fore.CYAN if COLORES_DISPONIBLES else ''} ║
║ 📅 {fecha} ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL if COLORES_DISPONIBLES else ''}
        """
        print(banner)
    
    def mostrar_progreso(self, actual, total, combo_nombre, tipo, muestra):
        """Mostrar barra de progreso multilínea (Tipo 7)"""
        porcentaje = (actual / total) * 100
        barra_len = 30
        completados = int(barra_len * actual / total)
        barra = '=' * completados + ' ' * (barra_len - completados)
        
        # Línea 1-3: Barra de progreso
        print(f"\n{Fore.CYAN if COLORES_DISPONIBLES else ''}╔{'═' * barra_len}╗")
        print(f"║ [{barra}] {porcentaje:.1f}% {actual}/{total} ║")
        print(f"╚{'═' * barra_len}╝{Style.RESET_ALL if COLORES_DISPONIBLES else ''}")
        
        # Línea 4-5: Información del combo
        print(f"{Fore.YELLOW if COLORES_DISPONIBLES else ''}📁 Combo: {combo_nombre}")
        print(f"🔧 Tipo: {tipo} | Generado: {muestra[:20]}...{Style.RESET_ALL if COLORES_DISPONIBLES else ''}")
        
        # Mover cursor hacia arriba para sobrescribir
        sys.stdout.write('\033[5A')
        sys.stdout.flush()
    
    def generar_nombre(self, tipo):
        """Generar nombre según tipo (1: nombre+apellido, 2: solo nombre)"""
        nombre = random.choice(NOMBRES_LATINOS)
        if tipo == 1:
            apellido = random.choice(APELLIDOS_LATINOS)
            return f"{nombre}{apellido}"
        return nombre
    
    def generar_contrasena(self, longitud=10):
        """Generar contraseña segura"""
        if longitud < 8:
            longitud = 10
        return ''.join(random.choice(CARACTERES) for _ in range(longitud))
    
    def generar_combo(self, tipo):
        """Generar un combo según el tipo"""
        if tipo == 1:  # Nombre:Nombre
            nombre1 = self.generar_nombre(1)  # nombre+apellido
            nombre2 = self.generar_nombre(1)  # nombre+apellido
            return f"{nombre1}:{nombre2}"
        
        elif tipo == 2:  # Nombre+Número:Nombre+Número
            nombre1 = self.generar_nombre(random.choice([1, 2]))  # 50% nombre+apellido, 50% solo nombre
            nombre2 = self.generar_nombre(random.choice([1, 2]))
            num1 = random.randint(1, 9999)
            num2 = random.randint(1, 9999)
            return f"{nombre1}{num1}:{nombre2}{num2}"
        
        elif tipo == 3:  # Nombre:Contraseña
            nombre = self.generar_nombre(1)  # nombre+apellido
            contrasena = self.generar_contrasena()
            return f"{nombre}:{contrasena}"
        
        return ""
    
    def generar_combos(self):
        """Menú de generación de combos"""
        try:
            # Solicitar nombre del combo
            print(self.colorear("\n📝 NOMBRE DEL COMBO:", Fore.CYAN))
            nombre_combo = input(self.colorear("> ", Fore.GREEN)).strip()
            while not nombre_combo:
                print(self.colorear("❌ El nombre no puede estar vacío", Fore.RED))
                nombre_combo = input(self.colorear("> ", Fore.GREEN)).strip()
            
            # Solicitar tipo
            print(self.colorear("\n📌 TIPO DE COMBO:", Fore.CYAN))
            print("1. Nombre:Nombre")
            print("2. Nombre+Número:Nombre+Número")
            print("3. Nombre:Contraseña")
            
            while True:
                try:
                    tipo = int(input(self.colorear("Selecciona (1-3): ", Fore.GREEN)))
                    if 1 <= tipo <= 3:
                        break
                    print(self.colorear("❌ Opción inválida (1-3)", Fore.RED))
                except ValueError:
                    print(self.colorear("❌ Ingresa un número válido", Fore.RED))
            
            # Solicitar cantidad
            print(self.colorear("\n📊 CANTIDAD DE COMBOS:", Fore.CYAN))
            while True:
                try:
                    cantidad = int(input(self.colorear("> ", Fore.GREEN)))
                    if cantidad > 0:
                        break
                    print(self.colorear("❌ La cantidad debe ser mayor a 0", Fore.RED))
                except ValueError:
                    print(self.colorear("❌ Ingresa un número válido", Fore.RED))
            
            # Preparar para generar
            tipo_nombres = ["Nombre:Nombre", "Nombre+Número:Nombre+Número", "Nombre:Contraseña"]
            nombre_archivo = f"{nombre_combo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            ruta_completa = os.path.join(self.ruta_actual, nombre_archivo)
            
            print(self.colorear(f"\n🚀 Generando {cantidad} combos...", Fore.GREEN))
            
            # Generar combos
            combos = []
            inicio = time.time()
            
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                # Escribir cabecera
                cabecera = f"COMBO: {nombre_combo}\nTIPO: {tipo_nombres[tipo-1]}\nFECHA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nTOTAL: {cantidad}\n{'='*50}\n\n"
                f.write(cabecera)
                
                # Generar y guardar combos
                for i in range(1, cantidad + 1):
                    combo = self.generar_combo(tipo)
                    combos.append(combo)
                    f.write(f"{combo}\n")
                    
                    # Mostrar progreso cada 10 combos o al final
                    if i % 10 == 0 or i == cantidad:
                        self.mostrar_progreso(i, cantidad, nombre_combo, tipo_nombres[tipo-1], combo)
                        time.sleep(0.1)  # Pequeña pausa para ver el progreso
            
            fin = time.time()
            tiempo = fin - inicio
            
            # Limpiar líneas de progreso
            print('\n' * 6)
            
            # Mostrar resultados
            print(self.colorear(f"\n✅ {cantidad} combos generados exitosamente!", Fore.GREEN))
            print(self.colorear(f"📁 Guardado en: {ruta_completa}", Fore.CYAN))
            print(self.colorear(f"⏱️ Tiempo: {tiempo:.2f} segundos", Fore.MAGENTA))
            
            # Mostrar algunos ejemplos
            print(self.colorear("\n📝 Ejemplos generados:", Fore.CYAN))
            for i, combo in enumerate(combos[:3], 1):
                print(f"  {i}. {combo}")
            if len(combos) > 3:
                print(f"  ... y {len(combos)-3} más")
            
        except Exception as e:
            print(self.colorear(f"\n❌ Error: {str(e)}", Fore.RED))
        
        input(self.colorear("\nPresiona Enter para continuar...", Fore.YELLOW))
    
    def ver_archivos(self):
        """Mostrar lista de archivos guardados"""
        self.mostrar_banner()
        print(self.colorear("📂 ARCHIVOS GUARDADOS", Fore.CYAN))
        print("=" * 50)
        
        try:
            archivos = []
            for f in os.listdir(self.ruta_actual):
                if f.endswith('.txt'):
                    ruta = os.path.join(self.ruta_actual, f)
                    tamaño = os.path.getsize(ruta)
                    fecha = datetime.fromtimestamp(os.path.getmtime(ruta))
                    archivos.append((f, tamaño, fecha))
            
            if not archivos:
                print(self.colorear("❌ No hay archivos guardados", Fore.YELLOW))
            else:
                archivos.sort(key=lambda x: x[2], reverse=True)
                for i, (nombre, tamaño, fecha) in enumerate(archivos, 1):
                    tamaño_str = f"{tamaño/1024:.2f} KB" if tamaño < 1024*1024 else f"{tamaño/(1024*1024):.2f} MB"
                    print(f"{i:2}. {nombre[:30]:30} {tamaño_str:10} {fecha.strftime('%Y-%m-%d %H:%M')}")
            
            print(f"\n📁 Ruta: {self.ruta_actual}")
            
        except Exception as e:
            print(self.colorear(f"❌ Error: {str(e)}", Fore.RED))
        
        input(self.colorear("\nPresiona Enter para continuar...", Fore.YELLOW))
    
    def mostrar_estadisticas(self):
        """Mostrar estadísticas de archivos y combos"""
        self.mostrar_banner()
        print(self.colorear("📊 ESTADÍSTICAS", Fore.CYAN))
        print("=" * 50)
        
        try:
            total_archivos = 0
            total_combos = 0
            total_tamaño = 0
            
            for f in os.listdir(self.ruta_actual):
                if f.endswith('.txt'):
                    ruta = os.path.join(self.ruta_actual, f)
                    total_archivos += 1
                    total_tamaño += os.path.getsize(ruta)
                    
                    # Intentar leer número de combos desde la cabecera
                    try:
                        with open(ruta, 'r', encoding='utf-8') as archivo:
                            lineas = archivo.readlines()
                            for linea in lineas:
                                if linea.startswith('TOTAL:'):
                                    total_combos += int(linea.split(':')[1].strip())
                                    break
                    except:
                        # Si falla, contar líneas
                        with open(ruta, 'r', encoding='utf-8') as archivo:
                            lineas = archivo.readlines()
                            # Restar cabecera (primeras 6 líneas aproximadamente)
                            combos_en_archivo = max(0, len(lineas) - 6)
                            total_combos += combos_en_archivo
            
            tamaño_str = f"{total_tamaño/1024:.2f} KB" if total_tamaño < 1024*1024 else f"{total_tamaño/(1024*1024):.2f} MB"
            
            print(f"📁 Archivos: {self.colorear(str(total_archivos), Fore.GREEN)}")
            print(f"🔑 Combos totales: {self.colorear(str(total_combos), Fore.GREEN)}")
            print(f"💾 Tamaño total: {self.colorear(tamaño_str, Fore.GREEN)}")
            print(f"📂 Directorio: {self.ruta_actual}")
            
        except Exception as e:
            print(self.colorear(f"❌ Error: {str(e)}", Fore.RED))
        
        input(self.colorear("\nPresiona Enter para continuar...", Fore.YELLOW))
    
    def test_generacion(self):
        """Mostrar 10 combos de prueba"""
        self.mostrar_banner()
        print(self.colorear("🧪 TEST DE GENERACIÓN - 10 COMBOS DE PRUEBA", Fore.CYAN))
        print("=" * 50)
        
        try:
            for tipo in [1, 2, 3]:
                tipo_nombre = ["Nombre:Nombre", "Nombre+Número:Nombre+Número", "Nombre:Contraseña"][tipo-1]
                print(self.colorear(f"\n📌 Tipo {tipo}: {tipo_nombre}", Fore.YELLOW))
                
                for i in range(10):
                    combo = self.generar_combo(tipo)
                    print(f"  {i+1:2}. {combo}")
        
        except Exception as e:
            print(self.colorear(f"❌ Error: {str(e)}", Fore.RED))
        
        input(self.colorear("\nPresiona Enter para continuar...", Fore.YELLOW))
    
    def ejecutar_menu(self):
        """Ejecutar el menú principal"""
        while True:
            try:
                self.mostrar_banner()
                print(self.colorear("\n📋 MENÚ PRINCIPAL", Fore.CYAN))
                print("=" * 40)
                print("1. 🚀 Generar combos")
                print("2. 📂 Ver archivos guardados")
                print("3. 📊 Estadísticas")
                print("4. 🧪 Test de generación")
                print("5. ❌ Salir")
                
                opcion = input(self.colorear("\nSelecciona una opción (1-5): ", Fore.GREEN)).strip()
                
                if opcion == '1':
                    self.generar_combos()
                elif opcion == '2':
                    self.ver_archivos()
                elif opcion == '3':
                    self.mostrar_estadisticas()
                elif opcion == '4':
                    self.test_generacion()
                elif opcion == '5':
                    print(self.colorear("\n👋 ¡Hasta luego!", Fore.MAGENTA))
                    break
                else:
                    print(self.colorear("❌ Opción inválida", Fore.RED))
                    input(self.colorear("Presiona Enter para continuar...", Fore.YELLOW))
            
            except KeyboardInterrupt:
                print(self.colorear("\n\n👋 ¡Hasta luego!", Fore.MAGENTA))
                break
            except Exception as e:
                print(self.colorear(f"\n❌ Error inesperado: {str(e)}", Fore.RED))
                input(self.colorear("Presiona Enter para continuar...", Fore.YELLOW))

def main():
    """Función principal"""
    try:
        # Verificar si estamos en Termux
        if not os.path.exists('/data/data/com.termux'):
            print("⚠️  Ejecutando en entorno no Termux")
        
        app = GeneradorCombos()
        app.ejecutar_menu()
    
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error fatal: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()