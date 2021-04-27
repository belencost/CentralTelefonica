
''' Consideraciones:
0. Como los datos son cargados en memoria y no hay persistencia, se deben cargar al menos una llamada para obtener una factura o historial no vacío.
1. Se utilizaron diccionarios con el objetivo de simplificar el funcionamiento del programa y utilizar los pocos datos que normamente nos da
una llamada como el número telefónico de origen y el de destino
2. Se realizaron algunas validaciones de entrada de datos pero no todas, con el objetivo de demostrar el conocimiento acerca de ello.
3. Se programó en un lenguaje Orientado a objetos como python porque es en el que más sentía seguridad por el momento.
4. No se realizó programación TDD porque mis intentos por aplicarlas me consumieron mucho tiempo y decidí investigar y hacer algunas pruebas 
pero no dejarlas representadas. Para este mini proyecto utilicé el módulo doctest porque me parecía el más conveniente dada la corta cantidad
de lineas de código.
5. También aprendí a debuggear el código con el módulo pdb. A lo largo del desarrollo lo utilicé.
6.Como los datos se toman del sistema, me limita a elegir llamadas realizadas en el momento, es decir generar historiales y facturales del mes de abril
'''

import datetime #Para obtener la fecha y hora
import time #Para simular la espera de una llamada telefónica
import os #Para limpiar la pantalla 

MONTO_FIJO = 300  # Abono fijo y mensual es una constante que se va a adicional al consumo total de todos los clientes


#Utilizo un diccionario para simplicar las funciones y poder probarlas, simulando que las siguientes claves son codigos telefónicos reales de pais y ciudad.
paises = {
    "1":0.1,
    "2":0.2,
    "3":0.3,
    "4":0.4,
    "5":0.5,
    "6":0.6,
    "7":0.7,
    "8":0.8,
    "9":0.9,
}
ciudades = {
    "1":0.1,
    "2":0.2,
    "3":0.3,
    "4":0.4,
    "5":0.5,
    "6":0.6,
    "7":0.7,
    "8":0.8,
    "9":0.9,
}

class NumeroTel: #Clase NumeroTel que almacena todos los atributos propios de un numero telefónico
    def __init__(self, codigo_pais, codigo_ciudad, numero):
        self.pais=codigo_pais
        self.ciudad=codigo_ciudad
        self.restante=numero


class Llamada: #Clase Llamada que almacena todos los atributos propios de un numero telefónico
    def __init__(self, tel_origen: NumeroTel, tel_destino: NumeroTel):
        self.origen = tel_origen
        self.destino = tel_destino
        self.duracion = None
        self.inicio = None
        self.costo = None
        self.tipo = ''

    def llamar(self): #Con ayuda de la libreria datetime obtengo el inicio de la llamada, es decir la hora y dia en que se realizo
        self.inicio = datetime.datetime.now()

    def obtener_mes(self): #De la hora y dia obtenida con datetime, obtengo con solamente el mes
        return self.inicio.month
    
    def obtener_hora(self): #De la hora y dia obtenida con datetime, obtengo con solamente la hora
        return self.inicio.hour

    def cortar(self): #Para cortar la llamada y tmb obtener la duracion de la llamada (hora y fecha inicial - hora y fecha actual) 
        self.duracion = datetime.datetime.now() - self.inicio
        print('Llamada finalizada ------- Duración: ', self.duracion)

    def tarifar_llamada(self): #Se realizan los cálculos del costo de cada llamada, comparando los codigos de pais y área ingresados. 
        if  self.origen.pais != self.destino.pais: 
            #obtengo la duracion en segundos y la divido por 60 para obtener minutos, luego la multiplico utilizando el codigo como clave del diccionario 
            self.costo = ((self.duracion).seconds)/60 * paises[self.origen.pais] 
            self.tipo = 'Internacional' #Voy guardando el tipo a medida que clasifico la llamada
        elif self.origen.ciudad != self.destino.ciudad:
            self.costo = ((self.duracion).seconds)/60 * ciudades[self.origen.ciudad]
            self.tipo = 'Nacional'
        else:
            self.tipo = 'Local'
            if self.inicio.weekday() <= 4:  #Me devuelve el día de la semana y controlo si es mejor a 4 para saber si es un día hábil ya que 5 y 6 corresponden a 'Sabado' y 'Domingo'
                if (self.obtener_hora()) > 8 and (self.obtener_hora()) < 20:  
                    self.costo = ((self.duracion).seconds)/60 * 0.2
                else: 
                    self.costo = ((self.duracion).seconds)/60 * 0.1
            else:
                self.costo = ((self.duracion).seconds)/60 * 0.1
        return self.costo


