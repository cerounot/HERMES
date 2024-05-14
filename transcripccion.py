import os
import json
from vosk import Model, KaldiRecognizer
import pyaudio

# Ruta al modelo de Idioma descargado.
modelo_idioma = "vosk-model-small-es-0.42"

# Inicializar el modelo
if not os.path.exists(modelo_idioma):
    print(f"El modelo en {modelo_idioma} no se encuentra")
    exit()

model = Model(modelo_idioma)
rec = KaldiRecognizer(model, 16000)

# Instanciamos PyAudio y creamos un Objeto Stream (para obtener los Inputs)
pAudio = pyaudio.PyAudio()
stream = pAudio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

print("Por favor, hable ahora...")
# Capturamos el Audio en Bucle y Procesamos.
while True:
    #! El primer parámetro es la cantidad de "Frames" a leer, el segundo es para levantar una excepción en caso de excederla.
    data = stream.read(4096, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        resultObj = json.loads(rec.Result())
        transcripccion = resultObj["text"]
        if transcripccion != '':
            print(transcripccion)

#* Paramos y cerramos el Stream
stream.stop_stream()
stream.close()
pAudio.terminate()
