
import numpy as np
import math
import wave
import struct
import os


def detect_note_duration(audio_file):

    sampling_freq = 44100
    window = 350
    start = []  
    end = []

    file_length = audio_file.getnframes()
    sound = np.zeros(file_length)
    for i in range(file_length):
        data = audio_file.readframes(1)
        data = struct.unpack("<h", data)
        sound[i] = int(data[0])
    sound = np.divide(sound, float(2 ** 15))
    sound_square = np.square(sound)

    i = 0
    xsum = []

    while(i<(file_length) - window):
        s = 0.00
        j = 0
         
        while(j<=window):
            s = s + sound_square[i + j]
            j = j + 1

        xsum.append(s)
        i = i + window

    i = 0
    fx=0
    threshold = 0.006

    for i in range(len(xsum)):
        if xsum[i]>threshold and fx==0:
            fx=1
            start.append(i*window)
        elif xsum[i]<threshold and fx==1:
            end.append(i*window)
            fx=0
        
        else:
            continue

    if len(start)!=len(end):
        end.append(i*window)

    for z in range(len(start)):
        sx = start[z]/44100.00
        ex = end[z]/44100.00
        Note_durations.append([round(sx,2),round(ex,2)])

    return Note_durations



def detect_silence_duration(audio_file):
	

    Silence_durations = []

    # Add your code here
    sampling_freq = 44100
    window = 350
    start = []  
    end = []

    audio_file.rewind()

    file_length = audio_file.getnframes()
    sound = np.zeros(file_length)
    for i in range(file_length):
        data = audio_file.readframes(1)
        data = struct.unpack("<h", data)
        sound[i] = int(data[0])
    sound = np.divide(sound, float(2 ** 15))    
    sound_square = np.square(sound)

    i = 0
    xsum = []

    while(i<(file_length) - window):
        s = 0.00
        j = 0
         
        while(j<=window):
            s = s + sound_square[i + j]
            j = j + 1

        xsum.append(s)
        i = i + window

    i = 0
    fx = 0
    threshold = 0.006

    for i in range(len(xsum)):
        if xsum[i]>threshold and fx==0:
            fx=1
            start.append(i*window)

        elif xsum[i]<threshold and fx==1:
            end.append(i*window)
            fx=0
        
        else:
            continue

    if len(start)!=len(end):
        end.append(i*window)

    for z in range(len(start)-1):
        sx = start[z+1]/44100.00
        ex = end[z]/44100.00
        Silence_durations.append([round(ex,2),round(sx,2)])

    if (len(sound)/44100.00) - (end[z+1]/44100.00) >= 0.05:
        Silence_durations.append([round(end[z+1]/44100.00,2),round(len(sound)/44100.00,2)])

    return Silence_durations


## Main Function

if __name__ == "__main__":


    path = os.getcwd()
    
    file_name = path + "\Task_1.2B_Audio_files\Audio_1.wav"
    audio_file = wave.open(file_name)
    
    Note_durations = detect_note_duration(audio_file)  
    Silence_durations = detect_silence_duration(audio_file)

    print("\n\tNotes Duration = " + str(Note_durations))
    print("\n\tSilence Duration = " + str(Silence_durations))

    # code for checking output for all audio files
    x = raw_input("\n\tWant to check output for all Audio Files - Y/N: ")

    if x == 'Y':

        Note_durations_list = []

        Silence_durations_list = []

        file_count = len(os.listdir(path + "\Task_1.2B_Audio_files"))

        for file_number in range(1, file_count):

            file_name = path +"\Task_1.2B_Audio_files\Audio_"+str(file_number)+".wav"
            audio_file = wave.open(file_name)
            
            Note_durations = detect_note_duration(audio_file)
            Silence_durations = detect_silence_duration(audio_file)
            
            Note_durations_list.append(Note_durations)
            Silence_durations_list.append(Silence_durations)

        print("\n\tNotes Duration = " + str(Note_durations_list[0]) + ",\n\t\t\t" + str(Note_durations_list[1]) + ",\n\t\t\t" + str(Note_durations_list[2]))
        print("\n\tSilence Duration = " + str(Silence_durations_list[0]) + ",\n\t\t\t" + str(Silence_durations_list[1]) + ",\n\t\t\t" + str(Silence_durations_list[2]))
