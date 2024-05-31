import pyaudio
from vosk_recognizer import VoskRecognizer
from queue_processor import QueueProcessor
from interfaces import Interfaces

# Instanciar PyAudio y crear un Objeto Stream
pAudio = pyaudio.PyAudio()
try:
    stream = pAudio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print("Por favor, hable ahora...")
    
    recognizer = VoskRecognizer("vosk-model-small-es-0.42")
    processor = QueueProcessor()

    # Capturar el audio en bucle y procesarlo
    while True:
        try:
            data = stream.read(4096, exception_on_overflow=False)
            transcription = recognizer.recognize(data)
            if transcription:
                if not processor.isOnQueue(): #alexis
                    processor.add_transcription(transcription)
            else:
                processor.process_queue()
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