import pyaudio as au
import pygame
import time
import threading
import mutagen 
from mutagen.wave import WAVE
import wave




mic=au.PyAudio()
stream=mic.open(format=au.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=2)
stream.start_stream()
run=True

def playBeep(bcount,bp,num=-1):
    global run
    run=True
    pygame.mixer.init()
    if num ==-1:
        while run :
            pygame.mixer.music.load(r"beep1.mp3")
            pygame.mixer.music.play()
            time.sleep(60/bp)
            for i in range(bcount-1):
                pygame.mixer.music.load(r"beep2.mp3")
                pygame.mixer.music.play()
                time.sleep(60/bp)
    else:
        for i in range(num):
            pygame.mixer.music.load(r"beep1.mp3")
            pygame.mixer.music.play()
            time.sleep(60/bp)
            for i in range(bcount-1):
                pygame.mixer.music.load(r"beep2.mp3")
                pygame.mixer.music.play()
                time.sleep(60/bp)
        
class ThreadMetronome(threading.Thread):
    def __init__(self,bcount,bp,num=-1):
        threading.Thread.__init__(self)
        self.bcount=bcount
        self.bp=bp
        self.num=num

    def setBPM(self,bp):
        self.bp=bp
    def setCount(self,bcount):
        self.bcount=bcount

    def run(self):
        global mtnm
        mtnm=threading.Thread(target=playBeep,args=(self.bcount,self.bp,self.num))
        mtnm.start()      

    def stop(self):
        global run
        run=False
        mtnm.join() 



bpm=160
bcount=4
met=ThreadMetronome(bcount,bpm)
met.run()
while True:
    
    print("Select BPM")
    print()
    print("Current BPM: ",bpm)
    print("Current Count: ",bcount)
    print("""

Select Option:

Set New BPM   [1]
Set New Count [2]
Continue      [3]
Exit          [4]

""")
    choice=int(input())
    if choice == 1:
        met.stop()
        bpm=int(input("Enter New BPM: "))
        print("loading..")
        met.setBPM(bpm)
        time.sleep(0.5)
        met.run()
        

    elif choice == 2:
        met.stop()
        bcount=int(input("Enter New Count: "))
        print("loading..")
        met.setCount(bcount)
        time.sleep(0.5)
        met.run()

    elif choice == 3:
        met.stop()
        pygame.mixer.music.stop()
        run=False
        break

    elif choice == 4:
        met.stop()
        exit()  
        
    
    



import numpy as np
rate = 44100
BUFFER_SIZE = 1024

sets = int(input("No. of Sets: "))
countin = int(input("Count-In Sets: "))

trim_start_time = 0.1 
trim_end_time = 0.14  
duration = (60 / bpm) * bcount * sets 
extra_time = trim_start_time + trim_end_time
total_frames = int(rate * (duration + extra_time))
frames = []

playBeep(bcount, bpm, num=countin)
run = False

print("Start!!")
frames_recorded = 0
while frames_recorded < total_frames:
    to_read = min(BUFFER_SIZE, total_frames - frames_recorded)
    data = stream.read(to_read)
    frames.append(data)
    frames_recorded += to_read
print("done")

stream.stop_stream()
stream.close()
mic.terminate()



audio_data = b''.join(frames)
audio_np = np.frombuffer(audio_data, dtype=np.int16)

trim_start = int(rate * trim_start_time)
intended_samples = int(rate * duration)
if len(audio_np) > (trim_start + intended_samples):
    audio_np = audio_np[trim_start:trim_start + intended_samples]
boost_factor = 2.0  
audio_np = np.clip(audio_np * boost_factor, -32768, 32767).astype(np.int16)
audio_data_boosted = audio_np.tobytes()

wf = wave.open("loop.wav", 'wb')
wf.setnchannels(1)
wf.setsampwidth(2)  
wf.setframerate(rate)
wf.writeframes(audio_data_boosted)
wf.close()
audio = WAVE("loop.wav")
audio_info = audio.info
length = int(audio_info.length)
print("Computed")

while True:
    print("playing")
    pygame.mixer.music.load(r"loop.wav")
    pygame.mixer.music.play()
    time.sleep(length)
    

