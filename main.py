import csv
import threading
import time

hora_inicial = time.time()  #Es la hora inicial de la simulación
canciones = []  #Esta es la lista general de canciones
cola_espera = []    #Esta es la cola de espera de canciones
cola_genero = []    #Esta es la cola de espera de canciones por genero
cola_artista = []   #Esta es la cola de espera de canciones por artista
cola_ano = []    #Esta es la cola de espera de canciones por año
canciones_reproducidas = [] #Esta es la cola de espera que se actualiza cada vez que se reproduce una canción

#Estamos definiendo la clase Cancion
class Cancion:
    def __init__(self, num, titulo, artista, genero, ano, bpm, nrgy, dnce, dB, live, val, dur, acous, spch, pop):
        self.num = num
        self.titulo = titulo
        self.artista = artista
        self.genero = genero
        self.ano = ano
        self.bpm = bpm
        self.nrgy = nrgy
        self.dnce = dnce
        self.dB = dB
        self.live = live
        self.val = val
        self.dur = dur
        self.acous = acous
        self.spch = spch
        self.pop = pop

#Este es el metodo que nos permite imprimir los atributos de la clase Cancion
    def __str__(self):
        return "# " + str(self.num) + ", Titulo: " + self.titulo + ", Artista: " + self.artista + ", Genero: " + self.genero + ", Año: " + str(
            self.ano) + ", bpm: " + str(self.bpm) + ", nrgy: " + str(self.nrgy) + ", dnce: " + str(self.dnce) + ", dB: " + str(
            self.dB) + ", live: " + str(self.live) + ", val: " + str(self.val) + ", dur: " + str(self.dur) + ", acous: " + str(
            self.acous) + ", spch: " + str(self.spch) + ", pop: " + str(self.pop)


contador = 0
tiempo_transcurrido = 0


#Este es el metodo que nos permite contar el tiempo (para la simulación de la lista de reproducción)
def contar():
    global contador, tiempo_transcurrido
    while True:
        time.sleep(1)
        contador += 10  #El contador aumenta de 10 a cada segundo, sino tendría que esperar mucho
        #tiempo para que se acabe de reproducir una canción
        tiempo_transcurrido += 10


hilo_contador = threading.Thread(target=contar)
hilo_contador.daemon = True
hilo_contador.start()


#Esta función nos permite agregar una canción a la lista general de canciones
def agregar_cancion():
    num = int(input("Ingrese el numero que le quieres dar a la cancion: "))
    titulo = input("Ingrese el titulo de la cancion: ")
    artista = input("Ingrese el artista de la cancion: ")
    genero = input("Ingrese el genero de la cancion: ")
    print("A partir de aquí, todos los atributos de la canción son números enteros.")
    ano = input("Ingrese el ano de la cancion: ")
    bpm = input("Ingrese el bpm de la cancion: ")
    nrgy = input("Ingrese el nrgy de la cancion: ")
    dnce = input("Ingrese el dnce de la cancion: ")
    dB = input("Ingrese el dB de la cancion: ")
    live = input("Ingrese el live de la cancion: ")
    val = input("Ingrese el val de la cancion: ")
    dur = input("Ingrese el dur de la cancion: ")
    acous = input("Ingrese el acous de la cancion: ")
    spch = input("Ingrese el spch de la cancion: ")
    pop = input("Ingrese el pop de la cancion: ")
    cancion = Cancion(num, titulo, artista, genero, ano, bpm, nrgy, dnce, dB, live, val, dur, acous, spch, pop)
    canciones.insert(int(num) - 1, cancion)
    for i in range(int(num), len(canciones)):
        canciones[i].num = str(int(canciones[i].num) + 1)


#Esta función carga todas las canciones del archivo csv a la lista general de canciones
def cargar_canciones():
    canciones = []
    with open('top10s.csv', newline='') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        next(lector_csv)  # Saltar la fila de encabezado
        for fila in lector_csv:
            cancion = Cancion(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], fila[9],
                              fila[10], fila[11], fila[12], fila[13], fila[14])
            canciones.append(cancion)
    return canciones


