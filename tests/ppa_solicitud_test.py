"""
Prueba de PPA Solicitud
"""
import json
import requests

API_PPA_SOLICITUD_URL = "http://127.0.0.1:8005/v3/ppa_solicitudes/solicitar"
API_TIMEOUT = 12
BANCO_FOTOGRAFIAS_RUTA = "/home/guivaloz/Pictures"


def test_ppa_solicitud():
    """
    Prueba de PPA Solicitud
    """

    # Datos de prueba
    datos = {
        "autoridad_clave": "TRC-J1-CIV",
        "cit_cliente_curp": "VALG710406HNLLZL04",
        "cit_cliente_email": "guillermo.valdes@pjecz.gob.mx",
        "cit_cliente_nombres": "Guillermo",
        "cit_cliente_apellido_primero": "Valdes",
        "cit_cliente_apellido_segundo": "Lozano",
        "cit_cliente_telefono": "8711542682",
        "domicilio_calle": "Juana de Arco",
        "domicilio_numero": "213",
        "domicilio_colonia": "Roma",
        "domicilio_cp": 24000,
        "compania_telefonica": "ATT",
        "numero_expediente": "1/2022",
        "identificacion_oficial_archivo": "ine.jpg",
        "identificacion_oficial_url": "https://noexiste.com/ine.jpg",
        "comprobante_domicilio_archivo": "domicilio.jpg",
        "comprobante_domicilio_url": "https://noexiste.com/domicilio.jpg",
        "autorizacion_archivo": "carta.jpg",
        "autorizacion_url": "https://noexiste.com/carta.jpg",
    }

    # Archivo con la identificación oficial
    identificacion_oficial_archivo = "ine.jpg"
    identificacion_oficial = open(f"{BANCO_FOTOGRAFIAS_RUTA}/{identificacion_oficial_archivo}", "rb")

    # Archivo con el comprobante de domicilio
    comprobante_domicilio_archivo = "cfe.jpg"
    comprobante_domicilio = open(f"{BANCO_FOTOGRAFIAS_RUTA}/{comprobante_domicilio_archivo}", "rb")

    # Archivo con la autorización
    autorizacion_archivo = "autorizacion.png"
    autorizacion = open(f"{BANCO_FOTOGRAFIAS_RUTA}/{autorizacion_archivo}", "rb")

    # Enviar
    try:
        respuesta = requests.post(
            API_PPA_SOLICITUD_URL,
            data=datos,
            files={
                "identificacion_oficial": (identificacion_oficial_archivo, identificacion_oficial),
                "comprobante_domicilio": (comprobante_domicilio_archivo, comprobante_domicilio),
                "autorizacion": (autorizacion_archivo, autorizacion),
            },
            timeout=API_TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        assert False, "No se pudo conectar con la API. " + str(error)
    except requests.exceptions.Timeout as error:
        assert False, "Tiempo de espera agotado al conectar con la API. " + str(error)
    except requests.exceptions.HTTPError as error:
        assert False, "Error HTTP la API arrojó un problema: " + str(error)
    except requests.exceptions.RequestException as error:
        assert False, "Error desconocido con la API . " + str(error)
    resultado = respuesta.json()

    # Cerrar archivos
    identificacion_oficial.close()
    comprobante_domicilio.close()
    autorizacion.close()

    # Verificar que el resultado sea exitoso
    if not "success" in resultado:
        assert False, "La respuesta no tiene el campo success"
    if not resultado["success"]:
        if "message" in resultado:
            assert False, resultado["message"]
        assert False, "La respuesta dice que la operacion fallo"

    # Mostrar los resultado de la respuesta
    print(resultado)

    # La prueba fue exitosa
    assert True


if __name__ == "__main__":
    test_ppa_solicitud()
