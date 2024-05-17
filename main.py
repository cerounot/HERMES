import os
import json
import pyaudio
import unicodedata
from vosk import Model, KaldiRecognizer
from io import StringIO
from PIL import Image

# Ruta al modelo de Idioma descargado.
modelo_idioma = "vosk-model-es-0.42"

# Inicializar el modelo de Vosk
if not os.path.exists(modelo_idioma):
    print(f"El modelo en {modelo_idioma} no se encuentra")
    exit()

model = Model(modelo_idioma)
rec = KaldiRecognizer(model, 16000)

# Queue
queue = []
queue_imgs = []
is_on_queue = False

def translate():
    global is_on_queue
    global queue
    print("######### Probando Queue #########")
    is_on_queue = True
    for x in queue:
        if len(x) > 1:
            # Muestran imagenes
            print("Imagen")
        else:
            # Mostrar letra
            print("Letra")
    queue.clear()
    is_on_queue = False
    print("######### Fin de la Prueba de Queue #########")

def normalize_str(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if unicodedata.category(c) != 'Mn')

def showImgs():
    global is_on_queue
    global queue_imgs
    print("######### Probando Queue #########")
    is_on_queue = True
    for img_name in queue_imgs:
        img_name_cleaned = normalize_str(img_name)  # Limpiar el nombre del archivo
        img_path = os.path.join("img", img_name_cleaned + ".png")
        try:
            img = Image.open(img_path)
            img.show()
        except Exception as e:
            print(f"Error al mostrar la imagen {img_name}: {e}")
    queue_imgs.clear()
    queue.clear()
    is_on_queue = False
    print("######### Fin de la Prueba de Queue #########")

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
                        print(transcripcion)
                        #* Para imágenes
                        queue_imgs.extend(transcripcion)
                        #* Para el Queue
                        # queue.extend(transcripcion.split(' '))
                else:
                    #* Para imágenes
                    showImgs()
                    #* Para Queue
                    translate()
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
