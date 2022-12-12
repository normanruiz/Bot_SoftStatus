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
# Avis Software es marca registrada.
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
# ARCHIVO             : conection.py
# AUTOR               : Norman Ruiz.
# COLABORADORES       : No aplica.
# VERSION             : 1.00 estable.
# FECHA DE CREACION   : 11/05/2022.
# ULTIMA ACTUALIZACION: 20/07/2022.
# LICENCIA            : GPL (General Public License) - Version 3.
#=============================================================================
# SISTEMA OPERATIVO   : Linux NT-9992031 4.4.0-19041-Microsoft
#               #488-Microsoft Mon Sep 01 13:43:00 PST 2020 x86_64 GNU/Linux.
# IDE                 : Atom 1.60.0.
# COMPILADOR          : Python 3.9.2.
# LICENCIA            : GPL (General Public License) - Version 3.
#=============================================================================
# DEDICATORIA: A mi hija Micaela Ruiz que me re aguanta.
#=============================================================================
# DESCRIPCION:
#             Este archivo incluye la definicion del modulo conection.
#
#             Las funciones conection permiten la iteraccion con la
#             base de datos.
#
#-------------------------------------------------------------------------------
# ARCHIVO DE CABECERA: No aplica
#
# FUNCIONES DEFINIDAS:
#==============================================================================|
#     NOMBRE     |  TIPO  |                    ACCION                          |
#================+========+====================================================|
# Conectar() |  Objeto  | Abre una conexion con la base de datos y retorna     |
#              conexion    el objeto de dicha conexion.                        |
#----------------+--------+----------------------------------------------------|
# Desconectar() | bool | Cierra la conexion contra la base de datos.           |
#----------------+--------+----------------------------------------------------|
# Ejecutar_consulta_origen() | dict | Ejecutra la query contra la base de      |
#                              datos que genera el listado de terminales con   |
#                              sus respectivas rerogramaciones pendientes.     |
#----------------+--------+----------------------------------------------------|
# Ejecutar_consulta_destino() | dict | Ejecutra la query contra la base de     |
#                              datos que genera el listado de terminales ya    |
#                              presentes en el circuito de la automatizacion.  |
#----------------+--------+----------------------------------------------------|
# Insertar_nuevos() | int | Ejecutra la nonquery contra la base de             |
#                              datos que inserta las nuevas terminales al      |
#                              circuito de la automatizacion.                  |
#----------------+--------+----------------------------------------------------|
# Actualizar_existentes() | int | Ejecutra la nonquery contra la base de       |
#                              datos que actualioza el contador de solicitudes |
#                              de las terminales ya presentes en el circuito   |
#                              de la automatizacion.                           |
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
import pyodbc
import files_bot.logger as log

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
# FUNCION   : objeto_conexion Conectar(dict, str).
# ACCION    : Abre la coneccion contra la base de datos.
# PARAMETROS:  dict, parametros de configuracion del bot.
#      str, una cadena/bandera indicando a que base de datos debe conectarse.
# DEVUELVE  : objeto conexion.
#---------------------------------------------------------------------------
def Conectar(configuracion, ubicacion):
    conexion = False
    try:
        mensaje = "Conectando a base de datos " + ubicacion + "..."
        log.Escribir_log(mensaje)
        cadena_de_conexion = 'DRIVER=' + configuracion["parametros"]["conexiones"][ubicacion]["driver"] + ';SERVER=' + configuracion["parametros"]["conexiones"][ubicacion]["server"] + ';DATABASE=' + configuracion["parametros"]["conexiones"][ubicacion]["database"] + ';UID=' + configuracion["parametros"]["conexiones"][ubicacion]["username"] + ';PWD=' + configuracion["parametros"]["conexiones"][ubicacion]["password"] + ';TrustServerCertificate=yes'
        conexion = pyodbc.connect(cadena_de_conexion)
        mensaje = "Conexion establecida con base de datos " + ubicacion + "..."
        log.Escribir_log(mensaje)
    except Exception as excepcion:
        mensaje = "ERROR - Conectando a base de datos " + ubicacion + ": " + str(excepcion)
        print(" ", mensaje)
        log.Escribir_log(mensaje)
    finally:
        return conexion

