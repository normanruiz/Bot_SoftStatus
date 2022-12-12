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
# ARCHIVO             : filter.py
# AUTOR               : Norman Ruiz.
# COLABORADORES       : No aplica.
# VERSION             : 1.00 estable.
# FECHA DE CREACION   : 12/12/2022.
# ULTIMA ACTUALIZACION: 12/12/2022.
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
#             Este archivo incluye la definicion del modulo filter.
#
#             Las funciones filter permiten la del nuevo lote de registros a
#             manipular en la tabla de destino e historial
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
def generar_lote(config, datosOrigen, datosRepositorio):
    estado = True
    lote = {}
    create = 0
    update = 0
    delete = 0

    try:
        mensaje = "Generando lote de registros a persistir..."
        print("  " + mensaje)
        log.Escribir_log(mensaje)

        for terminal in datosRepositorio:
            if terminal not in datosOrigen:
                lote[terminal] = ['d', None]
                delete += 1

        for terminal, campos in datosOrigen.items():
            if terminal not in datosRepositorio:
                lote[terminal] = ['c', campos]
                create += 1
            elif campos[2] !=  datosRepositorio[terminal][2]:
                lote[terminal] = ['u', campos]
                update += 1

        mensaje = "Registros a crear: " + str(create)
        print(" ", mensaje)
        log.Escribir_log(mensaje)
        mensaje = "Registros a actualizar: " + str(update)
        print(" ", mensaje)
        log.Escribir_log(mensaje)
        mensaje = "Registros a eliminar: " + str(delete)
        print(" ", mensaje)
        log.Escribir_log(mensaje)

        mensaje = "Subproceso finalizado..."
        print(" ", mensaje)
        log.Escribir_log(mensaje)

    except Exception as excepcion:
        estado = False
        mensaje = "ERROR - Generando lote de registros: " + str(excepcion)
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
        if estado:
            return lote
        else:
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
