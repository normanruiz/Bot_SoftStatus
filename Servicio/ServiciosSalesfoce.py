from Servicio.ConexionAPI import ConexionAPI


class ServiciosSalesforce:
    def __init__(self, log, configuracion):
        self._log = log
        self._configuracion = configuracion
        self._terminales = {}

    @property
    def log(self):
        return self._log

    @property
    def configuracion(self):
        return self._configuracion

    @property
    def terminales(self):
        return self._terminales

    @terminales.setter
    def terminales(self, terminales):
        self._terminales = terminales

    def buscarterminales(self):
        estado = True
        datos = {}
        try:
            mensaje = f"Recuperando datos de Salesforce..."
            self.log.escribir(mensaje)

            datos_api = self.configuracion.conexiones[5]
            api_salesforce = ConexionAPI(self.log)
            api_salesforce.autenticarse(datos_api)
            datos = api_salesforce.consultar()
            if datos is False:
                raise Exception('Fallo la recoleccion de datos.')

            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Recuperando datos de Salesforce: {type(excepcion)} - {str(excepcion)}"
            self.log.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            self.log.escribir(mensaje)
        finally:
            return (estado, datos)
