# Local Babagaboosh
Simple app that lets you have a verbal conversation with a local AI model using Ollama, Vosk and Kokoro or Piper.  
Originally written by DougDoug.

## SETUP:
1) This was written in Python 3.12.

2) Run `pip install -r requirements.txt` to install all modules.

3) This uses the Vosk, Kokoro TTS or Piper TTS, and Ollama.

4) Optionally, you can use OBS Websockets and an OBS plugin to make images move while talking. First open up OBS. Make sure you're running version 28.X or later. Click Tools, then WebSocket Server Settings. Make sure "Enable WebSocket server" is checked. Then set Server Port to '4455' and set the Server Password to 'TwitchChat9'. If you use a different Server Port or Server Password in your OBS, just make sure you update the config file file accordingly. Next install the Move OBS plugin: https://obsproject.com/forum/resources/move.913/ Now you can use this plugin to add a filter to an audio source that will change an image's transform based on the audio waveform. For example, I have this filter on a specific audio track that will move Pajama Sam's image whenever text-to-speech audio is playing in that audio track. Note that OBS must be open when you're running this code, otherwise OBS WebSockets won't be able to connect. If you don't need the images to move while talking, you can just delete the OBS portions of the code.

## Using the App

1) Run `main.py`

2) Once it's running, press the key defined under the config file under the name `key_start_recording` to start the conversation, and Vosk will listen to your microphone and transcribe it into text.

3) Once you're done talking, press the key defined under the config file under the name `key_stop_recording`. Then the code will send all of the recorded text to the AI.

4) Wait a few seconds for the AI to generate a response and for the TTS engine to turn that response into audio. Once it's done playing the response, you can press the `key_start_recording` again to start the loop again and continue the conversation.
