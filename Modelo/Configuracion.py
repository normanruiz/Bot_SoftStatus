class Configuracion:
    def __init__(self):
        self._configfile = 'config.xml'
        self._bot = None
        self._conexiones = []

    @property
    def configfile(self):
        return self._configfile

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, bot):
        self._bot = bot

    @property
    def conexiones(self):
        return self._conexiones

    @conexiones.setter
    def conexiones(self, conexiones):
        self._conexiones = conexiones


class Autor:
    def __init__(self, nombre=None, correo=None):
        self._nombre = nombre
        self._correo = correo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, correo):
        self._correo = correo


class Bot:
    def __init__(self, nombre=None, estado=None, hilos=None, autor=None):
        self._nombre = nombre
        self._estado = estado
        self._hilos = hilos
        self._autor = autor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, estado):
        self._estado = estado

    @property
    def hilos(self):
        return self.hilos

    @hilos.setter
    def hilos(self, hilos):
        self._hilos = hilos

    @property
    def autor(self):
        return self._autor

    @autor.setter
    def autor(self, autor):
        self._autor = autor


class ConexionSQLServer:
    def __init__(self, driver=None, server=None, database=None, username=None, password=None, select=None, insert=None,
                 update=None, delete=None, history=None):
        self._driver = driver
        self._server = server
        self._database = database
        self._username = username
        self._password = password
        self._select = select
        self._insert = insert
        self._update = update
        self._delete = delete
        self._history = history

    @property
    def driver(self):
        return self._driver

    @property
    def server(self):
        return self._server

    @property
    def database(self):
        return self._database

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def select(self):
        return self._select

    @property
    def insert(self):
        return self._insert

    @property
    def update(self):
        return self._update

    @property
    def delete(self):
        return self._delete

    @property
    def history(self):
        return self._history

class ConexionMySQL:
    def __init__(self, host=None, port=None, database=None, username=None, password=None, select=None, insert=None,
                 update=None, delete=None, history=None):
        self._host = host
        self._port = port
        self._database = database
        self._username = username
        self._password = password
        self._select = select
        self._insert = insert
        self._update = update
        self._delete = delete
        self._history = history

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def database(self):
        return self._database

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def select(self):
        return self._select

    @property
    def insert(self):
        return self._insert

    @property
    def update(self):
        return self._update

    @property
    def delete(self):
        return self._delete

    @property
    def history(self):
        return self._history

class ApiTeams:
    def __init__(self, remitente=None, destinatario=None, ip=None, port=None, adjunto=True):
        self._remitente = remitente
        self._destinatario = destinatario
        self._ip = ip
        self._port = port
        self._adjunto = True if adjunto == "True" else False

    @property
    def remitente(self):
        return self._remitente

    @remitente.setter
    def remitente(self, remitente):
        self._remitente = remitente

    @property
    def destinatario(self):
        return self._destinatario

    @destinatario.setter
    def destinatario(self, destinatario):
        self._destinatario = destinatario

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip):
        self._ip = ip

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    @property
    def adjunto(self):
        return self._adjunto

    @adjunto.setter
    def adjunto(self, adjunto):
        self._adjunto = True if adjunto == "True" else False
