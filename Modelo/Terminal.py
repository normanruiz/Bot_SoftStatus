class Terminal:
    def __init__(self):
        self._numero = None
        self._sistema_operativo = None
        self._vvm = None
        self._medio_comunicacion = None
        self._plantilla = None
        self._software = None
        self._software_objetivo = None
        self._plataforma = None
        self._fecha_actualizacion_soft = None
        self._actualizacion = None
        self._obsolescencia = None

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        self._numero = numero

    @property
    def sistema_operativo(self):
        return self._sistema_operativo

    @sistema_operativo.setter
    def sistema_operativo(self, sistema_operativo):
        self._sistema_operativo = sistema_operativo[:40] if sistema_operativo is not None else sistema_operativo

    @property
    def vvm(self):
        return self._vvm

    @vvm.setter
    def vvm(self, vvm):
        self._vvm = vvm

    @property
    def medio_comunicacion(self):
        return self._medio_comunicacion

    @medio_comunicacion.setter
    def medio_comunicacion(self, medio_comunicacion):
        self._medio_comunicacion = medio_comunicacion

    @property
    def plantilla(self):
        return self._plantilla

    @plantilla.setter
    def plantilla(self, plantilla):
        self._plantilla = plantilla

    @property
    def software(self):
        return self._software

    @software.setter
    def software(self, software):
        self._software = software

    @property
    def software_objetivo(self):
        return self._software_objetivo

    @software_objetivo.setter
    def software_objetivo(self, software_objetivo):
        self._software_objetivo = software_objetivo

    @property
    def plataforma(self):
        return self._plataforma

    @plataforma.setter
    def plataforma(self, plataforma):
        self._plataforma = plataforma

    @property
    def fecha_actualizacion_soft(self):
        return self._fecha_actualizacion_soft

    @fecha_actualizacion_soft.setter
    def fecha_actualizacion_soft(self, fecha_actualizacion_soft):
        self._fecha_actualizacion_soft = fecha_actualizacion_soft

    @property
    def actualizacion(self):
        return self._actualizacion

    @actualizacion.setter
    def actualizacion(self, actualizacion):
        self._actualizacion = actualizacion

    @property
    def obsolescencia(self):
        return self._obsolescencia

    @obsolescencia.setter
    def obsolescencia(self, obsolescencia):
        self._obsolescencia = obsolescencia

    def __str__(self):
        return f"Numero: {self.numero} - Plantilla: {self.plantilla} - Software: {self.software} - Medio de Comunicacion: {self.medio_comunicacion}"

    def __ne__(self, other):
        if self.sistema_operativo != other.sistema_operativo or self.vvm != other.vvm or self.plantilla != other.plantilla or self.software != other.software or self.software_objetivo != other.software_objetivo or self.fecha_actualizacion_soft != other.fecha_actualizacion_soft or self.actualizacion != other.actualizacion or self.obsolescencia != other.obsolescencia:
            return True
        else:
            return False

    def to_insert(self):
        return (self.numero, self.sistema_operativo, self.vvm, self.software, self.software_objetivo, self.plantilla, self.plataforma, self.actualizacion, self.obsolescencia, self.fecha_actualizacion_soft)

    def to_update(self):
        return (self.sistema_operativo, self.vvm, self.software, self.software_objetivo, self.plantilla, self.plataforma, self.actualizacion, self.obsolescencia, self.fecha_actualizacion_soft, self.numero)
