##############################################################################
# ARCHIVO             : bot.py
# AUTOR/ES            : Ruiz Norman
# VERSION             : 1.00 estable.
# FECHA DE CREACION   : 14/11/2022.
# ULTIMA ACTUALIZACION: 16/11/2022.
# LICENCIA            : GPL (General Public License) - Version 3.
#  **************************************************************************
#  * El software libre no es una cuestion economica sino una cuestion etica *
#  **************************************************************************
#
# Este programa es software libre;  puede redistribuirlo  o  modificarlo bajo
# los terminos de la Licencia Publica General de GNU  tal como se publica por
# la  Free Software Foundation;  ya sea la version 3 de la Licencia,  o (a su
# eleccion) cualquier version posterior.
#
# Este programa se distribuye con la esperanza  de que le sea util,  pero SIN
# NINGUNA  GARANTIA;  sin  incluso  la garantia implicita de MERCANTILIDAD  o
# IDONEIDAD PARA UN PROPOSITO PARTICULAR.
#
# Vea la Licencia Publica General GNU para mas detalles.
#
# Deberia haber recibido una copia de la Licencia Publica General de GNU junto
# con este proyecto, si no es asi, escriba a la Free Software Foundation, Inc,
# 59 Temple Place - Suite 330, Boston, MA 02111-1307, EE.UU.

#=============================================================================
# SISTEMA OPERATIVO   : Linux NT-9992031 4.4.0-19041-Microsoft #1237-Microsoft Sat Sep 11 14:32:00 PST 2021 x86_64 GNU/Linux.
# IDE                 : VIM - Vi IMproved 8.2 (2019 Dec 12, compiled Oct 01 2021 01:51:08)
# COMPILADOR          : Python 3.9.2
# LICENCIA            : GPL (General Public License) - Version 3.
#=============================================================================
# DESCRIPCION:
#              Bot de recoleccion y actualizacion de la tabla de reporteria de software de terminales.
#
#/////////////////////////////////////////////////////////////////////////////

#*****************************************************************************
#                       CONFIGURACION MULTIPLATAFORMA
#=============================================================================
# COMPILACION EN WINDOWS
#-----------------------------------------------------------------------------
# Si este programa se va a compilar en Windows, descomente las tres lineas
# siguientes, y comente las tres lineas de "COMPILACION EN LINUX".
#-----------------------------------------------------------------------------

# Sin especificar

#=============================================================================
# COMPILACION EN LINUX
#-----------------------------------------------------------------------------
# Si este programa se va a compilar en Linux, descomente las tres lineas
# siguientes, y comente las tres lineas de "COMPILACION EN WINDOWS".
#-----------------------------------------------------------------------------

# Sin especificar

#*****************************************************************************
#                             DECLARACIONES GLOBALES
#=============================================================================

# Sin especificar

#*****************************************************************************
#                             INCLUSIONES ESTANDAR
#=============================================================================
import os

#*****************************************************************************
#                             INCLUSIONES PERSONALES
#=============================================================================
import files_bot.logger as log
import files_bot.config as configuracion
import files_bot.source as source
import files_bot.destiny as destiny
import files_bot.filter as filter
import files_bot.action as action

#==============================================================================
# DECLARACION DEL ESPACIO DE NOMBRES POR DEFECTO
#------------------------------------------------------------------------------

# Sin especificar

#==============================================================================
# FUNCION PRINCIPAL - PUNTO DE INICIO DEL PROYECTO
#------------------------------------------------------------------------------
def main():
    status_code = 0
    try:
        os.system('clear')
        parametros = None
        status = True

        mensaje = " " + "=" * 128
        print(mensaje)
        log.Escribir_log(mensaje, False)
        mensaje = "Iniciando SoftStatus's Bot..."
        print("  " + mensaje)
        log.Escribir_log(mensaje)
        mensaje = " " + "~" * 128
        print(mensaje)
        log.Escribir_log(mensaje, False)

        # Cargo la configuracion desde un archivo
        if status:
            config = configuracion.Cargar()
            if not(config):
                status = False
            else:
                status = config["parametros"]["bot"]["estado"]

        # Carga de datos
        if status:
            datosOrigen = source.Recolectar(config)
            if not(datosOrigen):
                status = False

        if status:
            datosRepositorio = destiny.Recolectar(config)
            if datosRepositorio == False:
                status = False

        # Generacion de lote de registros
        if status:
            loteRegistros = filter.generar_lote(datosOrigen, datosRepositorio)
            if loteRegistros == False:
                status = False

        # Persistencia de datos
        if status:
            status = action.persistir_datos(config, loteRegistros)

        # Generando historial
        if status:
            status = action.generar_historial(config)

    except Exception as excepcion:
        status_code = 1
        mensaje = " " + "-" * 128
        print(mensaje)
        log.Escribir_log(mensaje, False)
        mensaje = "ERROR - Ejecucion principal: " + str(excepcion)
        print("  " + mensaje)
        log.Escribir_log(mensaje)
    finally:
        if not(status):
            mensaje = " " + "-" * 128
            print(mensaje)
            log.Escribir_log(mensaje, False)
            mensaje = "WARNING!!! - Proceso principal interrumpido, no se realizaran mas acciones..."
            print("  ", mensaje)
            log.Escribir_log(mensaje)

        mensaje = " " + "~" * 128
        print(mensaje)
        log.Escribir_log(mensaje, False)
        mensaje = "Finalizando SoftStatus's Bot..."
        print("  " + mensaje)
        log.Escribir_log(mensaje)
        mensaje = " " + "=" * 128
        print(mensaje)
        log.Escribir_log(mensaje, False)
        print()
        return status_code

#==============================================================================
# LLAMADA DE INICIO
#------------------------------------------------------------------------------
main()

#=============================================================================
#                            FIN DE ARCHIVO
##############################################################################
