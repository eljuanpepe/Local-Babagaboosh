from kokoro_onnx import Kokoro
from piper import PiperVoice
import soundfile as sf
import tomllib
import wave
import os


class TTSManager:
    def __init__(self):
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)
        self.engine = config["tts"]["tts_engine"]

        if self.engine == "kokoro":
            self.voice = config["tts"]["kokoro"]["voice"]
            self.kokoro = Kokoro(
                "models/kokoro-model/kokoro-v1.0.int8.onnx",
                "models/kokoro-model/voices-v1.0.bin",
            )
            # all_voices = self.kokoro.get_voices()
            # print(f"\nAll TTS voices: \n{all_voices}\n")
        else:
            self.voice = f"models/piper-voices/{config["tts"]["piper"]["voice"]}.onnx"
            self.piper = PiperVoice.load(self.voice)

    def kokoro_manager(self, input_text, subdirectory=""):
        samples, sample_rates = self.kokoro.create(
            input_text, voice=self.voice, speed=1.0
        )

        output_dir = subdirectory or "."
        file_name = f"___Msg{str(hash(input_text))}.wav"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, file_name)

        sf.write(output_path, samples, sample_rates)

        return output_path

    def piper_manager(self, input_text, subdirectory=""):
        output_dir = subdirectory or "."
        file_name = f"___Msg{str(hash(input_text))}.wav"

        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, file_name)

        with wave.open(output_path, "wb") as wav_file:
            self.piper.synthesize_wav(input_text, wav_file)

        return output_path

    def text_to_audio(self, input_text, subdirectory=""):
        if self.engine == "kokoro":
            return self.kokoro_manager(input_text, subdirectory)
        else:
            return self.piper_manager(input_text, subdirectory)
