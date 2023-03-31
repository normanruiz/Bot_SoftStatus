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
# ARCHIVO             : source.py
# AUTOR               : Norman Ruiz.
# COLABORADORES       : No aplica.
# VERSION             : 1.00 estable.
# FECHA DE CREACION   : 16/11/2022.
# ULTIMA ACTUALIZACION: 16/11/2022.
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
#             Este archivo incluye la definicion del modulo source.
#
#             Las funciones source permiten la manipulacion de datos en desde
#             las bases de datos de origen.
#
#-------------------------------------------------------------------------------
# ARCHIVO DE CABECERA: No aplica
#
# FUNCIONES DEFINIDAS:
#==============================================================================|
#     NOMBRE     |  TIPO  |                    ACCION                          |
#================+========+====================================================|
# Cargar()       | dict | Carga la configuracion desde un archivo json.        |
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

#*****************************************************************************
#                             INCLUSIONES PERSONALES
#=============================================================================
import files_bot.logger as log
import files_bot.conection as conection

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
# FUNCION   : dict/bool Recolectar().
# ACCION    : .
# PARAMETROS: void, no recibe nada.
# DEVUELVE  : dict, la configuracion del bot,
#             bool, False si no encuentra nada o algo sale mal.
#---------------------------------------------------------------------------

def Recolectar(config):
    dataset_aux = []
    campos_aux = []
    dataset = {}
    conexion = False
    ubicacion = "ConfigPal"
    consulta = config["parametros"]["conexiones"][ubicacion]["select"]
    plataformas = ['Paystore Newland', 'Paystore Pax']
    try:
        mensaje = "Cargando nuevo set de datos..."
        print("  " + mensaje)
        log.Escribir_log(mensaje)

        conexion = conection.Conectar(config, ubicacion)
        dataset_aux = conection.Ejecutar_consulta(conexion, ubicacion, consulta)
        conection.Desconectar(conexion, ubicacion)

        for registro in dataset_aux:
            for campo in registro:
                campos_aux.append(None if campo is None else str(campo).replace('\t', '').replace('\n', ''))
            if campos_aux[5] in plataformas:
                campos_aux[1] = None
                campos_aux[2] = None
                campos_aux[3] = None
                campos_aux[4] = None
                campos_aux[7] = None
                campos_aux[8] = None
                campos_aux[9] = None
                dataset[campos_aux[0]] = campos_aux[1:]
            else:
                dataset[campos_aux[0]] = campos_aux[1:]
            campos_aux.clear()

        mensaje = "Subproceso finalizado..."
        print(" ", mensaje)
        log.Escribir_log(mensaje)
    except Exception as excepcion:
        dataset = False
        mensaje = "ERROR - Cargando nuevo set de datos: " + str(excepcion)
        print(" ", mensaje)
        log.Escribir_log(mensaje)
        mensaje = " " + "-" * 128
        print(mensaje)
        log.Escribir_log(mensaje, False)
        mensaje = "WARNING!!! - Subproceso interrumpido..."
        print(" ", mensaje)
        log.Escribir_log(mensaje)
    finally:
        mensaje = " " + "-" * 128
        print(mensaje)
        log.Escribir_log(mensaje, False)
        return dataset


#---------------------------------------------------------------------------
# FUNCION   :
# ACCION    :
# PARAMETROS:
# DEVUELVE  :
#---------------------------------------------------------------------------

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
