from Modelo.Bot import Bot
from Servicio.ServiciosConfiguracion import ServiciosConfiguracion
from Servicio.ServiciosETL import ServiciosETL
from Servicio.ServiciosLog import ServiciosLog


class ServiciosBot:
    def __init__(self):
        self._bot = Bot()

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, bot):
        self._bot = bot

    def iniciar(self):
        servicios_log = None
        try:
            servicios_log = ServiciosLog()
            self.bot.estado = servicios_log.verificar_archivo_log()
            if self.bot.estado is False:
                return

            mensaje = " " + "=" * 128
            servicios_log.escribir(mensaje, tiempo=False)
            mensaje = f"Iniciando Bot Soft Status..."
            servicios_log.escribir(mensaje)
            mensaje = " " + "~" * 128
            servicios_log.escribir(mensaje, tiempo=False)

            servicios_configuracion = ServiciosConfiguracion()
            self.bot.estado = servicios_configuracion.cargar(servicios_log)
            if self.bot.estado is False:
                return
            self.bot.estado = servicios_configuracion.configuracion.bot.estado
            if self.bot.estado is False:
                mensaje = f"Bot apagado por configuracion..."
                servicios_log.escribir(mensaje)
                return

            servicios_etl = ServiciosETL()
            self.bot.estado = servicios_etl.extract(servicios_log, servicios_configuracion.configuracion)
            if self.bot.estado is False:
                return

            self.bot.estado = servicios_etl.transform(servicios_log)
            if self.bot.estado is False:
                return

            self.bot.estado = servicios_etl.load(servicios_log, servicios_configuracion.configuracion.conexiones[6])
            if self.bot.estado is False:
                return

        except Exception as excepcion:
            self.bot.estado = False
            mensaje = f" {'-' * 128}"
            servicios_log.escribir(mensaje, tiempo=False)
            mensaje = f"ERROR - Ejecucion principal: {type(excepcion)} - {str(excepcion)}"
            servicios_log.escribir(mensaje)
        finally:
            if not self.bot.estado:
                mensaje = f" {'-' * 128}"
                servicios_log.escribir(mensaje, tiempo=False)
                mensaje = f"WARNING!!! - Proceso principal interrumpido, no se realizaran mas acciones..."
                servicios_log.escribir(mensaje)
            mensaje = f" {'~' * 128}"
            servicios_log.escribir(mensaje, tiempo=False)
            mensaje = f"Finalizando Bot Soft Status..."
            servicios_log.escribir(mensaje)
            mensaje = f" {'=' * 128}"
            servicios_log.escribir(mensaje, tiempo=False)
            return 0 if self.bot.estado else 1