#Esta función nos permite eliminar una canción de la lista general de canciones
def eliminar_cancion():
    num = int(input("Ingrese el número de la canción que desea eliminar: "))
    for i in range(0, len(canciones)):
        if int(canciones[i].num) == num:
            del canciones[i]
            break
    for i in range(num - 1, len(canciones)):
        canciones[i].num = i + 1


#Esta función nos permite ver todas las canciones de la lista general de canciones
def mostrar_canciones():
    for cancion in canciones:
        print(str(cancion))


#Esta función nos permite agregar una canción a la lista de escucha desde la lista general de canciones
def lista_espera():
    global contador, tiempo_transcurrido
    num = input("Ingrese el número de la canción que quieres escuchar o agregar a la lista de espera: ")
    cancion = canciones[int(num) - 1]

    if len(cola_espera) == 0:
        contador = 0
        tiempo_transcurrido = 0
    # Agregar canción a la cola de espera
    cola_espera.append(cancion)
    canciones_reproducidas.append(cancion)

    # Calcular duración total de la cola y hora final prevista
    duracion_total = sum(int(c.dur) for c in cola_espera)
    hora_final_prevista = hora_inicial + duracion_total

    # Imprimir información de la cola de espera
    print("Hora inicial:", time.strftime("%H:%M:%S", time.localtime(hora_inicial)))
    print("Duración total: {} horas, {} minutos y {} segundos".format(duracion_total // 3600,
                                                                      (duracion_total % 3600) // 60,
                                                                      duracion_total % 60))
    print("Hora final prevista:", time.strftime("%H:%M:%S", time.localtime(hora_final_prevista)))
    if len(canciones_reproducidas) > 0:
        print("Reproduciendo canción: {}".format(canciones_reproducidas[0].titulo))



#Esta función nos permite ver todas las canciones de la lista de escucha
def mostrar_lista_espera():
    for cancion in canciones_reproducidas:
        print(str(cancion))

    duracion_total = sum(int(c.dur) for c in cola_espera)
    hora_final_prevista = hora_inicial + duracion_total
    if len(canciones_reproducidas) != 0:
        print("Hora inicial:", time.strftime("%H:%M:%S", time.localtime(hora_inicial)))
        print("Duración total: {} horas, {} minutos y {} segundos".format(duracion_total // 3600,
                                                                          (duracion_total % 3600) // 60,
                                                                          duracion_total % 60))
        print("Hora final prevista:", time.strftime("%H:%M:%S", time.localtime(hora_final_prevista)))
    else:
        print("No hay canciones en la lista de escucha.")

    if len(canciones_reproducidas) > 0:
        print("Reproduciendo canción: {}".format(canciones_reproducidas[0].titulo))


#Esta funcón nos permite eliminar las canciones que ya se acabaron de reproducir
def eliminar_canciones_terminadas():
    global contador, tiempo_transcurrido
    for i, cancion in enumerate(cola_espera):
        while contador < int(cola_espera[i].dur):
            return
        if contador >= int(cola_espera[i].dur):
            del canciones_reproducidas[0]
            tiempo_transcurrido -= int(cola_espera[i].dur)
            contador = tiempo_transcurrido





#Esta función nos permite eliminar una canción de la lista de escucha
def borrar_cancion():
    nume = int(input("Ingrese el número de la canción que desea borrar: "))

    # Verificar que el número de canción es válido
    if nume < 1:
        print("Número de canción inválido.")
        return

    for cancion in cola_espera:
        if int(cancion.num) == nume:
            cola_espera.remove(cancion)
            canciones_reproducidas.remove(cancion)
            break

    # Actualizar duracion total
    duracion_total = sum(int(c.dur) for c in cola_espera)

    # Actualizar hora final prevista
    hora_final_prevista = hora_inicial + duracion_total

    print("Hora inicial:", time.strftime("%H:%M:%S", time.localtime(hora_inicial)))
    print("Duración total: {} horas, {} minutos y {} segundos".format(duracion_total // 3600,
                                                                      (duracion_total % 3600) // 60,
                                                                      duracion_total % 60))
    print("Hora final prevista:", time.strftime("%H:%M:%S", time.localtime(hora_final_prevista)))


