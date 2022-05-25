import os, unittest
from wav_flac_to_mp3_gui import convert_flac, convert_wav


test_wav = [r"c:\Users\...\Documents\PyAudioFileConversion\test_wav.wav"]
test_flac = [r"c:\Users\...\Documents\PyAudioFileConversion\test_flac.flac"]

converted_wav = [r"c:\Users\...\Documents\PyAudioFileConversion\test_wav.mp3"]
converted_flac = [r"c:\Users\...\Documents\PyAudioFileConversion\test_flac.mp3"]
   
test_mp3_wav = [r"c:\Users\...\Documents\PyAudioFileConversion\test_wav1.mp3"]
test_mp3_flac = [r"c:\Users\...\Documents\PyAudioFileConversion\test_flac1.mp3"]

mp3_size_flac = os.path.getsize(test_mp3_flac[0])
mp3_size_wav = os.path.getsize(test_mp3_wav[0])
converted_wav_size = os.path.getsize(converted_wav[0])
converted_flac_size = os.path.getsize(converted_flac[0])

convert_wav(test_wav)
convert_flac(test_flac)

class Tests(unittest.TestCase):

    def test(self):
        self.assertEqual(mp3_size_wav, converted_wav_size)
        self.assertEqual(mp3_size_flac, converted_flac_size)
if __name__ == "__main__":
    unittest.main()