class Facturacion:
    def __init__(self, monto_mensual_fijo=MONTO_FIJO) -> None:
        self.llamadas = []
        self.monto_fijo = monto_mensual_fijo

    def agregar_llamada(self, llamada: Llamada): #Agrego un objeto llamada (una instancia de Llamada) a la lista de llamadas
        self.llamadas.append(llamada)

    def calcular_monto_mensual(self, nro, mes):
        acumulador = 0
        for llamada in self.llamadas:
            if llamada.obtener_mes()==mes and ''.join([llamada.origen.pais, llamada.origen.ciudad, llamada.origen.restante])==str(nro):
                acumulador += llamada.tarifar_llamada()
        return acumulador

    def imprimir_llamadas(self, nro, mes):  #Para imprimir llamadas segun mes y cliente
        print('')
        print('----------HISTORIAL DE LLAMADAS DEL PERIODO ', mes, 'DEL CLIENTE ',nro,'---------------')
        print('')
        print('             Número marcado ------- Costo --------- Tipo')
        cont=0 #Contador de llamadas realizadas por el cliente en un mes determinado
        for llamada in self.llamadas:
            if llamada.obtener_mes()==mes and ''.join([llamada.origen.pais, llamada.origen.ciudad, llamada.origen.restante])==str(nro):
                llamada.costo=llamada.tarifar_llamada()
                print ('                 +' + '-'.join([llamada.destino.pais, llamada.destino.ciudad, llamada.destino.restante]), 
                        '             {0:.3f}'.format(llamada.costo) ,'        ' ,llamada.tipo) 
                #El join me une los campos y los transforma en una cadena de caracteres, por ello al nro ingresado lo tengo que tranformar en string
                cont+=1
        print('                  -                -                   -')
        print('Se realizaron ', cont, 'llamadas en total.')

    def imprimir_facturas(self, nro, mes): 
        print('-------------------------------------------------------------------------')
        print('--------------- FACTURA DEL PERIODO ', mes, 'DEL CLIENTE ',nro,'-------------------')
        print('')
        self.imprimir_llamadas(nro, mes)
        print('')
        print('--------------------------RESUMEN DE CUENTA-----------------------------')
        print('')
        print('Consumo por llamadas: {0:.3f}'.format(self.calcular_monto_mensual(nro, mes)))
        print('')
        print('Abono mensual fijo: {}'.format(self.monto_fijo))
        print('')
        print('Consumo Total (llamadas + abono): {0:.3f}'.format(self.calcular_monto_mensual(nro, mes)+self.monto_fijo))
        print('----------------------------------------------------------------------------')
        
        
#Funcion que controla la ejecucion del programa
def main():

    unaFacturacion=Facturacion() #Creo un objeto factura 
    while True: 
        menu=str(input("""      
        \n------------------------------------CENTRAL TELEFÓNICA-----------------------------------\n
        
        1 - Generar Factura de Cliente     
        2 - Llamar
        3 - Historial de llamadas de un Cliente
        0 - Salir \n\n            
        """))

        if menu=='1':
            os.system("cls")
            try: 
                nro = int(input('Ingrese el teléfono del cliente del cual desea obtener la factura: ')) 
                print('Ingrese un mes del 1 al 12 siendo: ')
                mes = int(input('1-En 2-Feb 3-Mar 4-Abr 5-May 6-Jun 7-Jul 8-Agos 9-Sep 10-Oct 11-Nov 12-Dic: '))
                if (mes == 0 or mes > 12): 
                    print(' -------------- Ingreso incorrecto de datos ------------------- ')
                    input('Presione /Enter/ para volver al menu...')
                    pass
                else:
                    os.system("cls")
                    unaFacturacion.imprimir_facturas(nro, mes) 
                    input('                 Presione /Enter/ para continuar...')
            except ValueError:
                print(' -------------- Ingreso incorrecto de datos ------------------- ')
                input('Presione /Enter/ para continuar...')
                pass
        elif menu=='2':  #Pido el ingreso por teclado de los atributos del numero telefonico de origen y destino de la llamada
            os.system("cls")
            pais_origen=input('Ingrese el codigo del pais del numero origen:   +')
            ciudad_origen =input('Ingrese el codigo de area del numero origen: ')
            numero_origen =input('Termine de discar el numero: ')
            nO='+'+str(pais_origen)+' - '+str(ciudad_origen)+' - '+str(numero_origen)
            numero_origen = NumeroTel(pais_origen, ciudad_origen, numero_origen)
            pais_destino=input('Ingrese el codigo del pais del numero al que desea llamar:  +')
            ciudad_destino =input('Ingrese el codigo de area del numero destion: ')
            numero_destino =input('Termine de discar el numero: ')
            nD='+'+str(pais_destino)+' - '+str(ciudad_destino)+' - '+str(numero_destino)
            numero_destino = NumeroTel(pais_destino, ciudad_destino, numero_destino)
            #Se guardan los atributos de un objeto llamada
            llamada = Llamada(numero_origen, numero_destino)
            llamada.llamar()
            #Se inicia la llamada (Se guarda la fecha y hora de inicio)
            print('')
            print('Conectando llamada:     ')
            time.sleep(2)  #Solamente utilizo esta funcion para simular la espera en conexión de una llamada
            print('')
            print(     nO, '   ------->   ', nD     )
            time.sleep(2)
            print('')
            #Una vez que la conexion se realiza agrego una llamada a la lista de llamadas
            unaFacturacion.agregar_llamada(llamada)
            input ('Llamada exitosa----------Llamando----------para Cortar presione /Enter/ ')
            llamada.cortar()
        elif menu == '3':
            os.system("cls")
            try:
                nro = int(input('Ingrese el numero del cliente que desea obtener la factura: '))
                print('Ingrese un mes del 1 al 12 siendo: ')
                mes = int(input('1-En 2-Feb 3-Mar 4-Abr 5-May 6-Jun 7-Jul 8-Agos 9-Sep 10-Oct 11-Nov 12-Dic: '))
                if (mes == 0 or mes > 12): 
                    print(' -------------- Ingreso incorrecto de datos ------------------- ')
                    input('Presione /Enter/ para volver al menu...')
                    pass
                else:
                    os.system("cls")
                    unaFacturacion.imprimir_llamadas(nro, mes)  
                    pass         
            except ValueError:
                print(' -------------- Ingreso incorrecto de datos ------------------- ')
                input('Presione /Enter/ para continuar...')
                pass
        elif menu == '0':
            return False
        else:
            print('                 ------------------------Opcion no válida-----------------------')
            print('')
            input('                 Presione /Enter/ para continuar...')
            os.system("cls")


if __name__ == '__main__':
    main()
