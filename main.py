import pyaudio as au
import pygame
import time
import threading
import mutagen 
from mutagen.wave import WAVE
import wave




mic=au.PyAudio()
stream=mic.open(format=au.paInt16,channels=2,rate=44100,input=True,frames_per_buffer=2)
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
        
        


bpm=200
bcount=4
while True:
    run=False
    
    print("Select BPM")
    print()
    print("Current BPM: ",bpm)
    print("Current Count: ",bcount)
    mtnm=threading.Thread(target=playBeep,args=(bcount,bpm))
    mtnm.start()
    print("""

Select Option:

Set New BPM   [1]
Set New Count [2]
Continue      [3]

""")
    choice=int(input())
    if choice == 1:
        bpm=int(input("Enter New BPM: "))
        print("loading..")
        time.sleep(4)

    elif choice == 2:
        bcount=int(input("Enter New Count: "))
        print("loading..")
        time.sleep(4)

    elif choice == 3:
        pygame.mixer.music.stop()
        run=False
        break
    
        
    
    



rate=44100

sets=int(input("No. of Sets: "))
countin=int(input("Count-In Sets: "))
sec=int((60/bpm)*bcount*sets)
frames=[]

playBeep(bcount,bpm,num=countin)
run=False

print("Start!!")
for i in range(sec):
    data=stream.read(rate)
    frames.append(data)

    print(44100/sec)
print("done")

stream.stop_stream()
stream.close()
mic.terminate()
wf = wave.open("loop.wav", 'wb')
wf.setnchannels(2)
wf.setsampwidth(mic.get_sample_size(au.paInt16))
wf.setframerate(rate)
wf.writeframes(b''.join(frames))
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
    