#---------------------------------------------------------------------------
# FUNCION   : bool Desconectar(objeto_conexion, str)
# ACCION    : Cierra la conexion contra la base de datos
# PARAMETROS: objeto_conexion, la conexion que debe cerrarse
#      str, una cadena/bandera indicando a que base de datos debe conectarse.
# DEVUELVE  : bool, el estado en True si termino sin errores
#                    y False caso contrario
#---------------------------------------------------------------------------
def Desconectar(conexion, ubicacion):
    status = False
    try:
        mensaje = "Cerrando conexion con base de datos: " + ubicacion + "..."
        log.Escribir_log(mensaje)
        conexion.close()
        status = True
        mensaje = "Conexion a base de datos: " + ubicacion + " cerrada..."
        log.Escribir_log(mensaje)
    except Exception as excepcion:
        mensaje = "ERROR - Cerrando conexion a base de datos:" + ubicacion + ": " + str(excepcion)
        log.Escribir_log(mensaje)
    finally:
        return status

#---------------------------------------------------------------------------
# FUNCION   : dict Ejecutar_consulta_origen(objeto_conexion, str, str)
# ACCION    : Consulta la base de datos para recuperar las terminales con
#             repros pendientes.
# PARAMETROS: objeto_conexion, la conexion a utilizar
#             str, la base de datos a donde apuntar
#             str, la query que se ejecutara
# DEVUELVE  : dict, coleccion de terminales y sus respectivas repros
#---------------------------------------------------------------------------
def Ejecutar_consulta(conexion, ubicacion, consulta):
    data = []
    aux_terminal = None
    cursor = None
    try:
        mensaje = "Ejecutando query contra " + ubicacion + "..."
        log.Escribir_log(mensaje)
        mensaje = "Query: " + consulta
        log.Escribir_log(mensaje)
        mensaje = "Generando cursor..."
        log.Escribir_log(mensaje)
        cursor = conexion.cursor()

        mensaje = "Comenzando lectura de datos..."
        log.Escribir_log(mensaje)
        cursor.execute(consulta)
        registro = cursor.fetchone()
        while registro:
            data.append(registro)
            registro = cursor.fetchone()
        mensaje = "Lectura de datos finalizada..."
        log.Escribir_log(mensaje)

    except Exception as excepcion:
        mensaje = "ERROR - Ejecutando query :" + str(excepcion)
        print("  " + mensaje)
        log.Escribir_log(mensaje)
    finally:
        if cursor:
            cursor.close()
            mensaje = "Destruyendo cursor..."
            log.Escribir_log(mensaje)
        return data

