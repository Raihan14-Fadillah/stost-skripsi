from flask import Flask, render_template, request, jsonify
from gtts import gTTS
from pydub import AudioSegment
import io
import base64
import ngram_IndMad as NIM  # Untuk Indonesia ke Madura
import ngram_MadInd as NMI  # Untuk Madura ke Indonesia
import fsa

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    
    # Ambil data dari request JSON
    kalimat = data.get("kalimat", "").strip()
    mode = data.get("mode", "ind_to_mad")  # Default mode Indonesia ke Madura
    tingkat = data.get("tingkat", "1")  # Default tingkat untuk Madura

    if not kalimat:
        return jsonify({"translation": "Masukkan teks untuk melihat hasil terjemahan.", "audio_data": ""})
    
    if mode == "ind_to_mad":
        translation, audio_data = text_to_speech_madura(kalimat, tingkat)
    elif mode == "mad_to_ind":
        translation, audio_data = text_to_speech_indonesia(kalimat)
    else:
        return jsonify({"translation": "Mode terjemahan tidak valid.", "audio_data": ""})
    
    return jsonify({"translation": translation, "audio_data": audio_data})

# Fungsi untuk menghilangkan jeda (silence) dari awal dan akhir audio
def strip_silence(audio_segment, silence_threshold=-50.0, chunk_size=10):
    start_trim = 0
    end_trim = len(audio_segment)

    # Cari awal audio (bukan diam)
    while start_trim < len(audio_segment) and audio_segment[start_trim:start_trim + chunk_size].dBFS < silence_threshold:
        start_trim += chunk_size

    # Cari akhir audio (bukan diam)
    while end_trim > start_trim and audio_segment[end_trim - chunk_size:end_trim].dBFS < silence_threshold:
        end_trim -= chunk_size

    return audio_segment[start_trim:end_trim]

def text_to_speech_madura(kalimat, tingkat):
    # Proses Indonesia ke Madura
    output = NIM.translateNGram(kalimat, tingkat)
    hasil = NIM.indonesia_madura(output, tingkat)
    print(f"Terjemahan Madura: {hasil}")

    # Selalu pecah per suku kata, bukan per kata
    kata_list = hasil.split()

    output_audio = AudioSegment.empty()
    fade_duration = 50  # ms
    crossfade_duration = 125  # ms

    for kata in kata_list:
        suku_kata_list = fsa.proses_fsa(kata.lower())
        print(f"Kata '{kata}' dipecah menjadi suku kata: {suku_kata_list}")

        for suku_kata in suku_kata_list:
            audio_suku_kata = fsa.get_audio_segment(suku_kata)
            if audio_suku_kata is not None:
                audio_suku_kata = strip_silence(audio_suku_kata)
                audio_suku_kata = audio_suku_kata.normalize()
                audio_suku_kata = audio_suku_kata.fade_in(fade_duration).fade_out(fade_duration)

                if output_audio.duration_seconds > 0:
                    output_audio = output_audio.append(audio_suku_kata, crossfade=crossfade_duration)
                else:
                    output_audio += audio_suku_kata
            else:
                print(f"Suku kata '{suku_kata}' tidak ditemukan dalam dataset.")

    # Set sample rate dan ekspor audio
    output_audio = output_audio.set_frame_rate(44100)
    output_path = "output_madura.m4a"
    output_audio.export(output_path, format="ipod")
    print(f"Teks berhasil dikonversi ke suara. File output disimpan sebagai {output_path}")

    # Konversi ke base64
    buffer = io.BytesIO()
    output_audio.export(buffer, format="wav")
    buffer.seek(0)
    audio_data = base64.b64encode(buffer.read()).decode("utf-8")

    return hasil, audio_data

def text_to_speech_indonesia(kalimat):
    try:
        # Proses Madura ke Indonesia
        translated_words = NMI.translateNGram(kalimat, "kamus.csv")
        hasil = NMI.madura_indonesia(translated_words)
    except Exception:
        # Jika terjadi kesalahan, kembalikan kata asli
        hasil = kalimat

    # Menggunakan gTTS untuk menghasilkan audio
    tts = gTTS(text=hasil, lang="id")
    mp3_buffer = io.BytesIO()
    tts.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)

    audio = AudioSegment.from_file(mp3_buffer, format="mp3")
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    audio_data = base64.b64encode(buffer.read()).decode("utf-8")
    
    return hasil, audio_data

if __name__ == "__main__":
    app.run(debug=True)