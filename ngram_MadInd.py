import pandas as pd
import ecsmad as ec

def getIndexArray(kata, array):
    try:
        return array.index(kata)
    except ValueError:
        return None

def translateNGram(input_text, kamus_file):
    input_text = input_text.strip()  # Menghapus spasi di awal/akhir kalimat

    # Ubah teks menjadi lowercase
    lowercase_input = input_text.lower()

    # Split input menjadi array kata
    input_words = lowercase_input.split()

    # Output array untuk menampung hasil terjemahan
    translated_array = []

    # Baca kamus dari file CSV
    kamus_df = pd.read_csv(kamus_file)

    # Loop melalui setiap kata dalam input
    i = 0
    while i < len(input_words):
        # Cek untuk bigram
        if i + 1 < len(input_words):
            bigram = " ".join(input_words[i:i+2])  # Bentuk bigram
            bigram_matches = kamus_df[kamus_df['madura'].str.contains(bigram, case=False, na=False)]

            if not bigram_matches.empty:
                # Bigram ditemukan, cek trigram
                if i + 2 < len(input_words):
                    trigram = " ".join(input_words[i:i+3])  # Bentuk trigram

                    # Cek trigram
                    trigram_matches = kamus_df[kamus_df['madura'].str.contains(trigram, case=False, na=False)]
                    if not trigram_matches.empty:
                        # Trigram ditemukan, terjemahkan
                        row_trigram = trigram_matches.iloc[0]  # Ambil hasil pertama
                        translated_array.append(row_trigram['indonesia'])  # Simpan hasil terjemahan
                        i += 3  # Lewati trigram yang sudah diproses
                        continue  # Lanjutkan ke iterasi berikutnya

                # Cek bigram
                if not bigram_matches.empty:
                    row_bigram = bigram_matches.iloc[0]  # Ambil hasil pertama
                    translated_array.append(row_bigram['indonesia'])  # Simpan hasil terjemahan
                    i += 2  # Lewati bigram yang sudah diproses
                    continue  # Lanjutkan ke iterasi berikutnya

        # Jika bigram tidak ditemukan, lanjutkan ke unigram
        unigram = input_words[i]
        unigram_matches = kamus_df[kamus_df['madura'] == unigram]

        if not unigram_matches.empty:
            row_unigram = unigram_matches.iloc[0]  # Ambil hasil pertama
            translated_array.append(row_unigram['indonesia'])  # Simpan hasil terjemahan
        else:
            translated_array.append(unigram)  # Jika tidak ada di kamus, tambahkan kata asli

        i += 1  # Lanjutkan ke kata berikutnya

    # Gabungkan hasil terjemahan menjadi satu string, dipisahkan spasi
    return " ".join(translated_array)  # Kembalikan hasil terjemahan sebagai string
    
def madura_indonesia(kalimat):
    # Baca data dari kamus.csv dan imbuhan_madura.csv
    kamus = pd.read_csv('kamus.csv')
    imbuhan_madura = pd.read_csv('imbuhan_madura.csv')

    # Tanda baca yang akan dihapus
    tanda = ['(', ')', '.', ',', '?', '!', '\\', ':', ';', '"']

    kalimat_asli = kalimat
    kalimat = kalimat.translate(str.maketrans('', '', ''.join(tanda)))

    arr_kata_asli = kalimat_asli.split()
    kata = kalimat.split()

    # Stem setiap kata menggunakan ecs_madura
    kata_stem = []
    for ind, value in enumerate(kata):
        awalan, akhiran = [], []
        hasil_stem = ec.ecs_madura(value, awalan, akhiran)
        kata_stem.append(hasil_stem)
        
    # Terjemahkan setiap kata yang di-stem
    kata_indo = []
    for nomor, isi in enumerate(kata_stem):
        kata_asli = arr_kata_asli[nomor]
        kata_asal = kata[nomor]
        tanda_baca = kata_asli.replace(kata_asal, '')

        hasil_kamus = kamus[kamus['madura'] == isi]
        if not hasil_kamus.empty:
            hasil = hasil_kamus.iloc[0]
            kata_indo_word = hasil['indonesia']
            kata_indo.append(kata_indo_word + tanda_baca)
        else:
            kata_indo.append(isi + tanda_baca)

    # Gabungkan hasil terjemahan
    kalimat_indo = ' '.join(kata_indo)

    return kalimat_indo
