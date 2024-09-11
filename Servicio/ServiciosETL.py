from Servicio.ConexionDBSQLServer import ConexionDBSQLServer
from Servicio.ConexionDBMySQL import ConexionDBMySQL
from Servicio.ServiciosAlerta import ServiciosAlerta
from Modelo.Terminal import Terminal
from Servicio.ServiciosSalesfoce import ServiciosSalesforce
import json
from datetime import date
import time

class ServiciosETL:
    def __init__(self, servicios_log, configuracion):
        self._servicios_log = servicios_log
        self._configuracion = configuracion
        self._terminalstatus_installed_terminals = {}
        self._coredownloadlog_data_soft = {}
        self._medio_comunicacion = {}
        self._lapostecno_tabla_versiones = {}
        self._terminals_meters_all = {}
        self._datos_pax_paystore = {}
        self._terminales_softstatus = {}
        self._producto_software_base = {}
        self._producto_software = {}
        self._terminales = {}
        self._terminales_existentes = {}
        self._terminales_insert = {}
        self._terminales_update = {}
        self._terminales_delete = {}

    @property
    def servicios_log(self):
        return self._servicios_log

    @servicios_log.setter
    def servicios_log(self, servicios_log):
        self._servicios_log = servicios_log

    @property
    def configuracion(self):
        return self._configuracion

    @configuracion.setter
    def configuracion(self, configuracion):
        self._configuracion = configuracion

    @property
    def terminalstatus_installed_terminals(self):
        return self._terminalstatus_installed_terminals

    @terminalstatus_installed_terminals.setter
    def terminalstatus_installed_terminals(self, terminalstatus_installed_terminals):
        self._terminalstatus_installed_terminals = terminalstatus_installed_terminals

    @property
    def coredownloadlog_data_soft(self):
        return self._coredownloadlog_data_soft

    @coredownloadlog_data_soft.setter
    def coredownloadlog_data_soft(self, coredownloadlog_data_soft):
        self._coredownloadlog_data_soft = coredownloadlog_data_soft

    @property
    def medio_comunicacion(self):
        return self._medio_comunicacion

    @medio_comunicacion.setter
    def medio_comunicacion(self, medio_comunicacion):
        self._medio_comunicacion = medio_comunicacion

    @property
    def lapostecno_tabla_versiones(self):
        return self._lapostecno_tabla_versiones

    @lapostecno_tabla_versiones.setter
    def lapostecno_tabla_versiones(self, lapostecno_tabla_versiones):
        self._lapostecno_tabla_versiones = lapostecno_tabla_versiones

    @property
    def terminals_meters_all(self):
        return self._terminals_meters_all

    @terminals_meters_all.setter
    def terminals_meters_all(self, terminals_meters_all):
        self._terminals_meters_all = terminals_meters_all

    @property
    def datos_pax_paystore(self):
        return self._datos_pax_paystore

    @datos_pax_paystore.setter
    def datos_pax_paystore(self, datos_pax_paystore):
        self._datos_pax_paystore = datos_pax_paystore

    @property
    def terminales_softstatus(self):
        return self._terminales_softstatus

    @terminales_softstatus.setter
    def terminales_softstatus(self, terminales_softstatus):
        self._terminales_softstatus = terminales_softstatus

    @property
    def producto_software_base(self):
        return self._producto_software_base

    @producto_software_base.setter
    def producto_software_base(self, producto_software_base):
        self._producto_software_base = producto_software_base

    @property
    def producto_software(self):
        return self._producto_software

    @producto_software.setter
    def producto_software(self, producto_software):
        self._producto_software = producto_software

    @property
    def terminales(self):
        return self._terminales

    @terminales.setter
    def terminales(self, terminales):
        self._terminales = terminales

    @property
    def terminales_existentes(self):
        return self._terminales_existentes

    @terminales_existentes.setter
    def terminales_existentes(self, terminales_existentes):
        self._terminales_existentes = terminales_existentes

    @property
    def terminales_insert(self):
        return self._terminales_insert

    @terminales_insert.setter
    def terminales_insert(self, terminales_insert):
        self._terminales_insert = terminales_insert

    @property
    def terminales_update(self):
        return self._terminales_update

    @terminales_update.setter
    def terminales_update(self, terminales_update):
        self._terminales_update = terminales_update

    @property
    def terminales_delete(self):
        return self._terminales_delete

    @terminales_delete.setter
    def terminales_delete(self, terminales_delete):
        self._terminales_delete = terminales_delete

    def extract(self, servicioslog, configuracion):
        estado = True
        try:
            mensaje = f"Iniciando extraccion de datos..."
            servicioslog.escribir(mensaje)

            mensaje = f"Extrayendo listado de terminales instaladas..."
            servicioslog.escribir(mensaje)
            conexion = configuracion.conexiones[0]
            conexion_terminal_status = ConexionDBMySQL(servicioslog)
            estado = conexion_terminal_status.conectar(conexion.host, conexion.port, conexion.database,
                                                   conexion.username, conexion.password)
            if estado is False:
                return
            estado, self.terminalstatus_installed_terminals = conexion_terminal_status.ejecutar_select(conexion.select)
            if estado is False:
                return
            del conexion
            mensaje = f"Registros recuperados: {len(self.terminalstatus_installed_terminals)}..."
            servicioslog.escribir(mensaje)

            mensaje = f"Extrayendo datos de core_dowload_log..."
            servicioslog.escribir(mensaje)
            conexion = configuracion.conexiones[1]
            conexion_core_dowload_log = ConexionDBSQLServer(servicioslog)
            estado = conexion_core_dowload_log.conectar(conexion.driver, conexion.server, conexion.database, conexion.username, conexion.password)
            if estado is False:
                return
            estado, self.coredownloadlog_data_soft = conexion_core_dowload_log.ejecutar_select(conexion.select)
            if estado is False:
                return
            del conexion
            mensaje = f"Registros recuperados: {len(self.coredownloadlog_data_soft)}..."
            servicioslog.escribir(mensaje)

            mensaje = f"Extrayendo datos automatizacion medio comunicacion..."
            servicioslog.escribir(mensaje)
            conexion = configuracion.conexiones[2]
            conexion_automatizacion_medio_comunicacion = ConexionDBSQLServer(servicioslog)
            estado = conexion_automatizacion_medio_comunicacion.conectar(conexion.driver, conexion.server, conexion.database,
                                                       conexion.username, conexion.password)
            if estado is False:
                return
            estado, self.medio_comunicacion = conexion_automatizacion_medio_comunicacion.ejecutar_select(conexion.select)
            if estado is False:
                return
            del conexion
            mensaje = f"Registros recuperados: {len(self.medio_comunicacion)}..."
            servicioslog.escribir(mensaje)

            mensaje = f"Extrayendo datos lapostecno_tabla_versiones..."
            servicioslog.escribir(mensaje)
            conexion_lapostecno_tabla_versiones = ConexionDBSQLServer(servicioslog)
            conexion = configuracion.conexiones[3]
            estado = conexion_lapostecno_tabla_versiones.conectar(conexion.driver, conexion.server, conexion.database,
                                                       conexion.username, conexion.password)
            if estado is False:
                return
            estado, self.lapostecno_tabla_versiones = conexion_lapostecno_tabla_versiones.ejecutar_select(conexion.select)
            if estado is False:
                return
            del conexion
            mensaje = f"Registros recuperados: {len(self.lapostecno_tabla_versiones)}..."
            servicioslog.escribir(mensaje)

            mensaje = f"Extrayendo datos dashboard..."
            servicioslog.escribir(mensaje)
            conexion = configuracion.conexiones[4]
            conexion_dashboard = ConexionDBMySQL(servicioslog)
            estado = conexion_dashboard.conectar(conexion.host, conexion.port, conexion.database,
                                                       conexion.username, conexion.password)
            if estado is False:
                return
            estado, self.terminals_meters_all = conexion_dashboard.ejecutar_select(conexion.select)
            if estado is False:
                return
            del conexion
            mensaje = f"Registros recuperados: {len(self.terminals_meters_all)}..."
            servicioslog.escribir(mensaje)

            # mensaje = f"Extrayendo datos salesforce..."
            servicios_salesforce = ServiciosSalesforce(servicioslog, configuracion)
            estado, self.datos_pax_paystore = servicios_salesforce.buscarterminales()
            if estado is False:
                return

            mensaje = f"Extrayendo datos soft_status..."
            servicioslog.escribir(mensaje)
            conexion = configuracion.conexiones[6]
            conexion_soft_status = ConexionDBMySQL(servicioslog)
            estado = conexion_soft_status.conectar(conexion.host, conexion.port, conexion.database,
                                                       conexion.username, conexion.password)
            if estado is False:
                return
            estado, self.terminales_softstatus = conexion_soft_status.ejecutar_select(conexion.select)
            if estado is False:
                return
            del conexion
            mensaje = f"Registros recuperados: {len(self.terminales_softstatus)}..."
            servicioslog.escribir(mensaje)

            mensaje = f"Extrayendo datos producto software..."
            servicioslog.escribir(mensaje)

            with open("producto_software.json", "r", encoding="utf8") as file:
                self.producto_software_base = json.load(file)

            mensaje = f"Registros recuperados: {len(self.producto_software_base)}..."
            servicioslog.escribir(mensaje)

            mensaje = f"Subproceso finalizado..."
            servicioslog.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Extrayendo datos: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            servicioslog.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            servicioslog.escribir(mensaje, tiempo=False)
            return estado

    def transform(self, servicioslog):
        estado = True
        datos_ingenico = {}
        datos_paystore_pax = {}
        dashboard = {}
        try:
            mensaje = f"Iniciando transformacion de datos..."
            servicioslog.escribir(mensaje)

            mensaje = f"Analizando conjunto de productos classic..."
            servicioslog.escribir(mensaje)

            for terminal, producto in self.datos_pax_paystore.items():
                if producto is not None:
                    if producto in self.producto_software_base:
                        self.producto_software[terminal] = self.producto_software_base[producto]
                    else:
                        self.producto_software[terminal] = None
                        with open('producto_software_fail.log', "a", encoding="utf8") as file_log:
                            file_log.write(f"Terminal:{terminal} - Producto:{producto}\n")
                    if producto == 'Classic':
                        datos_paystore_pax[terminal] = producto
                else:
                    self.producto_software[terminal] = None

            self.datos_pax_paystore = None
            self.producto_software_base = None

            mensaje = f"Analizando conjunto base de terminales ..."
            servicioslog.escribir(mensaje)
            for registro in self.terminalstatus_installed_terminals:
                terminal = Terminal()
                terminal.numero = registro[0]
                if terminal.numero in self.producto_software.keys():
                    terminal.software_objetivo = self.producto_software[terminal.numero]
                else:
                    terminal.software_objetivo = None
                self.terminales[terminal.numero] = terminal
            self.terminalstatus_installed_terminals = None
            self.producto_software = None

            mensaje = f"Analizando conjunto de datos del parametrizador..."
            servicioslog.escribir(mensaje)
            for registro in self.coredownloadlog_data_soft:
                if registro[0] in self.terminales.keys():
                    terminal = self.terminales[registro[0]]
                    terminal.sistema_operativo = None if registro[1] is None else str(registro[1]).replace('\t', '').replace('\n', '')
                    terminal.vvm = registro[2]
                    terminal.software = registro[3]
                    terminal.plantilla = registro[4]
                    terminal.fecha_actualizacion_soft = registro[5]
                    self.terminales[terminal.numero] = terminal
                    del terminal
            self.coredownloadlog_data_soft = None

            mensaje = f"Analizando conjunto de datos de medios de comiunicacion..."
            servicioslog.escribir(mensaje)
            for registro in self.medio_comunicacion:
                if registro[2] is not None and registro[2][:2].replace(" ", "") == "06":
                    datos_ingenico[registro[0]] = registro[2]
                if registro[0] in self.terminales.keys():
                    terminal = self.terminales[registro[0]]
                    terminal.medio_comunicacion = registro[1]
                    self.terminales[terminal.numero] = terminal
                    del terminal
            self.medio_comunicacion = None

            mensaje = f"Analizando conjunto de datos de plataformas..."
            servicioslog.escribir(mensaje)
            for numero, terminal in self.terminales.items():
                if terminal.numero[:2] == "38":
                    terminal.plataforma = "Moretti"
                elif terminal.numero in datos_ingenico.keys():
                    terminal.plataforma = "Ingenico Legacy"
                    terminal.sistema_operativo = None
                    terminal.vvm = None
                    terminal.software = datos_ingenico[terminal.numero]
                    terminal.plantilla = None
                elif (terminal.software is not None and terminal.software[:2] == "SP") or (terminal.plantilla is not None and terminal.plantilla[:2] == "SP"):
                    terminal.plataforma = "Softpay"
                    terminal.software = terminal.plantilla
                elif terminal.plataforma is None:
                    terminal.plataforma = "Legacy"

                if terminal.numero[:2] == '16':
                    terminal.plataforma = "Paystore Newland"
                elif terminal.numero in datos_paystore_pax.keys():
                    terminal.plataforma = "Paystore Pax"

            self.datos_pax_paystore = None

            mensaje = f"Analizando conjunto de datos paystore..."
            servicioslog.escribir(mensaje)

            dashboard = {}
            for registro in self.terminals_meters_all:
                dashboard[str(registro[0])] = registro

            for numero, terminal in self.terminales.items():
                if terminal.plataforma == "Paystore Newland":
                    if numero in dashboard.keys():
                        terminal_paystore = dashboard[numero]
                        terminal.sistema_operativo = terminal_paystore[1]
                        terminal.vvm = terminal_paystore[2]
                        terminal.software = terminal_paystore[3]
                        terminal.plantilla = terminal_paystore[4]
                        self.terminales[terminal.numero] = terminal
                        del terminal_paystore
                    else:
                        terminal.sistema_operativo = None
                        terminal.vvm = None
                        terminal.software = None
                        terminal.plantilla = None
                        terminal.fecha_actualizacion_soft = None
                elif terminal.plataforma == "Paystore Pax":
                    terminal.sistema_operativo = None
                    terminal.vvm = None
                    terminal.software = None
                    terminal.plantilla = None
                    terminal.fecha_actualizacion_soft = None
            self.terminals_meters_all = None
            del dashboard

            mensaje = f"Analizando conjunto de datos de la tabla de versiones sql..."
            servicioslog.escribir(mensaje)
            for numero, terminal in self.terminales.items():
                if terminal.plataforma in ["Ingenico Legacy", "Softpay"]:
                    terminal.actualizacion = "Presencial"
                    terminal.obsolescencia = "Critica"
                else:
                    terminal.actualizacion = None
                    terminal.obsolescencia = None
                    for registro in self.lapostecno_tabla_versiones:
                        if terminal.software == registro[0] and terminal.plantilla == registro[1]:
                            if terminal.plataforma == 'Paystore Newland':
                                terminal.actualizacion = registro[3]
                                terminal.obsolescencia = registro[2]
                            else:
                                if terminal.medio_comunicacion != None and terminal.medio_comunicacion != "Dial-Up":
                                    terminal.actualizacion = registro[3]
                                    terminal.obsolescencia = registro[2]
                                else:
                                    terminal.actualizacion = 'Presencial'
                                    terminal.obsolescencia = registro[2]
                            break

            mensaje = f"Analizando software faltante..."
            servicioslog.escribir(mensaje)
            reporte = {}
            alerta = False
            file = open('software_fail.log', "w", encoding="utf8")
            file.close()
            for numero, terminal in self.terminales.items():
                validado = False
                for registro in self.lapostecno_tabla_versiones:
                    if terminal.software == registro[0] and terminal.plantilla == registro[1]:
                        validado = True
                        break
                if validado == False:
                    if terminal.software not in reporte.keys():
                        reporte[terminal.software] = []
                    reporte[terminal.software].append(terminal.numero)
                    with open('software_fail.log', "a", encoding="utf8") as file_log:
                        file_log.write(f"[{str(date.today())} {time.strftime('%H:%M:%S', time.localtime())}] Terminal: {terminal.numero}, Plantilla: {terminal.plantilla}, Software: {terminal.software}, Medio de comunicacion: {terminal.medio_comunicacion}\n")
                    alerta = True
            if alerta == True:
                with open('software_fail.json', "w", encoding="utf8") as file:
                    json.dump(reporte, file, ensure_ascii=False, indent=4)
                serviciosAlerta = ServiciosAlerta(self.servicios_log, self.configuracion.conexiones[7])
                serviciosAlerta.enviar("Nuevo software detectado", "software_fail.json")

            self.lapostecno_tabla_versiones = None

            mensaje = f"Analizando conjunto de datos existentes..."
            servicioslog.escribir(mensaje)
            for registro in self.terminales_softstatus:
                terminal = Terminal()
                terminal.numero = registro[0]
                terminal.sistema_operativo = registro[1]
                terminal.vvm = registro[2]
                terminal.software = registro[3]
                terminal.software_objetivo = registro[4]
                terminal.plantilla = registro[5]
                terminal.plataforma = registro[6]
                terminal.fecha_actualizacion_soft = registro[7]
                terminal.actualizacion = registro[10]
                terminal.obsolescencia = registro[11]
                self.terminales_existentes[terminal.numero] = terminal
                del terminal
            self.terminales_softstatus = None
            mensaje = f"Lote total de terminales: {len(self.terminales)}..."
            servicioslog.escribir(mensaje)

            mensaje = f"Subproceso finalizado..."
            servicioslog.escribir(mensaje)

        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Transformando datos: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            servicioslog.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            servicioslog.escribir(mensaje, tiempo=False)
            return estado

    def load(self, servicioslog, datos_conexion):
        estado = True
        try:
            mensaje = f"Cargando terminales..."
            servicioslog.escribir(mensaje)

            mensaje = f"Generando lote de terminales a insertar ..."
            servicioslog.escribir(mensaje)
            terminales_insert = self.terminales.keys() - self.terminales_existentes.keys()
            for terminal_insert in terminales_insert:
                self.terminales_insert[terminal_insert] = self.terminales[terminal_insert]
            mensaje = f"Total de nuevas terminales a insertar: {len(self.terminales_insert)}"
            servicioslog.escribir(mensaje)

            mensaje = f"Generando lote de terminales a eliminar ..."
            servicioslog.escribir(mensaje)
            self.terminales_delete = self.terminales_existentes.keys() - self.terminales.keys()
            mensaje = f"Total de terminales existentes a eliminar: {len(self.terminales_delete)}"
            servicioslog.escribir(mensaje)

            mensaje = f"Generando lote de terminales a actualizar ..."
            servicioslog.escribir(mensaje)
            terminales_update = self.terminales.keys() - self.terminales_insert.keys()
            for terminal_update in terminales_update:
                if self.terminales[terminal_update] != self.terminales_existentes[terminal_update]:
                    self.terminales_update[terminal_update] = self.terminales[terminal_update]
            mensaje = f"Total de terminales existentes a actualizar: {len(self.terminales_update)}"
            servicioslog.escribir(mensaje)

            mensaje = f"Impactando lote de terminales a insertar..."
            servicioslog.escribir(mensaje)

            if len(self.terminales_insert) > 0:
                datos_insert = []
                for numero, terminal in self.terminales_insert.items():
                    datos_insert.append(terminal.to_insert())
                conexion_soft_status = ConexionDBMySQL(servicioslog)
                estado = conexion_soft_status.conectar(datos_conexion.host, datos_conexion.port, datos_conexion.database,
                                                       datos_conexion.username, datos_conexion.password)
                conexion_soft_status.ejecutar_insert(datos_conexion.insert, tuple(datos_insert))
                conexion_soft_status.desconectar()
            else:
                mensaje = f"Lote vacio, no hay terminales para insertar..."
                servicioslog.escribir(mensaje)

            mensaje = f"Impactando lote de terminales a eliminar..."
            servicioslog.escribir(mensaje)

            if len(self.terminales_delete) > 0:
                conexion_soft_status = ConexionDBMySQL(servicioslog)
                estado = conexion_soft_status.conectar(datos_conexion.host, datos_conexion.port, datos_conexion.database,
                                                       datos_conexion.username, datos_conexion.password)
                conexion_soft_status.ejecutar_delete(datos_conexion.delete, tuple(self.terminales_delete))
                conexion_soft_status.desconectar()
            else:
                mensaje = f"Lote vacio, no hay terminales para eliminar..."
                servicioslog.escribir(mensaje)

            mensaje = f"Impactando lote de terminales a actualizar..."
            servicioslog.escribir(mensaje)
            if len(self.terminales_update) > 0:
                datos_update = []
                for numero, terminal in self.terminales_update.items():
                    datos_update.append(terminal.to_update())
                conexion_soft_status = ConexionDBMySQL(servicioslog)
                estado = conexion_soft_status.conectar(datos_conexion.host, datos_conexion.port, datos_conexion.database,
                                                       datos_conexion.username, datos_conexion.password)
                conexion_soft_status.ejecutar_update(datos_conexion.update, tuple(datos_update))
                conexion_soft_status.desconectar()
            else:
                mensaje = f"Lote vacio, no hay terminales para actualizar..."
                servicioslog.escribir(mensaje)

            mensaje = f"Generando historia..."
            servicioslog.escribir(mensaje)

            conexion_soft_status = ConexionDBMySQL(servicioslog)
            estado = conexion_soft_status.conectar(datos_conexion.host, datos_conexion.port, datos_conexion.database,
                                                   datos_conexion.username, datos_conexion.password)
            conexion_soft_status.ejecutar_sp(datos_conexion.history)
            conexion_soft_status.desconectar()

            mensaje = f"Subproceso finalizado..."
            servicioslog.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Cargando terminales: {type(excepcion)} - {str(excepcion)}"
            servicioslog.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            servicioslog.escribir(mensaje)
        finally:
            return estado
