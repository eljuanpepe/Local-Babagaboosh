import time
import tomllib
from pynput import keyboard
from rich import print
from speech_to_text import SpeechToTextManager
from ollama_chat import AIManager
from text_to_speech import TTSManager
from obs_websockets import OBSWebsocketsManager
from audio_player import AudioManager

BACKUP_FILE = "ChatHistoryBackup.txt"

elevenlabs_manager = TTSManager()
obswebsockets_manager = OBSWebsocketsManager()
openai_manager = AIManager()
speechtotext_manager = SpeechToTextManager()
audio_manager = AudioManager()

with open("ai_system_prompt.txt", "r") as file:
    system_prompt = file.read()

with open("config.toml", "rb") as f:
    config = tomllib.load(f)
    talk_key = config["speech_to_text"]["key_start_recording"]
    scene = config["obs_websockets"]["scene"]
    source = config["obs_websockets"]["source"]

FIRST_SYSTEM_MESSAGE = {
    "role": "system",
    "content": system_prompt,
}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)


def on_press(key):
    if getattr(key, "name", None) == talk_key:
        return False


print(f"[green]Starting the loop, press {talk_key} to begin")
while True:
    with keyboard.Listener(on_press=on_press) as listener:  # type: ignore
        listener.join()

    print(f"[green]User pressed {talk_key} key! Now listening to your microphone:")

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()

    if mic_result == "":
        print("[red]Did not receive any input from your microphone!")
        continue

    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(mic_result)

    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    # Send it to 11Labs to turn into cool audio
    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result)

    # Enable the picture of Pajama Sam in OBS
    obswebsockets_manager.set_source_visibility(scene, source, True)

    # Play the mp3 file
    audio_manager.play_audio(elevenlabs_output, True, True, True)

    # Disable Pajama Sam pic in OBS
    obswebsockets_manager.set_source_visibility(scene, source, False)

    print(
        "[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n"
    )
