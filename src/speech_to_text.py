import vosk
import sounddevice as sd
import keyboard
import queue
import json
import sys


class SpeechToTextManager:
    def __init__(self):
        self.fs = 48000
        self.queue = queue.Queue()
        self.stop_recording = False

        vosk.SetLogLevel(-1)
        print("Starting speech to text engine please wait...")
        model_path = "model"
        model = vosk.Model(model_path)
        self.rec = vosk.KaldiRecognizer(model, self.fs)

        keyboard.add_hotkey("p", lambda: setattr(self, "stop_recording", True))

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.queue.put(bytes(indata))

    def on_press(self, key):
        try:
            print("reached", key.char)
            if key.char == "p":
                self.stop_recording = True
        except AttributeError:
            pass

    def speechtotext_from_mic_continuous(self):
        full_transcript = []
        self.stop_recording = False

        print("Speak into your microphone")
        with sd.RawInputStream(
            samplerate=self.fs,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self.callback,
        ):

            while not self.stop_recording:
                try:
                    data = self.queue.get(timeout=0.1)
                except queue.Empty:
                    continue

                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "")
                    if text:
                        full_transcript.append(text)

        final = json.loads(self.rec.FinalResult())
        full_transcript.append(final.get("text", ""))

        return " ".join(full_transcript).strip()
