from kokoro_onnx import Kokoro
import soundfile as sf
import tomllib
import os


class TTSManager:
    def __init__(self):
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)

        self.voice = config["tts"]["kokoro"]["voice"]
        self.kokoro = Kokoro(
            "models/kokoro-model/kokoro-v1.0.int8.onnx",
            "models/kokoro-model/voices-v1.0.bin",
        )
        # all_voices = self.kokoro.get_voices()
        # print(f"\nAll TTS voices: \n{all_voices}\n")

    def text_to_audio(
        self, input_text, voice=None, save_as_wave=False, subdirectory=""
    ):
        tts_voice = self.voice if voice is None else voice

        samples, sample_rates = self.kokoro.create(
            input_text, voice=tts_voice, speed=1.0
        )

        ext = "wav" if save_as_wave else "mp3"
        file_name = f"___Msg{str(hash(input_text))}.{ext}"

        output_dir = subdirectory or "."
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, file_name)

        sf.write(output_path, samples, sample_rates)

        return output_path


if __name__ == "__main__":
    elevenlabs_manager = TTSManager()

    file_path = elevenlabs_manager.text_to_audio(
        "This is my saved test audio, please make me beautiful", "af_aoede"
    )
    print("Finished with all tests")
