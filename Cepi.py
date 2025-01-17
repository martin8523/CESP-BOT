from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime


app = Flask(__name__)

# Diccionario en memoria para rastrear el estado de los usuarios
usuarios = {}



@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():

    numero_telefono = request.form.get('From')
    mensaje_cliente = request.form.get('Body').strip()
    
    # Obtener la fecha actual
    fecha_actual = datetime.now().date()
    
    # Verificar si el usuario es nuevo o si es un nuevo día
    if (numero_telefono not in usuarios or 
        usuarios[numero_telefono]["ultima_fecha"] != fecha_actual):
        usuarios[numero_telefono] = {
            "bienvenida_enviada": False,
            "ultima_fecha": fecha_actual,
            "estado": "inicio"
        }
    
    respuesta = ""
    estado = usuarios[numero_telefono]["estado"]
    
    if not usuarios[numero_telefono]["bienvenida_enviada"]:
        respuesta = ("  ¡Bienvenido al Chat Bot de CESPAZ!\n"
                      "¿En qué puedo ayudarte hoy?\n"
                    "1. Como me puedo adherir?\n"
                    "2. Horarios de atención\n"
                    "3. Que cobertura ofrecen?\n"
                    "4. Tengo un reclamo o necesito otra informacion\n"
                    "5. Terminar la Conversacion\n")
        usuarios[numero_telefono]["bienvenida_enviada"] = True
        usuarios[numero_telefono]["estado"] = "menu_principal"

    elif estado == "menu_principal":
        if mensaje_cliente == "1":
            respuesta = ("Te podes adherir mediante dos modalidades:\n"
                         "1. Si tenes suministro a tu nombre\n"
                         "2. Si alquilas o no tenes suministro a tu nombre\n"
                         " \n"
                         "0. Volver al menú principal")
            usuarios[numero_telefono]["estado"] = "menu_adherir"
        elif mensaje_cliente == "2":
            respuesta = ("Nuestros horarios de atención son de 8 AM a 13 PM de lunes a viernes y contamos con guardia las 24 Hs para el ingreso de Servicios\n"
                         " \n"
                         "0. Volver al menú principal")
            usuarios[numero_telefono]["estado"] = "inicio"
        elif mensaje_cliente == "3":
            respuesta = ("La cobertura se comprende de: Retiro y o traslado hasta 250 km. Gestión de defunción ante registro civil y municipio. Ataúd y servicio de velación, nicho en los panteones de Cooperativa en concesión por 10 años ( que es el periodo que la municipalidad está dando las concesiones actualmente)\n"
                         " \n"
                         "Puede visitar el siguiente enlace para mayor informacion\n"
                         "https://www.coopsal.com.ar/servicio-cespaz.php\n"
                         " \n"
                         "0. Volver al menú principal")
            usuarios[numero_telefono]["estado"] = "inicio"
        elif mensaje_cliente == "4":
            respuesta = ("Completa el siguiente formulario y nos comunicaremos con vos.\n"
                         " \n"
                         "https://forms.gle/mY1CKwHTXVCezakx7\n"
                         "0. Volver al menú principal")
            usuarios[numero_telefono]["estado"] = "inicio"
        elif mensaje_cliente == "5":
            respuesta = ("Gracias por comunicarte con nostros.")
            usuarios[numero_telefono]["estado"] = "fin"
        else:
            respuesta = ("Opción no válida. Por favor, elija una opción del menú:\n"
                        "1. Como me puedo adherir?\n"
                        "2. Horarios de atención\n"
                        "3. Que cobertura ofrecen?\n"
                        "4. Tengo un reclamo o necesito otra informacion\n"
                        "5. Terminar la Conversacion\n")
    elif estado == "inicio":
        if mensaje_cliente == "0":
            respuesta = ("¡Bienvenido al Chat Bot de CESPAZ!\n"
                         " \n"
                         "¿En qué puedo ayudarte hoy?\n"
                        "1. Como me puedo adherir?\n"
                        "2. Horarios de atención\n"
                        "3. Que cobertura ofrecen?\n"
                        "4. Tengo un reclamo o necesito otra informacion\n"
                        "5. Terminar la Conversacion\n")
            usuarios[numero_telefono]["estado"] = "menu_principal"
    elif estado == "menu_adherir":
        if mensaje_cliente == "0":
            respuesta = ("Te podes adherir mediante dos modalidades:\n"
                         "1. Si tenes suministro a tu nombre\n"
                         "2. Si alquilas o no tenes suministro a tu nombre\n"
                         " \n"
                         "0. Volver al menú principal")
            usuarios[numero_telefono]["estado"] = "menu_principal"
        elif mensaje_cliente == "1":
            respuesta = ("Con suministro a tu nombre: El alta se realiza en forma presencial o virtual."
                         "Se necesitan los DNI de todo el grupo familiar y los datos del Suministro." 
                         "Tanto el titular como su conyuge pueden vivir en cualquier punto del pail,"
                          "el resto de los adherentes debe vivir y tener en su DNI el domicilio del suministro\n"
                         "Completa este formulario y luego envianos las fotos de todos los dni de tu grupo familiar. El alta se realiza en el momento\n"
                         " \n"
                         "https://forms.gle/ndfaQ8ZqqtggbG4M6\n"
                         " \n"
                         "0. Volver al menú anterior")
            usuarios[numero_telefono]["estado"] = "submenu_adhe"
        elif mensaje_cliente == "2":
            respuesta = ("Sin suministro a mi nombre:El alta se realiza en forma presencial y se necesita los DNI de todo el grupo familiar\n"
                         "Acercate con tu DNI y el de tu grupo familiar a nuestras oficinas y tramitalo en menos de 5 minutos\n"
                         " \n"
                         "0. Volver al menú anterior")
            usuarios[numero_telefono]["estado"] = "submenu_adhe"
        else:
            respuesta = ("Opción no válida. Por favor, elija una opcion de la lista:\n"
                         "1. Si tenes suministro a tu nombre\n"
                         "2. Si alquilas o no tenes suministro a tu nombre\n"
                         "0. Volver al menú principal")
    elif estado == "submenu_adhe":
        if mensaje_cliente == "0":
            respuesta = ("Te podes adherir mediante dos modalidades:\n"
                         "1. Si tenes suministro a tu nombre\n"
                         "2. Si alquilas o no tenes suministro a tu nombre\n"
                         "0. Volver al menú principal")
            usuarios[numero_telefono]["estado"] = "menu_principal"
        
    # Configurar la respuesta de Twilio
    resp = MessagingResponse()
    resp.message(respuesta)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
