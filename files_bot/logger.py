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
# ARCHIVO             : logger.py
# AUTOR               : Norman Ruiz.
# COLABORADORES       : No aplica.
# VERSION             : 1.00 estable.
# FECHA DE CREACION   : 06/05/2022.
# ULTIMA ACTUALIZACION: 14/11/2022.
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
#              Bot de recoleccion y actualizacion de la tabla de reporteria de software de terminales.
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
import os
from datetime import date
import time

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
def Verificar_archivo_log():
    estado = True
    fecha = str(date.today())
    carpeta_log = os.path.join(".", "files_log")
    archivo_log = "log-" + fecha + ".txt"
    filename = os.path.join(carpeta_log, archivo_log)
    file_log = None

    try:
        if not os.path.exists(carpeta_log):
            os.mkdir(carpeta_log)
        if not os.path.exists(filename):
            Crear_archivo(filename)
    except Exception as excepcion:
        estado = False

    finally:
        if not file_log is None:
            file_log.close()
        return estado

#---------------------------------------------------------------------------
# FUNCION   : bool Escribir_log(str).
# ACCION    : Escribe una linea con un mensaje en el archivo de logs.
# PARAMETROS: str, la cadena a escribir en el log.
# DEVUELVE  : void, no devuelve nada.
#---------------------------------------------------------------------------
def Crear_archivo(filename):
    file_log = open(filename, "x")
    file_log.write(" " + "=" * 128 + "\n")
    file_log.write("  " + str(date.today()) + " - Archivo de log generado\n")

#---------------------------------------------------------------------------
# FUNCION   : bool Escribir_log(str).
# ACCION    : Escribe una linea con un mensaje en el archivo de logs.
# PARAMETROS: str, la cadena a escribir en el log.
# DEVUELVE  : void, no devuelve nada.
#---------------------------------------------------------------------------
def Escribir_log(mensaje, tiempo = True):
    estado = True
    fecha = str(date.today())
    hora = time.strftime('%H:%M:%S', time.localtime())
    carpeta_log = os.path.join(".", "files_log")
    archivo_log = "log-" + fecha + ".txt"
    filename = os.path.join(carpeta_log, archivo_log)
    file_log = None
    try:
        Verificar_archivo_log()
        file_log = open(filename, 'a')
        if tiempo:
            registro = "  " + hora + " " + mensaje + "\n"
        else:
            registro = mensaje + "\n"
        file_log.write(registro)

    except Exception as excepcion:
        estodo = False
        print("  ERROR - Escribiendo log:", str(excepcion))

    finally:
        if not file_log is None:
            file_log.close()
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
