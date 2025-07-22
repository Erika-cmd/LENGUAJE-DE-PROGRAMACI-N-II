import time
import sys

def limpiar_pantalla():
    """Limpia la consola para una mejor experiencia de usuario."""
    # Para sistemas Windows
    if sys.platform.startswith('win'):
        os.system('cls')
    # Para sistemas Unix (Linux, macOS)
    else:
        os.system('clear')

def mostrar_estado(inventario, objetivo_chupetines, mensaje=""):
    """Muestra el inventario actual y el estado del juego."""
    # limpiar_pantalla() # Descomentar si quieres limpiar la pantalla en cada actualización
    print("\n" + "="*50)
    print("        LOS SOBREVIVIENTES: El Desafío de los Caramelos")
    print("="*50)
    print(f"\nOBJETIVO: Obtener {objetivo_chupetines} Chupetines para el grupo.")
    print("\n--- TU INVENTARIO ACTUAL ---")
    print(f"🍋 Caramelos de Limón: {inventario['limon']}")
    print(f"🥚 Caramelos de Huevo: {inventario['huevo']}")
    print(f"🍐 Caramelos de Pera: {inventario['pera']}")
    print(f"🍭 Chupetines: {inventario['chupetin']} / {objetivo_chupetines}")
    print("\n" + "-"*50)
    if mensaje:
        print(f"MENSAJE: {mensaje}")
    print("-" * 50)

def verificar_fin_juego(inventario, objetivo_chupetines):
    """Verifica si el juego ha terminado (victoria o derrota)."""
    # Condición de Victoria
    if inventario['chupetin'] >= objetivo_chupetines:
        mostrar_estado(inventario, objetivo_chupetines, "¡VICTORIA! ¡Todos los Sobrevivientes tienen su chupetín!")
        return True, True # Juego terminado, Ganaste

    # Condición de Derrota (no hay más movimientos posibles)
    can_create = (inventario['limon'] >= 2 and inventario['pera'] >= 2 and inventario['huevo'] >= 2)
    can_exchange = (inventario['chupetin'] >= 1)

    if not can_create and not can_exchange:
        mostrar_estado(inventario, objetivo_chupetines, "¡DERROTA! No hay más movimientos posibles y no alcanzaste la meta.")
        return True, False # Juego terminado, Perdiste

    return False, False # Juego no terminado

def jugar():
    """Función principal del juego."""
    inventario = {
        'limon': 7, # Ejemplo: 7 de limón
        'pera': 7,  # Ejemplo: 7 de pera
        'huevo': 6, # Ejemplo: 6 de huevo
        'chupetin': 0
    }
    objetivo_chupetines = 10
    
    juego_terminado = False
    victoria = False
    
    while not juego_terminado:
        mostrar_estado(inventario, objetivo_chupetines)
        
        print("\n--- OPCIONES ---")
        print("1. Crear 1 Chupetín (Necesitas: 2🍋, 2🥚, 2🍐)")
        print("2. Canjear 1 Chupetín por Caramelos (Recibes: 2🍋, 2🥚, 2🍐)")
        print("3. Salir del Juego")
        
        opcion = input("Elige tu acción (1, 2 o 3): ")
        
        mensaje_accion = ""
        if opcion == '1':
            if inventario['limon'] >= 2 and inventario['huevo'] >= 2 and inventario['pera'] >= 2:
                inventario['limon'] -= 2
                inventario['huevo'] -= 2
                inventario['pera'] -= 2
                inventario['chupetin'] += 1
                mensaje_accion = "¡Chupetín creado! Has usado 2🍋, 2🥚, 2🍐."
            else:
                mensaje_accion = "❌ ¡Faltan caramelos para crear un chupetín! Necesitas 2 de cada tipo."
        elif opcion == '2':
            if inventario['chupetin'] >= 1:
                inventario['chupetin'] -= 1
                inventario['limon'] += 2
                inventario['huevo'] += 2
                inventario['pera'] += 2
                mensaje_accion = "✅ ¡Chupetín canjeado! Has recibido 2🍋, 2🥚, 2🍐."
            else:
                mensaje_accion = "❌ No tienes chupetines para canjear."
        elif opcion == '3':
            print("Saliendo del juego. ¡Gracias por jugar a Los Sobrevivientes!")
            time.sleep(2) # Espera un poco antes de salir
            sys.exit()
        else:
            mensaje_accion = "Opción no válida. Por favor, elige 1, 2 o 3."

        juego_terminado, victoria = verificar_fin_juego(inventario, objetivo_chupetines)
        if not juego_terminado: # Solo muestra el mensaje si el juego no ha terminado
            mostrar_estado(inventario, objetivo_chupetines, mensaje_accion)
            time.sleep(2) # Espera un poco para que el usuario lea el mensaje
    
    # Después de que el bucle termina, se muestra el mensaje final de victoria o derrota.
    print("\n--- FIN DEL JUEGO ---")
    if victoria:
        print("¡Felicidades! Lograste que todos los Sobrevivientes tuvieran su chupetín.")
    else:
        print("No lograste tu objetivo. Los Sobrevivientes tendrán que buscar otras soluciones...")
    print("="*50)
    print("Presiona Enter para salir.")
    input() # Espera a que el usuario presione Enter para cerrar la consola

if __name__ == "__main__":
    import os # Importa os aquí para limpiar_pantalla
    jugar()