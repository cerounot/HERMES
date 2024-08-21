import os
import json
import pyaudio
import unicodedata
from vosk import Model, KaldiRecognizer
import time
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Ruta al modelo de Idioma descargado.
modelo_idioma = "vosk-model-es-0.42"

# Inicializar el modelo de Vosk
if not os.path.exists(modelo_idioma):
    print(f"El modelo en {modelo_idioma} no se encuentra")
    exit()

model = Model(modelo_idioma)
rec = KaldiRecognizer(model, 16000)

# Conexión a MongoDB
try:
    # Conectar a MongoDB Atlas
    #uri = "mongodb+srv://CeroUnoClusterAdmin:209197219Jenniffer@cluster0.pk2h25a.mongodb.net/?appName=Cluster"
    uri = "Uri del Servidor"
    # mongo_client = MongoClient(uri, server_api=ServerApi('1'))
    mongo_client = MongoClient(uri, server_api=ServerApi('1'))
    db = mongo_client["Hermes"]
    collection = db["Diccionario"]
    print("Conexión exitosa a MongoDB")
except pymongo.errors.ConfigurationError as e:
    print(f"Error de configuración: {e}")
except Exception as e:
    print(f"Error: {e}")

# Queue
queue_imgs = []
is_on_queue = False

def normalize_str(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if unicodedata.category(c) != 'Mn')

def showImgs():
    global is_on_queue, queue_imgs
    is_on_queue = True
    cycle_images()
    queue_imgs.clear()
    is_on_queue = False

def cycle_images():
    for word in queue_imgs:
        try:
            #? Usamos una expresión regular para en
            document = collection.find_one({ "text": { "$regex": fr"\b{word}\b", "$options": "i" } })
            print("\nResultado:")
            print(document)
        except Exception as e:
            print(f"Error al mostrar la imagen {word}: {e}")
            continue

# Instanciar PyAudio y crear un Objeto Stream
pAudio = pyaudio.PyAudio()
try:
    stream = pAudio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print("Por favor, hable ahora...")
    # Capturar el audio en bucle y procesarlo
    while True:
        try:
            data = stream.read(4096, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                resultObj = json.loads(rec.Result())
                transcripcion = resultObj.get("text", "")
                if transcripcion:
                    if is_on_queue is False:
                        print(f"Dijiste: {transcripcion}")
                        splitted = transcripcion.split(' ')
                        queue_imgs.extend(splitted)
                        showImgs()
                else:
                    pass
        except KeyboardInterrupt:
            print("Interrupción recibida, deteniendo...")
            break
        except Exception as e:
            print(f"Error al procesar el audio: {e}")
            break
finally:
    # Parar y cerrar el Stream
    stream.stop_stream()
    stream.close()
    pAudio.terminate()
    print("Stream terminado correctamente.")
