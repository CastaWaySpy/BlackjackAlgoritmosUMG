import random
import time

PAUSA = 1.5

# Crear baraja estándar de 52 cartas
def crear_baraja():
    palos = ['♠', '♥', '♦', '♣']
    valores = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 10, 'Q': 10, 'K': 10, 'A': 11
    }
    baraja = []
    for palo in palos:
        for valor, puntos in valores.items():
            baraja.append((valor + palo, puntos))
    random.shuffle(baraja)
    return baraja

# Calcular puntaje considerando los As
def puntaje(mano):
    total = sum(carta[1] for carta in mano)
    ases = sum(1 for carta in mano if carta[0].startswith('A'))
    while total > 21 and ases:
        total -= 10
        ases -= 1
    return total

# Mostrar mano
def mostrar_mano(nombre, mano, ocultar=False):
    if ocultar:
        print(f"{nombre}: [{mano[0][0]}, ?]")
    else:
        cartas = ', '.join(c[0] for c in mano)
        print(f"{nombre}: [{cartas}] → Total: {puntaje(mano)}")

# Turno de un jugador
def turno_jugador(nombre, mano, baraja):
    while True:
        print("----------------------------------------")
        mostrar_mano(nombre, mano)
        if puntaje(mano) > 21:
            print(f"{nombre} se pasó de 21. ❌")
            time.sleep(PAUSA)
            break
        eleccion = input(f"{nombre}, ¿quieres otra carta? (s/n): ").lower()
        if eleccion == 's':
            print(f"{nombre} toma una carta...")
            time.sleep(PAUSA)
            nueva = baraja.pop()
            mano.append(nueva)
            print(f"{nombre} recibe {nueva[0]}")
            time.sleep(PAUSA)
        else:
            break
    return mano

# Turno del dealer
def turno_dealer(dealer, baraja):
    print("\n----------------------------------------")
    print("Turno del Dealer...")
    time.sleep(PAUSA)

    print("El dealer revela su mano:")
    mostrar_mano("Dealer", dealer)
    time.sleep(PAUSA)

    while puntaje(dealer) < 17:
        print("Dealer toma una carta...")
        time.sleep(PAUSA)
        nueva = baraja.pop()
        dealer.append(nueva)
        print(f"Dealer recibe {nueva[0]}")
        mostrar_mano("Dealer", dealer)
        time.sleep(PAUSA)

    return dealer

# Comparar resultados
def comparar(nombre, mano_jugador, mano_dealer, saldo, apuesta):
    pj = puntaje(mano_jugador)
    pd = puntaje(mano_dealer)
    print("----------------------------------------")
    print(f"Resultado de {nombre}: {pj} vs {pd}")
    time.sleep(PAUSA)

    if pj > 21:
        print(f"{nombre} pierde la apuesta de ${apuesta}.")
        saldo -= apuesta
    elif pd > 21 or pj > pd:
        print(f"¡{nombre} gana ${apuesta}!")
        saldo += apuesta
    elif pj < pd:
        print(f"{nombre} pierde la apuesta de ${apuesta}.")
        saldo -= apuesta
    else:
        print(f"{nombre} empata y recupera su apuesta.")
    time.sleep(PAUSA)
    return saldo

# Modo de 1 jugador
def modo_un_jugador():
    saldo = 100
    ronda = 1

    while True:
        print(f"\n----------------------------------------")
        print(f"🎲 RONDA {ronda} — Saldo: ${saldo}")
        print("----------------------------------------")

        if saldo <= 0:
            print("Te quedaste sin dinero. Fin del juego.")
            return

        baraja = crear_baraja()
        apuesta = int(input("Apuesta: "))

        if apuesta > saldo:
            print("No puedes apostar más de tu saldo.")
            continue

        jugador = [baraja.pop(), baraja.pop()]
        dealer = [baraja.pop(), baraja.pop()]

        print("\n--- Manos iniciales ---")
        mostrar_mano("Jugador", jugador)
        mostrar_mano("Dealer", dealer, ocultar=True)
        time.sleep(PAUSA)

        jugador = turno_jugador("Jugador", jugador, baraja)
        dealer = turno_dealer(dealer, baraja)

        print("\n--- RESULTADOS ---")
        mostrar_mano("Dealer", dealer)
        saldo = comparar("Jugador", jugador, dealer, saldo, apuesta)

        seguir = input("\n¿Jugar otra ronda? (s/n): ").lower()
        if seguir != 's':
            return
        ronda += 1

# Modo de 2 jugadores
def modo_dos_jugadores():
    saldo1 = saldo2 = 100
    ronda = 1

    while True:
        print(f"\n----------------------------------------")
        print(f"🎲 RONDA {ronda} — Saldos: J1=${saldo1} | J2=${saldo2}")
        print("----------------------------------------")

        if saldo1 <= 0 and saldo2 <= 0:
            print("Ambos jugadores se quedaron sin dinero. Fin del juego.")
            return

        baraja = crear_baraja()
        apuesta1 = int(input("Jugador 1, apuesta: "))
        apuesta2 = int(input("Jugador 2, apuesta: "))

        if apuesta1 > saldo1 or apuesta2 > saldo2:
            print("No pueden apostar más de su saldo.")
            continue

        jugador1 = [baraja.pop(), baraja.pop()]
        jugador2 = [baraja.pop(), baraja.pop()]
        dealer = [baraja.pop(), baraja.pop()]

        print("\n--- Manos iniciales ---")
        mostrar_mano("Jugador 1", jugador1)
        mostrar_mano("Jugador 2", jugador2)
        mostrar_mano("Dealer", dealer, ocultar=True)
        time.sleep(PAUSA)

        jugador1 = turno_jugador("Jugador 1", jugador1, baraja)
        jugador2 = turno_jugador("Jugador 2", jugador2, baraja)
        dealer = turno_dealer(dealer, baraja)

        print("\n--- RESULTADOS ---")
        mostrar_mano("Dealer", dealer)
        saldo1 = comparar("Jugador 1", jugador1, dealer, saldo1, apuesta1)
        saldo2 = comparar("Jugador 2", jugador2, dealer, saldo2, apuesta2)

        print(f"\nSaldos → J1=${saldo1} | J2=${saldo2}")
        time.sleep(PAUSA)

        seguir = input("\n¿Jugar otra ronda? (s/n): ").lower()
        if seguir != 's':
            return
        ronda += 1

# Menú principal
def menu():
    print("----------------------------------------")
    print("🃏  BLACKJACK SZ  🃏")
    print("----------------------------------------")
    print("1) Un jugador vs Dealer")
    print("2) Dos jugadores vs Dealer")
    print("0) Salir")
    print("----------------------------------------")

    opcion = input("Elige una opción: ")
    if opcion == '1':
        modo_un_jugador()
    elif opcion == '2':
        modo_dos_jugadores()
    else:
        print("Hasta la próxima.")

menu()