#Esta función nos permite buscar una canción por su género
def busqueda_por_genero():
    genero = input("Ingrese el genero que desea buscar: ")
    for cancion in canciones:
        if cancion.genero == genero:
            cola_genero.append(cancion)
    for cancion in cola_genero:
        print(str(cancion))
    duracion_total = sum(int(c.dur) for c in cola_genero)
    hora_final_prevista = hora_inicial + duracion_total

    # Imprimir información de la cola de espera
    print("Hora inicial:", time.strftime("%H:%M:%S", time.localtime(hora_inicial)))
    print("Duración total: {} horas, {} minutos y {} segundos".format(duracion_total // 3600,
                                                                      (duracion_total % 3600) // 60,
                                                                      duracion_total % 60))
    print("Hora final prevista:", time.strftime("%H:%M:%S", time.localtime(hora_final_prevista)))


#Esta función nos permite buscar una canción por su artista
def busqueda_por_artista():
    artista_buscar = input("Ingresa el nombre del artista que quieres buscar: ")
    for cancion in canciones:
        if artista_buscar in cancion.artista:
            cola_artista.append(cancion)
    for cancion in cola_artista:
        print(str(cancion))
    duracion_total = sum(int(c.dur) for c in cola_artista)
    hora_final_prevista = hora_inicial + duracion_total
    print("Hora inicial:", time.strftime("%H:%M:%S", time.localtime(hora_inicial)))
    print("Duración total: {} horas, {} minutos y {} segundos".format(duracion_total // 3600,
                                                                      (duracion_total % 3600) // 60,
                                                                      duracion_total % 60))
    print("Hora final prevista:", time.strftime("%H:%M:%S", time.localtime(hora_final_prevista)))


#Esta función nos permite buscar una canción por su año
def busqueda_por_ano():
    ano = input("Ingrese el año que desea buscar: ")
    for cancion in canciones:
        if cancion.ano == ano:
            cola_ano.append(cancion)
    for cancion in cola_ano:
        print(str(cancion))
    duracion_total = sum(int(c.dur) for c in cola_ano)
    hora_final_prevista = hora_inicial + duracion_total
    print("Hora inicial:", time.strftime("%H:%M:%S", time.localtime(hora_inicial)))
    print("Duración total: {} horas, {} minutos y {} segundos".format(duracion_total // 3600,
                                                                      (duracion_total % 3600) // 60,
                                                                      duracion_total % 60))
    print("Hora final prevista:", time.strftime("%H:%M:%S", time.localtime(hora_final_prevista)))





if __name__ == '__main__':
    canciones = cargar_canciones()

    while True:


        print("\n\nBienvenido al reproductor de canciones:")
        print("1. Agregar canción a la lista general")
        print("2. Eliminar canción de la lista general")
        print("3. Mostrar todas las canciones")
        print("4. Escuchar canción o agregar a la lista de escucha")
        print("5. Mostrar lista de escucha")
        print("6. Borrar una canción de la lista de espera")
        print("7. Escuchar canciones por género")
        print("8. Escuchar canciones por artista")
        print("9. Escuchar canciones por año")
        print("10. Salir")

        opcion = input("\nIngrese una opcion: ")

        if opcion == "1":
            agregar_cancion()
            print("Canción agregada exitosamente!")
        elif opcion == "2":
            eliminar_cancion()
            print("Canción eliminada exitosamente!")
        elif opcion == "3":
            mostrar_canciones()
        elif opcion == "4":
            eliminar_canciones_terminadas()
            lista_espera()
        elif opcion == "5":
            eliminar_canciones_terminadas()
            mostrar_lista_espera()
        elif opcion == "6":
            borrar_cancion()
        elif opcion == "7":
            busqueda_por_genero()
        elif opcion == "8":
            busqueda_por_artista()
        elif opcion == "9":
            busqueda_por_ano()
        elif opcion == "10":
            print("¡Gracias por usar el reproductor de canciones!")
            break
        else:
            print("Opción inválida, por favor ingrese una opción válida.")
