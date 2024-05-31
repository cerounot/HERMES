import os
import json
from vosk import Model, KaldiRecognizer

class VoskRecognizer:
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            print(f"El modelo en {model_path} no se encuentra")
            exit()
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)

    def recognize(self, data):
        if self.rec.AcceptWaveform(data):
            resultObj = json.loads(self.rec.Result())
            return resultObj.get("text", "")
        else:
            return None