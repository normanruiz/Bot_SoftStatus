from email.message import EmailMessage
import smtplib
import json
class ServiciosAlerta:

    def __init__(self, servicios_log, conexion):
        self._servicios_log = servicios_log
        self._conexion = conexion

    @property
    def servicios_log(self):
        return self._servicios_log

    @servicios_log.setter
    def servicios_log(self, servicios_log):
        self._servicios_log = servicios_log

    @property
    def conexion(self):
        return self._conexion

    @conexion.setter
    def conexion(self, conexion):
        self._conexion = conexion

    def enviar(self, asunto, archivo_adjunto):
        estado = True
        try:
            remitente = self.conexion.remitente
            destinatario = self.conexion.destinatario
            email = EmailMessage()
            email["From"] = remitente
            email["To"] = destinatario
            email["Subject"] = asunto
            if self.conexion.adjunto is True:
                with open(archivo_adjunto) as file:
                    attachment = json.load(file)
                    attachment = json.dumps(attachment)
                    bs = attachment.encode('utf-8')
                    email.add_attachment(bs, maintype='application', subtype='json', filename=archivo_adjunto)
            s = smtplib.SMTP(self.conexion.ip, self.conexion.port)
            s.send_message(email)
            s.quit()
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Enviando alerta: {type(excepcion)} - {str(excepcion)}"
            self.servicios_log.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            self.servicios_log.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            self.servicios_log.escribir(mensaje, tiempo=False)
            return estado