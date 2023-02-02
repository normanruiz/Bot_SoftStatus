##############################################################################
#                             AVIS SOFTWARE                                  #
#                     (Productos de Software Libre)                          #
#                                                                            #
##############################################################################
#
#  **************************************************************************
#  * El software libre no es una cuestion economica sino una cuestion etica *
#  **************************************************************************
#
# Avis Software es marca registrada.4
#
# Este programa es software libre; puede redistribuirlo o modificarlo bajo los
# terminos de la Licencia Publica General de GNU tal como se publica por la
# Free Software Foundation; ya sea la version 3 de la Licencia, o (a su
# eleccion) cualquier version posterior.
#
# Este programa se distribuye con la esperanza de que le sea util, pero SIN
# NINGUNA GARANTIA; sin incluso la garantia implicita de MERCANTILIDAD o
# IDONEIDAD PARA UN PROPOSITO PARTICULAR.
#
# Vea la Licencia Publica General GNU para mas detalles.
#
# Deberia haber recibido una copia de la Licencia Publica General de GNU
# junto con este programa, si no es asi, escriba a la Free Software Foundation,
# Inc, 59 Temple Place - Suite 330, Boston, MA 02111-1307, EE.UU.
#
##############################################################################
# ARCHIVO             : action.py
# AUTOR               : Norman Ruiz.
# COLABORADORES       : No aplica.
# VERSION             : 1.00 estable.
# FECHA DE CREACION   : 14/12/2022.
# ULTIMA ACTUALIZACION: 14/12/2022.
# LICENCIA            : GPL (General Public License) - Version 3.
#=============================================================================
# SISTEMA OPERATIVO   : Linux NT-9992031 4.4.0-19041-Microsoft #1237-Microsoft Sat Sep 11 14:32:00 PST 2021 x86_64 GNU/Linux.
# IDE                 : VIM - Vi IMproved 8.2 (2019 Dec 12, compiled Oct 01 2021 01:51:08)
# COMPILADOR          : Python 3.9.2
# LICENCIA            : GPL (General Public License) - Version 3.
#=============================================================================
# DEDICATORIA: A mi hija Micaela Ruiz que me re aguanta.
#=============================================================================
# DESCRIPCION:
#             Este archivo incluye la definicion del modulo action.
#
#             Las funciones action se encargan de organizar la persistencoa
#             de los datos.
#
#-------------------------------------------------------------------------------
# ARCHIVO DE CABECERA: No aplica
#
# FUNCIONES DEFINIDAS:
#==============================================================================|
#     NOMBRE     |  TIPO  |                    ACCION                          |
#================+========+====================================================|
# Verificar_archivo() | void | Verifica si el archivo de log del dia existe y  |
#                             de no ser asi lo genera.                         |
#----------------+--------+----------------------------------------------------|
# Escribir_log   |  void  | Escribe una linea con un mensaje en el rachivo     |
#                           de logs.                                           |
#================+========+====================================================|
#
#-------------------------------------------------------------------------------
# MODIFICACIONES DE LA VERSION 0.01 estable (05/05/2022)
# AUTOR DE LA MODIFICACION: Norman Ruiz.
# * Ejemplo de historial de modificaciones.
#
#-------------------------------------------------------------------------------
#
#///////////////////////////////////////////////////////////////////////////////

#*****************************************************************************
#                             INCLUSIONES ESTANDAR
#=============================================================================
import files_bot.logger as log
import files_bot.conection as data_conection
from threading import Thread

#*****************************************************************************
#                             INCLUSIONES PARA WINDOWS
#=============================================================================

# Sin especificar

#*****************************************************************************
#                             INCLUSIONES PARA LINUX
#=============================================================================

# Sin especificar

#*****************************************************************************
#               ESPACIO DE NOMBRES DE LA LIBRERIA
#=============================================================================

# Sin especificar

#***************************************************************************
#                        FUNCIONES PARA LINUX
#===========================================================================
# FUNCION   : bool verificar_archivo()
# ACCION    : Verifica si el archivo de log del dia existe y
#             de no ser asi lo genera.
# PARAMETROS: void, no recibe nada.
# DEVUELVE  : void, no devuelve nada.
#---------------------------------------------------------------------------
def persistir_datos(config, loteRegistros):
    estado = True
    ubicacion = "LaposTecno"
    insert = config["parametros"]["conexiones"][ubicacion]["insert"]
    update = config["parametros"]["conexiones"][ubicacion]["update"]
    delete = config["parametros"]["conexiones"][ubicacion]["delete"]
    threads = []
    thread = 0
    count = 0
    max_threads = int(config["parametros"]["bot"]["hilos"])
    threadsregistros = {}

    try:
        mensaje = "Anexanado lote de datos..."
        print("  " + mensaje)
        log.Escribir_log(mensaje)

        registros = len(loteRegistros)
        if (registros % max_threads != 0):
            registros += max_threads

        registros_threds = registros // max_threads

        for terminal, campos in loteRegistros.items():
            threadsregistros[terminal] = list(campos)
            count += 1
            if (count == registros_threds):
                thread += 1
                conexion = data_conection.Conectar(config, ubicacion)
                threads.append(Thread(target=Impactar_cambio, args=(conexion, ubicacion, insert, update, delete, dict(threadsregistros), thread)))
                count = 0
                threadsregistros.clear()

        conexion = data_conection.Conectar(config, ubicacion)
        threads.append(Thread(target=Impactar_cambio, args=(conexion, ubicacion, insert, update, delete, dict(threadsregistros), thread)))
        count = 0
        threadsregistros.clear()

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        mensaje = "Subproceso finalizado..."
        print(" ", mensaje)
        log.Escribir_log(mensaje)
        mensaje = " " + "-" * 128
        print(mensaje)
        log.Escribir_log(mensaje, False)

    except Exception as excepcion:
        estado = False
        mensaje = "ERROR - Anexanado lote de datos: " + str(excepcion)
        print(" ", mensaje)
        log.Escribir_log(mensaje)
        mensaje = " " + "-" * 128
        print(mensaje)
        log.Escribir_log(mensaje, False)
        mensaje = "WARNING!!! - Subproceso interrumpido..."
        print(" ", mensaje)
        log.Escribir_log(mensaje)

    finally:
        return estado

