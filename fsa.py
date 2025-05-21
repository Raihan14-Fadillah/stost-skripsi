# Fungsi FSA untuk memecah teks menjadi suku kata

import re
import os
from pydub import AudioSegment
from pydub.playback import play

# Path ke folder audio Madura
folder_path = "audio_madura"

# Fungsi untuk membaca file audio berdasarkan nama
def get_audio_segment(nama):
    file_path = os.path.join(folder_path, f"{nama}.mp3")
    if os.path.exists(file_path):
        return AudioSegment.from_file(file_path, format="mp3")
    else:
        return None

# Fungsi FSA untuk memecah teks menjadi suku kata
def proses_fsa(kata):
    hasil = fsa_tingkat_satu(kata)
    return hasil

# Definisi FSA 1 dan FSA 2 seperti sebelumnya
def fsa_tingkat_satu(kata):
    vocal = ["a", "â", "e", "è", "i", "o", "u", "'", "È", "Â"]
    konsonan2 = ["b", "g", "d", "j", "k"]
    kata = kata.lower()
    kata = re.sub(r'[\\-]', '', kata)
    huruf = list(kata)
    hasil1 = []
    pola = []
    i = 0

    while i < len(huruf):
        if huruf[i] == "n":
            if (i + 1 < len(huruf) and (huruf[i + 1] == "g" or huruf[i + 1] == "y") and
                (i + 2 < len(huruf) and huruf[i + 2] in vocal)):
                hasil1.append(huruf[i] + huruf[i + 1] + huruf[i + 2])
                pola.append(3)
                i += 2
            elif (i + 1 < len(huruf) and (huruf[i + 1] == "g" or huruf[i + 1] == "y")):
                hasil1.append(huruf[i] + huruf[i + 1])
                pola.append(2)
                i += 1
            elif (i + 1 < len(huruf) and huruf[i + 1] in vocal):
                hasil1.append(huruf[i] + huruf[i + 1])
                pola.append(3)
                i += 1
            else:
                hasil1.append(huruf[i])
                pola.append(2)
            hasil1.append("-")
        elif huruf[i] in konsonan2:
            if (i + 1 < len(huruf) and huruf[i + 1] == "h" and
                (i + 2 < len(huruf) and huruf[i + 2] in vocal)):
                hasil1.append(huruf[i] + huruf[i + 1] + huruf[i + 2])
                pola.append(3)
                i += 2
            elif (i + 1 < len(huruf) and huruf[i + 1] == "h"):
                hasil1.append(huruf[i] + huruf[i + 1])
                pola.append(2)
                i += 1
            elif (i + 1 < len(huruf) and huruf[i + 1] in vocal):
                hasil1.append(huruf[i] + huruf[i + 1])
                pola.append(3)
                i += 1
            else:
                hasil1.append(huruf[i])
                pola.append(2)
            hasil1.append("-")
        elif huruf[i] in vocal:
            hasil1.append(huruf[i])
            hasil1.append("-")
            pola.append(1 if huruf[i] != "'" else 4)
        else:
            if (i + 1 < len(huruf) and huruf[i + 1] in vocal):
                hasil1.append(huruf[i] + huruf[i + 1])
                pola.append(3)
                i += 1
            else:
                hasil1.append(huruf[i])
                pola.append(2)
            hasil1.append("-")
        i += 1

    return fsa_tingkat_dua(hasil1, pola)

def fsa_tingkat_dua(kata, pola):
    hasil2 = []
    arr_skt = ''.join(kata).split('-')
    i = 0

    while i < len(arr_skt):
        if i < len(pola):
            if i < len(pola) - 1 and pola[i] == 1 and (pola[i + 1] == 2 or pola[i + 1] == 4):
                hasil2.append(arr_skt[i] + arr_skt[i + 1])
                i += 1
            elif pola[i] == 1:
                hasil2.append(arr_skt[i])
            elif i < len(pola) - 2 and pola[i] == 2 and pola[i + 1] == 3 and (pola[i + 2] == 2 or pola[i + 2] == 4):
                hasil2.append(arr_skt[i] + arr_skt[i + 1] + arr_skt[i + 2])
                i += 2
            elif i < len(pola) - 1 and pola[i] == 2 and pola[i + 1] == 3:
                hasil2.append(arr_skt[i] + arr_skt[i + 1])
                i += 1
            elif i < len(pola) - 1 and pola[i] == 3 and (pola[i + 1] == 2 or pola[i + 1] == 4):
                hasil2.append(arr_skt[i] + arr_skt[i + 1])
                i += 1
            elif pola[i] == 3:
                hasil2.append(arr_skt[i])
        hasil2.append("-")
        i += 1

    return [s.strip('-') for s in hasil2 if s.strip('-')]