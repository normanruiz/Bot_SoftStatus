import xmltodict

from Modelo.ApiSalesforce import ApiSalesforce
from Modelo.Configuracion import Autor, Bot, ConexionSQLServer, Configuracion, ConexionMySQL
from Servicio.decrypt import decifrar



class ServiciosConfiguracion:
    def __init__(self):
        self._configuracion = Configuracion()

    @property
    def configuracion(self):
        return self._configuracion

    def cargar(self, servicioslog):
        estado = True
        try:
            mensaje = f"Cargando configuracion..."
            servicioslog.escribir(mensaje)
            with open(self.configuracion.configfile, 'r', encoding='utf8') as xmlfile:
                xmlconfig = xmlfile.read()
                config = xmltodict.parse(xmlconfig)
                autor = Autor(config["parametros"]["bot"]["autor"]["nombre"],
                              config["parametros"]["bot"]["autor"]["correo"])
                bot = Bot(config["parametros"]["bot"]["nombre"],
                          True if config["parametros"]["bot"]["estado"] == 'True' else False,
                          int(config["parametros"]["bot"]["hilos"]), autor)
                self.configuracion.bot = bot
                conexion_termianlstatus = \
                    ConexionSQLServer(config["parametros"]["conexiones"]["select_terminalstatus_instaladas"]["driver"],
                             config["parametros"]["conexiones"]["select_terminalstatus_instaladas"]["server"],
                             config["parametros"]["conexiones"]["select_terminalstatus_instaladas"]["database"],
                             config["parametros"]["conexiones"]["select_terminalstatus_instaladas"]["username"],
                             config["parametros"]["conexiones"]["select_terminalstatus_instaladas"]["password"],
                             config["parametros"]["conexiones"]["select_terminalstatus_instaladas"]["select"],
                             None,
                             None)
                self.configuracion.conexiones.append(conexion_termianlstatus)
                conexion_coredownloadlog_data_soft = \
                    ConexionSQLServer(config["parametros"]["conexiones"]["select_coredownloadlog_data_soft"]["driver"],
                             config["parametros"]["conexiones"]["select_coredownloadlog_data_soft"]["server"],
                             config["parametros"]["conexiones"]["select_coredownloadlog_data_soft"]["database"],
                             config["parametros"]["conexiones"]["select_coredownloadlog_data_soft"]["username"],
                             config["parametros"]["conexiones"]["select_coredownloadlog_data_soft"]["password"],
                             config["parametros"]["conexiones"]["select_coredownloadlog_data_soft"]["select"],
                             None,
                             None)
                self.configuracion.conexiones.append(conexion_coredownloadlog_data_soft)
                conexion_automatizacion_medio_comunicacion = \
                    ConexionSQLServer(config["parametros"]["conexiones"]["select_automatizacion_medio_comunicacion"]["driver"],
                             config["parametros"]["conexiones"]["select_automatizacion_medio_comunicacion"]["server"],
                             config["parametros"]["conexiones"]["select_automatizacion_medio_comunicacion"]["database"],
                             config["parametros"]["conexiones"]["select_automatizacion_medio_comunicacion"]["username"],
                             config["parametros"]["conexiones"]["select_automatizacion_medio_comunicacion"]["password"],
                             config["parametros"]["conexiones"]["select_automatizacion_medio_comunicacion"]["select"],
                             None,
                             None)
                self.configuracion.conexiones.append(conexion_automatizacion_medio_comunicacion)
                conexion_lapostecno_tabla_versiones = \
                    ConexionSQLServer(config["parametros"]["conexiones"]["select_lapostecno_tabla_versiones"]["driver"],
                             config["parametros"]["conexiones"]["select_lapostecno_tabla_versiones"]["server"],
                             config["parametros"]["conexiones"]["select_lapostecno_tabla_versiones"]["database"],
                             config["parametros"]["conexiones"]["select_lapostecno_tabla_versiones"]["username"],
                             config["parametros"]["conexiones"]["select_lapostecno_tabla_versiones"]["password"],
                             config["parametros"]["conexiones"]["select_lapostecno_tabla_versiones"]["select"],
                             None,
                             None)
                self.configuracion.conexiones.append(conexion_lapostecno_tabla_versiones)
                datos_desifrados = decifrar()
                conexion_terminals_meters_all = \
                    ConexionMySQL(datos_desifrados["servidor"],
                             config["parametros"]["conexiones"]["select_terminals_meters_all"]["port"],
                             config["parametros"]["conexiones"]["select_terminals_meters_all"]["database"],
                             datos_desifrados["usuario"],
                             datos_desifrados["password"],
                             config["parametros"]["conexiones"]["select_terminals_meters_all"]["select"],
                             None,
                             None)
                self.configuracion.conexiones.append(conexion_terminals_meters_all)

                api_salesforce = ApiSalesforce(config["parametros"]["conexiones"]["api_salesforce"]["org"],
                                               config["parametros"]["conexiones"]["api_salesforce"]["client_id"],
                                               config["parametros"]["conexiones"]["api_salesforce"]["client_secret"],
                                               config["parametros"]["conexiones"]["api_salesforce"]["username"],
                                               config["parametros"]["conexiones"]["api_salesforce"]["password"],
                                               config["parametros"]["conexiones"]["api_salesforce"]["version"],
                                               config["parametros"]["conexiones"]["api_salesforce"]["select"])
                self.configuracion.conexiones.append(api_salesforce)

                conexion_soft_status = \
                    ConexionMySQL(config["parametros"]["conexiones"]["select_terminals_soft_status"]["host"],
                             config["parametros"]["conexiones"]["select_terminals_soft_status"]["port"],
                             config["parametros"]["conexiones"]["select_terminals_soft_status"]["database"],
                             config["parametros"]["conexiones"]["select_terminals_soft_status"]["username"],
                             config["parametros"]["conexiones"]["select_terminals_soft_status"]["password"],
                             config["parametros"]["conexiones"]["select_terminals_soft_status"]["select"],
                             config["parametros"]["conexiones"]["select_terminals_soft_status"]["insert"],
                             config["parametros"]["conexiones"]["select_terminals_soft_status"]["update"],
                             config["parametros"]["conexiones"]["select_terminals_soft_status"]["delete"],
                             config["parametros"]["conexiones"]["select_terminals_soft_status"]["history"],)
                self.configuracion.conexiones.append(conexion_soft_status)

            mensaje = f"Configuracion cargada correctamente..."
            servicioslog.escribir(mensaje)
            mensaje = f"Subproceso finalizado..."
            servicioslog.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Cargando configuracion: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            servicioslog.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            servicioslog.escribir(mensaje, tiempo=False)
            return estado