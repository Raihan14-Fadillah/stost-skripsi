import pandas as pd

def cek_kamus(kata):
    # Load the CSV file
    try:
        df = pd.read_csv('kamus.csv')
    except FileNotFoundError:
        print("File 'kamus.csv' not found.")
        return False
    
    # Check if the word exists in the 'madura' column
    if kata in df['madura'].values:
        return True
    else:
        return False

import re

def cek_rule_precedence(kata):
    # Definisikan pola ekspresi reguler
    pattern = r"(^è[^0-9]+(èpon|na)$)|(^a[^0-9]+èpon$)|(^ta[^0-9]+(è|wi|en|ana|aghi)$)|" \
              r"(^sa[^0-9]+(è|wi|nè)$)|(^pè[^0-9]+(è|wi|nè|en|wen)$)|(^pan[^0-9]+(è|wi|nè|en)$)|" \
              r"(^pam[^0-9]+(è|wi|nè|en)$)|(^pang[^0-9]+(è|wi|nè|en))|(^n[aiueo])|(^ny[aiueo])|" \
              r"(^m[aiueo])|(^ng[aiueo])"
    
    # Cek apakah kata sesuai dengan pola yang dilarang
    if re.search(pattern, kata, re.IGNORECASE):
        return True  # Jika ada kombinasi yang dilarang, kembalikan nilai True
    else:
        return False  # Jika tidak ada, kembalikan nilai False

def hapus_possesive_pronoun(kata, akhiran):
    if not cek_kamus(kata):
        # Memeriksa dan menangkap suffix yang sesuai
        match = re.search(r"(na|èpon|\Dèpon)$", kata, re.IGNORECASE)
        if match:
            # Menghapus pronomina posesif
            kata = kata[: -len(match.group(0))]  # Hapus berdasarkan panjang dari suffix yang ditemukan
            akhiran = f"{akhiran}-{match.group(0)}" if akhiran else match.group(0)

    return kata

def hapus_derivation_suffixes(kata, akhiran):
    if not cek_kamus(kata):  # Jika kata tidak ada di kamus
        # Pola untuk mencocokkan sufiks derivasi
        if re.search(r"(e|è|wi|nè|â|a|wa|an|yan|wan|en|wen|na|ana|wana|yana|aghi|waghi|yaghi)$", kata, re.IGNORECASE):
            suffixes = re.findall(r"(e|è|wi|nè|â|a|wa|an|yan|wan|en|wen|na|ana|wana|yana|aghi|waghi|yaghi)$", kata, re.IGNORECASE)
            kata = re.sub(r"(e|è|wi|nè|â|a|wa|an|yan|wan|en|wen|na|ana|wana|yana|aghi|waghi|yaghi)$", "", kata, flags=re.IGNORECASE)
            
            akhiran = f"{akhiran}-{suffixes[0]}" if suffixes else akhiran
            
            # Jika huruf terakhir adalah huruf konsonan rangkap 2, hapus huruf terakhir
            if re.search(r"[^aiueog]{2}$", kata):  # Cek apakah 2 huruf konsonan terakhir
                kata = re.sub(r"[^aiueo]$", "", kata)  # Kecuali g, a, i, u, e, o
                
    return kata

