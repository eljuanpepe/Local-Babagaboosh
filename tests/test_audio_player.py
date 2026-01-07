import os
import time
import unittest

from src.audio_player import AudioManager


class SoundPlayer(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.audio_manager = AudioManager()
        self.MP3_FILEPATH = "tests/audio/TestAudio_MP3.mp3"
        self.WAV_FILEPATH = "tests/audio/TestAudio_WAV.wav"
        self.lots_test_range = 3

        self.assertTrue(os.path.exists(self.MP3_FILEPATH), "Missing MP3 file")

    def test_mp3(self):
        self.audio_manager.play_audio(self.MP3_FILEPATH)

    def test_wav(self):
        self.audio_manager.play_audio(self.WAV_FILEPATH)

    def test_lots_of_mp3(self):
        for _ in range(self.lots_test_range):
            self.audio_manager.play_audio(self.MP3_FILEPATH, False, False, False)
            time.sleep(0.1)

    def test_lots_of_wav(self):
        for _ in range(self.lots_test_range):
            self.audio_manager.play_audio(self.WAV_FILEPATH, False, False, False)
            time.sleep(0.1)

    async def test_async(self):
        await self.audio_manager.play_audio_async(self.MP3_FILEPATH)
        time.sleep(1)
        await self.audio_manager.play_audio_async(self.WAV_FILEPATH)
        time.sleep(1)


if __name__ == "__main__":
    unittest.main()