#---------------------------------------------------------------------------
# FUNCION   : void Impactar_cambio(objeto_conexion, string, string, string, dict)
# ACCION    : Inserta y/o actualiza el nuevo lote de terminales en el proceso de migracion.
# PARAMETROS: objeto_conexion, la conecion contra la base de datos
#             string, la ubicacion  a la que apunta la conexion
#             string, la nonquery para los insert
#             string, la nonquery para los update
#             dict, el lote de terminales a impactar
# DEVUELVE  : void, no devuelve nada.
#---------------------------------------------------------------------------
def Impactar_cambio(conexion, ubicacion, insertAux, updateAux, deleteAux, sublote, thread):
    estado = True
    try:
        for terminal, campos in sublote.items():
            if campos[0] == 'c':
                insert = insertAux.replace('?1', str("'" + terminal + "'")).replace('?2', 'NULL' if campos[1][0] is None else str("'" + campos[1][0] + "'")).replace('?3', 'NULL' if campos[1][1] is None else str("'" + campos[1][1] + "'")).replace('?4', 'NULL' if campos[1][2] is None else str("'" + campos[1][2] + "'")).replace('?5', 'NULL' if campos[1][3] is None else str("'" + campos[1][3] + "'")).replace('?6', 'NULL' if campos[1][4] is None else str("'" + campos[1][4] + "'")).replace('?7', 'NULL' if campos[1][5] is None else str("'" + campos[1][5] + "'")).replace('?8', 'NULL' if campos[1][6] is None else str("'" + campos[1][6][:-3] + "'"))
                data_conection.Insertar_nuevos(conexion, insert, thread)
            elif campos[0] == 'u':
                update = updateAux.replace('?8', str("'" + terminal + "'")).replace('?1', 'NULL' if campos[1][0] is None else str("'" + campos[1][0] + "'")).replace('?2', 'NULL' if campos[1][1] is None else str("'" + campos[1][1] + "'")).replace('?3', 'NULL' if campos[1][2] is None else str("'" + campos[1][2] + "'")).replace('?4', 'NULL' if campos[1][3] is None else str("'" + campos[1][3] + "'")).replace('?5', 'NULL' if campos[1][4] is None else str("'" + campos[1][4] + "'")).replace('?6', 'NULL' if campos[1][5] is None else str("'" + campos[1][5] + "'")).replace('?7', 'NULL' if campos[1][6] is None else str("'" + campos[1][6][:-3] + "'"))
                data_conection.Actualizar_existentes(conexion, update, thread)
            elif campos[0] == 'd':
                delete = deleteAux.replace('?1', str("'" + terminal + "'"))
                data_conection.Eliminar_existentes(conexion, delete, thread)

    except Exception as excepcion:
        estado = False
        mensaje = "ERROR - Impactando cambio: " + str(excepcion)
        print(" ", mensaje)
        log.Escribir_log(mensaje)
        mensaje = " " + "-" * 128
        print(mensaje)
        log.Escribir_log(mensaje, False)
        mensaje = "WARNING!!! - Subproceso interrumpido..."
        print(" ", mensaje)
        log.Escribir_log(mensaje)

    finally:
        data_conection.Desconectar(conexion, ubicacion)
        return estado

#---------------------------------------------------------------------------
# FUNCION   : void Impactar_cambio(objeto_conexion, string, string, string, dict)
# ACCION    : Inserta y/o actualiza el nuevo lote de terminales en el proceso de migracion.
# PARAMETROS: objeto_conexion, la conecion contra la base de datos
#             string, la ubicacion  a la que apunta la conexion
#             string, la nonquery para los insert
#             string, la nonquery para los update
#             dict, el lote de terminales a impactar
# DEVUELVE  : void, no devuelve nada.
#---------------------------------------------------------------------------
def generar_historial(config):
    estado = True
    conexion = None
    ubicacion = "LaposTecno"
    consulta = config["parametros"]["conexiones"][ubicacion]["sp"]
    try:
        mensaje = "Generando historial..."
        print("  " + mensaje)
        log.Escribir_log(mensaje)

        conexion = data_conection.Conectar(config, ubicacion)
        estado = data_conection.Ejecutar_sp(conexion, ubicacion, consulta)
        data_conection.Desconectar(conexion, ubicacion)

        mensaje = "Subproceso finalizado..."
        print(" ", mensaje)
        log.Escribir_log(mensaje)

    except Exception as excepcion:
        estado = False
        mensaje = "ERROR - Generando historial: " + str(excepcion)
        print(" ", mensaje)
        log.Escribir_log(mensaje)
        mensaje = " " + "-" * 128
        print(mensaje)
        log.Escribir_log(mensaje, False)
        mensaje = "WARNING!!! - Subproceso interrumpido..."
        print(" ", mensaje)
        log.Escribir_log(mensaje)

    finally:
        data_conection.Desconectar(conexion, ubicacion)
        return estado
#***************************************************************************
#                        FUNCIONES PARA WINDOWS
#===========================================================================
# FUNCION   :
# ACCION    :
# PARAMETROS:
# DEVUELVE  :
#---------------------------------------------------------------------------

# Sin especificar

#=============================================================================
#                            FIN DE ARCHIVO
##############################################################################