def hapus_derivation_prefixes(kata, awalan):
    awalanprev = ""  # Deklarasi dan inisialisasi awalanprev

    for i in range(1, 4):  # Loop hingga 3 kali
        if not cek_kamus(kata):  # Jika kata tidak ada di kamus
            # Pemotongan biasa
            match = re.match(r"^(e|è|a|ta|ma|ka|sa|pa|koma|kamè|kapè|pè|pan|pam|pang)", kata)
            if match:
                if awalanprev != match.group(0):
                    kata = re.sub(r"^(e|è|a|ta|ma|ka|sa|pa|koma|kamè|kapè|pè|pan|pam|pang)", "", kata)
                    awalan += match.group(0)  # Simpan awalan sebagai parameter output
                    awalanprev = match.group(0)

            # Pemotongan bermorfologi
            match_n = re.match(r"^n[aiueo]", kata)
            if match_n:
                if awalanprev != match_n.group(0):
                    kata = re.sub(r"^n", "t", kata)
                    awalan += match_n.group(0).replace("n", "")  # Simpan awalan sebagai parameter output
                    awalanprev = match_n.group(0)

            match_ny = re.match(r"^ny[aiueo]", kata)
            if match_ny:
                if awalanprev != match_ny.group(0):
                    kata = re.sub(r"^ny", "s", kata)
                    awalan += match_ny.group(0).replace("ny", "")  # Simpan awalan sebagai parameter output
                    awalanprev = match_ny.group(0)

            match_m = re.match(r"^m[aiueo]", kata)
            if match_m:
                if awalanprev != match_m.group(0):
                    kata = re.sub(r"^m", "p", kata)
                    awalan += match_m.group(0).replace("m", "")  # Simpan awalan sebagai parameter output
                    awalanprev = match_m.group(0)

            match_ng = re.match(r"^ng[aiueo]", kata)
            if match_ng:
                if awalanprev != match_ng.group(0):
                    kata = re.sub(r"^ng", "k", kata)
                    awalan += match_ng.group(0).replace("ng", "")  # Simpan awalan sebagai parameter output
                    if not cek_kamus(kata):  # Jika tidak ada di kamus, hapus huruf k di awal
                        kata = re.sub(r"^k", "", kata)
                    awalanprev = match_ng.group(0)
        else:  # Jika ada di kamus, hentikan perulangan
            break

    return kata

def hapus_sisipan(kata):
    kataAwal = kata

    if not cek_kamus(kata):  # Jika tidak ada di kamus
        # Memeriksa dan menghapus sisipan
        match = re.match(r"^[^0-9]+(al|ar|en|in|om|um|am)", kata, re.IGNORECASE)
        if match:
            kata = re.sub(r"(al|ar|um|en|in|om|am)", "", kata, count=1, flags=re.IGNORECASE)

    if cek_kamus(kata):  # Memeriksa apakah kata yang dimodifikasi ada di kamus
        return kata  # Jika ada, kembalikan kata yang telah dipotong
    else:
        return kataAwal  # Jika tidak ada, kembalikan kata awal

def hapus_awalan(kata):
    awalanprev = ""  # Deklarasi dan inisialisasi awalanprev
    awalan = ""      # Deklarasi dan inisialisasi awalan

    if not cek_kamus(kata):  # Jika tidak ada di kamus
        # Pemotongan biasa
        match = re.match(r"^(e|è|a|ta|ma|ka|sa|pa|koma|kamè|kapè|pè|pan|pam|pang)", kata)
        if match:
            if awalanprev != match.group(0):
                kata = re.sub(r"^(e|è|a|ta|ma|ka|sa|pa|koma|kamè|kapè|pè|pan|pam|pang)", "", kata)
                awalan += match.group(0)  # Simpan awalan sebagai parameter output
                awalanprev = match.group(0)

        # Pemotongan bermorfologi
        match_n = re.match(r"^n[aiueo]", kata)
        if match_n:
            if awalanprev != match_n.group(0):
                kata = re.sub(r"^n", "t", kata)
                awalan += match_n.group(0).replace("n", "")  # Simpan awalan sebagai parameter output
                awalanprev = match_n.group(0)

        match_ny = re.match(r"^ny[aiueo]", kata)
        if match_ny:
            if awalanprev != match_ny.group(0):
                kata = re.sub(r"^ny", "s", kata)
                awalan += match_ny.group(0).replace("ny", "")  # Simpan awalan sebagai parameter output
                awalanprev = match_ny.group(0)

        match_m = re.match(r"^m[aiueo]", kata)
        if match_m:
            if awalanprev != match_m.group(0):
                kata = re.sub(r"^m", "p", kata)
                awalan += match_m.group(0).replace("m", "")  # Simpan awalan sebagai parameter output
                awalanprev = match_m.group(0)

        match_ng = re.match(r"^ng[aiueo]", kata)
        if match_ng:
            if awalanprev != match_ng.group(0):
                kata = re.sub(r"^ng", "k", kata)
                awalan += match_ng.group(0).replace("ng", "")  # Simpan awalan sebagai parameter output
                awalanprev = match_ng.group(0)

    return kata

