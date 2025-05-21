
import pandas as pd
import ecs 

def getIndexArray(kata, array):
    try:
        return array.index(kata)
    except ValueError:
        return None

def determineTingkatFilter(tingkat):
    if tingkat == "1":
        filter_tingkatan = ["lomrah", None]
    elif tingkat == "2":
        filter_tingkatan = ["tengngaan", "alos", None]
    elif tingkat == "3":
        filter_tingkatan = ["alos tengghi", None]
    else:
        filter_tingkatan = []  # Jika tingkat tidak sesuai, tidak ada filter tingkatan khusus.
    return filter_tingkatan

def translateNGram(input, tingkat):
    # Membaca data dari kamus.csv
    kamus = pd.read_csv('kamus.csv')
    
    # Mengubah input menjadi lowercase dan menghapus spasi di awal/akhir
    input = input.strip().lower()
    
    # Memecah input menjadi array kata
    inputWords = input.split(" ")
    
    # Output array untuk menyimpan hasil terjemahan
    translatedArray = []
    
    # Menentukan filter tingkatan
    filter_tingkatan = determineTingkatFilter(tingkat)
    
    # Loop untuk memproses setiap kata/bigram/trigram
    i = 0
    while i < len(inputWords):
        # Proses bigram
        if i + 1 < len(inputWords):
            bigram = " ".join(inputWords[i:i+2])  # Membentuk bigram
            # Filter bigram dari kamus
            filtered_kamus = kamus[
                (kamus['indonesia'].str.startswith(bigram)) & 
                (kamus['tingkatan'].isin(filter_tingkatan) | kamus['tingkatan'].isna())
            ]
            
            if not filtered_kamus.empty:
                # Cek trigram jika bigram ditemukan
                if i + 2 < len(inputWords):
                    trigram = " ".join(inputWords[i:i+3])  # Membentuk trigram
                    trigram_result = filtered_kamus[filtered_kamus['indonesia'] == trigram]
                    
                    if not trigram_result.empty:
                        # Jika trigram ditemukan, tambahkan hasil terjemahan
                        translatedArray.append(trigram_result.iloc[0]['madura'])
                        i += 3
                        continue  # Lanjutkan ke iterasi berikutnya
                    
                # Jika trigram tidak ditemukan, gunakan bigram
                bigram_result = filtered_kamus[filtered_kamus['indonesia'] == bigram]
                if not bigram_result.empty:
                    translatedArray.append(bigram_result.iloc[0]['madura'])
                    i += 2
                    continue  # Lanjutkan ke iterasi berikutnya
        
        # Jika bigram tidak ditemukan, proses unigram
        unigram = inputWords[i]
        unigram_result = kamus[
            (kamus['indonesia'] == unigram) & 
            (kamus['tingkatan'].isin(filter_tingkatan) | kamus['tingkatan'].isna())
        ]
        
        if not unigram_result.empty:
            # Jika unigram ditemukan, tambahkan hasil terjemahan
            translatedArray.append(unigram_result.iloc[0]['madura'])
        else:
            # Jika unigram tidak ditemukan, tambahkan kata asli
            translatedArray.append(unigram)
        
        i += 1  # Lanjutkan ke kata berikutnya

    return " ".join(translatedArray)  # Menggabungkan array menjadi satu string

def indonesia_madura(kalimat, tingkat):
    # Load data dari CSV menggunakan pandas
    def load_csv(file_path):
        return pd.read_csv(file_path)

    kamus = load_csv('kamus.csv')
    imbuhan_indo = load_csv('imbuhan_indo.csv')

    # Hilangkan tanda baca
    tanda = ['(', ')', '.', ',', '?', '!', '\\', ':', ';', '"']
    kalimat_asli = kalimat
    kalimat = ''.join(char for char in kalimat if char not in tanda).strip()

    arr_kata_asli = kalimat_asli.split(" ")
    kata = kalimat.split(" ")

    # Filter tingkatan
    filter_tingkatan = []
    if tingkat == "1":
        filter_tingkatan = [None, "lomrah"]
    elif tingkat == "2":
        filter_tingkatan = [None, "tengngaan", "alos"]
    elif tingkat == "3":
        filter_tingkatan = [None, "alos tengghi"]
    else:
        filter_tingkatan = [None]  # Untuk kata umum yang tingkatannya null

    # Stemming kata
    kata_stem = [ecs.Enhanced_CS(word) for word in kata]

    # Proses terjemahan
    kata_madura = []
    jenis_kata = []

    for nomor, isi in enumerate(kata_stem):
        kata_asli = arr_kata_asli[nomor]
        kata_asal = kata[nomor]
        tanda_baca = kata_asli.replace(kata_asal, '')

        # Cari di kamus menggunakan pandas
        hasil = kamus[kamus['indonesia'] == isi]

        # Filter berdasarkan tingkatan, jika tidak ada tingkatan maka None juga valid
        hasil = hasil[hasil['tingkatan'].isin(filter_tingkatan) | hasil['tingkatan'].isna()]

        if not hasil.empty:
            hasil_row = hasil.iloc[0]  # Ambil baris pertama jika ada hasil yang cocok
            kata_madura.append(hasil_row['madura'])
            jenis_kata.append(hasil_row['keterangan'])

            # Proses imbuhan
            imbuhan = kata_asal.replace(isi, '#')
            arrImbuhan = imbuhan.split('#')

            awalan = arrImbuhan[0].strip() if len(arrImbuhan) > 0 else ''
            akhiran = arrImbuhan[1].strip() if len(arrImbuhan) > 1 else ''

            arti_awalan = ''
            arti_akhiran = ''

            if awalan and not akhiran:
                imb_row = imbuhan_indo[(imbuhan_indo['awalan'] == awalan) & (imbuhan_indo['letak'] == 'awalan')]
                if not imb_row.empty:
                    arti_awalan = imb_row.iloc[0]['arti_awalan']
            
            if akhiran and not awalan:
                imb_row = imbuhan_indo[(imbuhan_indo['akhiran'] == akhiran) & (imbuhan_indo['letak'] == 'akhiran')]
                if not imb_row.empty:
                    arti_akhiran = imb_row.iloc[0]['arti_akhiran']

            if awalan and akhiran:
                imb_row = imbuhan_indo[(imbuhan_indo['awalan'] == awalan) & (imbuhan_indo['akhiran'] == akhiran) & (imbuhan_indo['letak'] == 'awalan akhiran')]
                if not imb_row.empty:
                    arti_awalan = imb_row.iloc[0]['arti_awalan']
                    arti_akhiran = imb_row.iloc[0]['arti_akhiran']

            kata_madura[nomor] = arti_awalan + kata_madura[nomor] + arti_akhiran + tanda_baca
        else:
            kata_madura.append(isi + tanda_baca)
            jenis_kata.append('xxx')

    kalimat_madura = " ".join(kata_madura)
    return kalimat_madura