#---------------------------------------------------------------------------
# FUNCION   : dict Ejecutar_consulta_destino(objeto_conexion, str, str)
# ACCION    : Consulta la base de datos para recuperar las terminales ya
#             dentro del circuitod e automatizacion.
# PARAMETROS: objeto_conexion, la conexion a utilizar
#             str, la base de datos a donde apuntar
#             str, la query que se ejecutara
# DEVUELVE  : dict, coleccion de terminales y su cantidad de solicitudes
#---------------------------------------------------------------------------
def Ejecutar_consulta_destino(conexion, ubicacion, consulta):
    data = {}
    aux_terminal = None
    aux_repro = []
    estados = ['Solicitado', 'Fallido']
    cursor = None
    try:
        mensaje = "Ejecutando query contra " + ubicacion + "..."
        log.Escribir_log(mensaje)
        mensaje = "Query: " + consulta
        log.Escribir_log(mensaje)
        mensaje = "Generando cursor..."
        log.Escribir_log(mensaje)
        cursor = conexion.cursor()
        mensaje = "Comenzando lectura de datos..."
        log.Escribir_log(mensaje)
        cursor.execute(consulta)
        registro = cursor.fetchone()
        if registro:
            aux_terminal = str(registro[0])
            if str(registro[2]) in estados:
                aux_repro.append('U')
            else:
                aux_repro.append('I')
            while registro:
                if aux_terminal == str(registro[0]):
                    aux_repro.append(int(registro[1]))
                else:
                    data[aux_terminal] = list(aux_repro)
                    aux_terminal = str(registro[0])
                    aux_repro.clear()
                    if str(registro[2]) in estados:
                        aux_repro.append('U')
                    else:
                        aux_repro.append('I')
                    aux_repro.append(registro[1])
                registro = cursor.fetchone()
            data[aux_terminal] = list(aux_repro)
        mensaje = "Lectura de datos finalizada..."
        log.Escribir_log(mensaje)
    except Exception as excepcion:
        print("  ERROR - Ejecutando consulta a destino:", excepcion)
        mensaje = "ERROR - Ejecutando query :" + str(excepcion)
        log.Escribir_log(mensaje)
    finally:
        if cursor:
            cursor.close()
            mensaje = "Destruyendo cursor..."
            log.Escribir_log(mensaje)
        return data

#---------------------------------------------------------------------------
# FUNCION   : int Insertar_nuevos(objeto_conexion, objeto_cursor, str, str, int)
# ACCION    : Ejecutra la nonquery contra la base de datos que inserta las
#             nuevas terminales al circuito de la automatizacion.
# PARAMETROS: objeto_conexion, la conexion a utilizar
#             objeto_cursor, el cursor para la ejecucion del nonquery
#             str, la cadena con el insert a realizar
#             str, la terminla a insertar
#             int, la prioridad a setear
# DEVUELVE  : int, 1 si se inserto el campo, 0 si fallo
#---------------------------------------------------------------------------
def Insertar_nuevos(conexion, cursor, nonquery_i, terminal, prioridad):
    status = 0
    try:
        count = cursor.execute(nonquery_i, terminal, prioridad).rowcount
        conexion.commit()
        if count == 1:
            status = 1
    except Exception as excepcion:
        mensaje = "ERROR - Insertando nuevo registro: Terminal " + Terminal + "..."
        log.Escribir_log(mensaje)
        mensaje = "ERROR - Insertando nuevo registro: " + excepcion
        log.Escribir_log(mensaje)
        print(" ", mensaje)
    finally:
        return status

#---------------------------------------------------------------------------
# FUNCION   : int Actualizar_existentes(conexion, cursor, nonquery_u, terminal, solicitudes)
# ACCION    : Ejecutra la nonquery contra la base de datos que actualioza el
#             contador de solicitudes de las terminales ya presentes en el
#             circuito de la automatizacion.
# PARAMETROS: objeto_conexion, la conexion a utilizar
#             objeto_cursor, el cursor para la ejecucion del nonquery
#             str, la cadena con el update a realizar
#             str, la terminla a actualizar
#             int, el numero de solicitures a setear
# DEVUELVE  : int, 1 si se actualizo el campo, 0 si fallo
#---------------------------------------------------------------------------
def Actualizar_existentes(conexion, cursor, nonquery_u, terminal, solicitudes):
    status = 0
    try:
        count = cursor.execute(nonquery_u, solicitudes, terminal).rowcount
        conexion.commit()
        if count == 1:
            status = 1
    except Exception as excepcion:
        mensaje = "ERROR - Actualizando registro existente: Terminal " + Terminal + "..."
        log.Escribir_log(mensaje)
        mensaje = "ERROR - Actualizando registro existente: " + excepcion
        log.Escribir_log(mensaje)
        print(" ", mensaje)
    finally:
        return status

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