def loop_pengembalian_akhiran(kata, prefix, suffix):
    akhiran = suffix.split("-")  # Simpan suffix di variabel akhiran sebagai list
    
    # Proses pengembalian prefix
    if prefix.strip() == "n":
        kata = re.sub(r"^t", "n", kata)
    elif prefix.strip() == "ny":
        kata = re.sub(r"^s", "ny", kata)
    elif prefix.strip() == "m":
        kata = re.sub(r"^p", "m", kata)
    elif prefix.strip() == "ng":
        kata = re.sub(r"^k", "ng", kata)
    else:
        kata = prefix + kata  # Kembalikan awalan yang telah dihapus

    kata = hapus_awalan(kata)  # Hilangkan awalan per-imbuhan

    for suffix_item in akhiran:  # Lakukan pengembalian akhiran per-imbuhan
        if cek_kamus(kata):  # Jika kata ditemukan di kamus
            break  # Hentikan loop jika kata sudah ditemukan
        else:
            # Jika tidak ada di kamus, tambahkan akhiran lalu hapus awalan
            kata += suffix_item
            kata = hapus_awalan(kata)

    # Cek apakah setelah loop kata ada di kamus
    if not cek_kamus(kata):
        if prefix.strip() == "n":
            kata = re.sub(r"^t", "n", kata)
        elif prefix.strip() == "ny":
            kata = re.sub(r"^s", "ny", kata)
        elif prefix.strip() == "m":
            kata = re.sub(r"^p", "m", kata)
        elif prefix.strip() == "ng":
            kata = re.sub(r"^k", "ng", kata)
        else:
            kata = prefix + kata  # Kembalikan awalan yang telah dihapus

    return kata

def ecs_madura(kata, terater, panoteng):
    pp = ""  # Pronouns posesif
    ds = ""   # Akhiran derivasi
    dp = ""   # Awalan derivasi
    kata = kata.strip()
    kata_awal = kata  # Simpan kata awal
    if "-" in kata:  # Periksa apakah ada tanda penghubung
        kata = kata.split("-")  # Pecah kata berdasarkan tanda penghubung
        if cek_rule_precedence(kata[1]):  # Jika rule precedence true
            kata[0] = hapus_sisipan(hapus_derivation_suffixes(hapus_possesive_pronoun(hapus_derivation_prefixes(kata[0], dp), pp), ds))
            kata[1] = hapus_sisipan(hapus_derivation_suffixes(hapus_possesive_pronoun(hapus_derivation_prefixes(kata[1], dp), pp), ds))
            kata = kata[1]  # Ambil kata kedua
        else:  # Jika rule precedence false
            kata[0] = hapus_sisipan(hapus_derivation_prefixes(hapus_derivation_suffixes(hapus_possesive_pronoun(kata[0], pp), ds), dp))
            kata[1] = hapus_sisipan(hapus_derivation_prefixes(hapus_derivation_suffixes(hapus_possesive_pronoun(kata[1], pp), ds), dp))
            kata = kata[1]  # Ambil kata kedua
    else:  # Jika tidak ada kata penghubung
        if cek_rule_precedence(kata[1]):  # Jika rule precedence true
            kata = hapus_sisipan(hapus_derivation_suffixes(hapus_possesive_pronoun(hapus_derivation_prefixes(kata, dp), pp), ds))
        else:
            kata = hapus_sisipan(hapus_derivation_prefixes(hapus_derivation_suffixes(hapus_possesive_pronoun(kata, pp), ds), dp))
            if len(kata) == 1:
                kata = kata_awal  # Kembalikan kata ke bentuk awal

    if not cek_kamus(kata):  # Jika setelah penghapusan masih tidak ada di kamus
        kata = loop_pengembalian_akhiran(kata, dp, f"{ds}{pp}")  # Lakukan loop_pengembalian_akhiran()

    if not cek_kamus(kata):  # Jika setelah loop kata yang di stem tidak ada di kamus
        kata = kata_awal  # Kembalikan kata awal
        
    terater = dp
    panoteng = ds+pp
    
    return kata