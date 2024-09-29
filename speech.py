
import io
import os
# Imports the Google Cloud client library
# pip install --upgrade google-cloud-texttospeech google-cloud-speech
from google.cloud import speech, texttospeech
# pip install sounddevice, scipy, soundfile
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf

path = os.getcwd()


credential_path = "C:\\Users\\yuzba\\Documents\\GitHub\\nlp-2021-494bf1773dbc.json"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

sys_delay = 1 # sec
userresponcefile = 'c_input.wav'
ttsfile='c_output.wav'


class STT():
    def __init__(self):        
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="en-US") 
        self.client = speech.SpeechClient()        

    def opensoundfile(self, file_name):        
        with io.open(file_name, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
        return audio

    def recognize(self, audio):
        response = ''
        try:
            response = self.client.recognize(config=self.config, audio=audio)
        except:
            print('Failed to recognize command')
        return response    

class TTS():
    def __init__(self):        
        self.client = texttospeech.TextToSpeechClient() 

    def tts_request(self, textstring):
        synthesis_input = texttospeech.SynthesisInput(text=textstring)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response

    def save2file(self, respond, outputfilename='pet_command_response.wav'):
        with open(outputfilename, 'wb') as out:
            out.write(respond.audio_content)
            print('Audio content written to file: ' + outputfilename)

# Example usage:
if __name__ == '__main__':
    # ts = TTS()
    # command = 'Feeding your pet now'
    # ts.save2file(ts.tts_request(command), 'pet_command_response.wav')
    pass
