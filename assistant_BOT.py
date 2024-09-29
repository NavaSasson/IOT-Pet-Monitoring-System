import time
from speech import *
import data_acq as da
from init import *
import pandas as pd 
from pocketsphinx import LiveSpeech
from icecream import ic as icA
from datetime import datetime 
import os.path
from os import path

def time_format():
    return f'{datetime.now()}  Assistant BOT|> '
icA.configureOutput(prefix=time_format)
icA.configureOutput(includeContext=False) # use True for including script file context file	

class BOT():
    def bl(self, pl, st, ts):						
        # First greeting
        icA('Hello! How can I help you with your pet today?')
        if path.exists('Hello_friend.wav'):
            pl.play('Hello_friend.wav')
        else:
            ts.save2file(ts.tts_request('Hello! How can I help you with your pet today?'), ttsfile)
            pl.play(ttsfile)
        time.sleep(sys_delay)    
        rep_pl = 0

        while True:
            pl.record(userresponcefile)
            time.sleep(sys_delay)
            try:        
                userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
            except:
                userresponcestring  = ''
            icA(userresponcestring)
            time.sleep(sys_delay)
            if len(userresponcestring) == 0:
                icA('Sorry, could you repeat that, please?')
                if path.exists('Sorry.wav'):
                    pl.play('Sorry.wav')
                else:    
                    ts.save2file(ts.tts_request('Sorry, could you repeat that, please?'), ttsfile)
                    pl.play(ttsfile)
                time.sleep(sys_delay)
                rep_pl += 1
                if rep_pl == 3:
                    break
                else:						
                    continue

            if 'stop it' in userresponcestring:            
                icA('Ok, goodbye!')
                if path.exists('Goodbye.wav'):
                    pl.play("Goodbye.wav")
                else:    
                    ts.save2file(ts.tts_request('Goodbye!'), ttsfile)
                    pl.play(ttsfile)
                time.sleep(sys_delay)
                return
            
            if "pet status" in userresponcestring:
                icA('Fetching pet status...')
                ts.save2file(ts.tts_request('Is your pet active and healthy?'), ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)
                pl.record(userresponcefile)
                time.sleep(sys_delay)
                try:        
                    userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                except:
                    userresponcestring  = ''
                icA(userresponcestring)
                if "yes" in userresponcestring:                    
                    icA('Great! Make sure to keep your pet hydrated and exercised.')
                else:
                    icA('Let me fetch the latest health records for your pet.')
                    pet_data = da.fetch_data(db_name, 'pet_data', 'HealthRecords')
                    if pet_data.empty:
                        health_report = 'No records available.'
                    else:
                        health_report = str(pet_data)
                    ts.save2file(ts.tts_request(health_report), ttsfile)					  
                    time.sleep(sys_delay)
                    pl.play(ttsfile)
                    time.sleep(sys_delay)

            if "feeding time" in userresponcestring:
                icA('Would you like to set a feeding schedule for your pet?')
                ts.save2file(ts.tts_request('Would you like to set a feeding schedule for your pet?'), ttsfile)
                time.sleep(sys_delay)
                pl.play(ttsfile)
                time.sleep(sys_delay)
                pl.record(userresponcefile)
                time.sleep(sys_delay)
                try:
                    userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
                except:
                    userresponcestring  = ''
                icA(userresponcestring)
                if 'yes' in userresponcestring:
                    icA('Setting up the feeding schedule...')
                    # Add feeding schedule functionality here
                else:
                    icA('Let me know if you need help with anything else.')

            # Additional pet-related functionalities can be added here.

if __name__ == '__main__':
    pl = Player()
    st = STT()
    ts = TTS()    
											  
    bot = BOT()
    keyphrase='pet'
    icA('BOT started..')
    speech = LiveSpeech(lm=False, keyphrase=keyphrase, kws_threshold=1e-20)
    while 1:
        for phrase in speech:
            icA(phrase)
            if keyphrase in phrase.segments(detailed=True)[0][0]:
                bot.bl(pl, st, ts)
                icA('Ending current interaction.')
                break
