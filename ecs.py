import csv

def cekKamus(kata):
    file_kamus = "kamus.csv"

    # Membuka file CSV dan mencari kata dalam kolom 'indonesia'
    with open(file_kamus, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['indonesia'] == kata:
                return True  # True jika ada
    
    return False  # False jika tidak ada
import re

def Del_Inflection_Suffixes(kata):
    inflection_suffixes = [r'([km]u|nya|[kl]ah|pun)$', r'([klt]ah|pun)$']

    for suffix in inflection_suffixes:
        new_kata, count = re.subn(suffix, '', kata)
        if count > 0:
            return new_kata  # Berhenti jika penghapusan dilakukan
    
    return kata  # Kembalikan kata tanpa perubahan jika tidak ada akhiran infleksi yang ditemukan


def Del_Derivation_Suffixes(kata):
    kata_asal = kata

    # Cek dan hapus akhiran -kan
    if re.search(r'(kan)$', kata):
        kata_baru = re.sub(r'(kan)$', '', kata)
        if cekKamus(kata_baru):  # Cek ke kamus
            return kata_baru

    # Cek dan hapus akhiran -an atau -i
    if re.search(r'(an|i)$', kata):
        kata_baru = re.sub(r'(an|i)$', '', kata)
        if cekKamus(kata_baru):  # Cek ke kamus
            return kata_baru

    return kata_asal  # Kembalikan kata asal jika tidak ada perubahan

def Del_Derivation_Prefix(kata):
    kata_asal = kata

    # Awalan di-, ke-, se-
    if re.match(r'^(di|[ks]e)\S{1,}', kata):
        kata_baru = re.sub(r'^(di|[ks]e)', '', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru

    # Awalan te-, me-, be-, pe-
    if re.match(r'^([tmbp]e)\S{1,}', kata):
        # Awalan be-
        if re.match(r'^(be)\S{1,}', kata):
            if re.match(r'^(ber)[aiueo]\S{1,}', kata):  # Aturan 1
                kata_baru = re.sub(r'^(ber)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(ber)', 'r', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru

            if re.match(r'^(ber)[^aiueor]\S{1,}', kata):  # Aturan 2
                kata_baru = re.sub(r'^(ber)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru

            if re.match(r'^(ber)[^aiueor][[:alpha:]]er[aiueo]\S{1,}', kata):
                kata_baru = re.sub(r'^(ber)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru

            if re.match(r'^belajar\S{0,}', kata):  # Aturan 4
                kata_baru = re.sub(r'^(bel)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru

            if re.match(r'^(be)[^aiueolr]er[^aiueo]\S{1,}', kata):  # Aturan 5
                kata_baru = re.sub(r'^(be)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru

        # Awalan te-
        if re.match(r'^(te)\S{1,}', kata):
            if re.match(r'^(terr)\S{1,}', kata):  
                return kata

            if re.match(r'^(ter)[aiueo]\S{1,}', kata):  # Aturan 6
                kata_baru = re.sub(r'^(ter)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(ter)', 'r', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru

            if re.match(r'^(ter)[^aiueor]er[aiueo]\S{1,}', kata):  # Aturan 7
                kata_baru = re.sub(r'^(ter)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru

            if re.match(r'^(ter)[^aiueor](?!er)\S{1,}', kata):  # Aturan 8
                kata_baru = re.sub(r'^(ter)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru

            if re.match(r'^(te)[^aiueor]er[aiueo]\S{1,}', kata):  # Aturan 9
                kata_baru = re.sub(r'^(te)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru

            if re.match(r'^(ter)[^aiueor]er[^aiueo]\S{1,}', kata):  # Aturan 35
                kata_baru = re.sub(r'^(ter)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
        
        # Awalan me-
        if re.match(r'^(me)\S{1,}', kata):  # Jika awalan me-
            if re.match(r'^(me)[lrwyv][aiueo]', kata):  # Aturan 10
                kata_baru = re.sub(r'^(me)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(mem)[bfvp]\S{1,}', kata):  # Aturan 11
                kata_baru = re.sub(r'^(mem)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(mem)((r[aiueo])|[aiueo])\S{1,}', kata):  # Aturan 13
                kata_baru = re.sub(r'^(mem)', 'm', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(mem)', 'p', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(men)[cdjszt]\S{1,}', kata):  # Aturan 14
                kata_baru = re.sub(r'^(men)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(men)[aiueo]\S{1,}', kata):  # Aturan 15
                kata_baru = re.sub(r'^(men)', 'n', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(men)', 't', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(meng)[ghqk]\S{1,}', kata):  # Aturan 16
                kata_baru = re.sub(r'^(meng)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(meng)[aiueo]\S{1,}', kata):  # Aturan 17
                kata_baru = re.sub(r'^(meng)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(meng)', 'k', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(menge)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(meny)[aiueo]\S{1,}', kata):  # Aturan 18
                kata_baru = re.sub(r'^(meny)', 's', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(me)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
        # awalan pe
        if re.match(r'^(pe)\S{1,}', kata):  # Jika awalan "pe-"
            
            if re.match(r'^(pe)[wy]\S{1,}', kata):  # Aturan 20
                kata_baru = re.sub(r'^(pe)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(per)[aiueo]\S{1,}', kata):  # Aturan 21
                kata_baru = re.sub(r'^(per)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(per)', 'r', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(per)[^aiueor][a-zA-Z](?!er)\S{1,}', kata): 
                kata_baru = re.sub(r'^(per)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(per)[^aiueor][a-zA-Z](er)[aiueo]\S{1,}', kata): 
                kata_baru = re.sub(r'^(per)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(pem)[bfv]\S{1,}', kata):  # Aturan 25
                kata_baru = re.sub(r'^(pem)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(pem)(r[aiueo]|[aiueo])\S{1,}', kata):  # Aturan 26
                kata_baru = re.sub(r'^(pem)', 'm', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(pem)', 'p', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(pen)[cdjzt]\S{1,}', kata):  # Aturan 27
                kata_baru = re.sub(r'^(pen)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(pen)[aiueo]\S{1,}', kata):  # Aturan 28
                kata_baru = re.sub(r'^(pen)', 'n', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(pen)', 't', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(peng)[^aiueo]\S{1,}', kata):  # Aturan 29
                kata_baru = re.sub(r'^(peng)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(peng)[aiueo]\S{1,}', kata):  # Aturan 30
                kata_baru = re.sub(r'^(peng)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(peng)', 'k', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(penge)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(peny)[aiueo]\S{1,}', kata):  # Aturan 31
                kata_baru = re.sub(r'^(peny)', 's', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = re.sub(r'^(pe)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(pel)[aiueo]\S{1,}', kata):  # Aturan 32
                kata_baru = re.sub(r'^(pel)', 'l', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(pelajar)\S{0,}', kata):  # Aturan 33
                kata_baru = re.sub(r'^(pel)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(pe)[^rwylmn]er[aiueo]\S{1,}', kata):  # Aturan 34
                kata_baru = re.sub(r'^(pe)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(pe)[^rwylmn](?!er)\S{1,}', kata):  # Aturan 35
                kata_baru = re.sub(r'^(pe)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
    
            if re.match(r'^(pe)[^aiueor]er[^aiueo]\S{1,}', kata):  # Aturan 36
                kata_baru = re.sub(r'^(pe)', '', kata)
                if cekKamus(kata_baru):
                    return kata_baru
                kata_baru = Del_Derivation_Suffixes(kata_baru)
                if cekKamus(kata_baru):
                    return kata_baru
                    
    if re.match(r'^(memper)\S{1,}', kata):
        kata_baru = re.sub(r'^(memper)', '', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru
        
        # Cek luluh -r
        kata_baru = re.sub(r'^(memper)', 'r', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru

    # Awalan "mempel-"
    if re.match(r'^(mempel)\S{1,}', kata):
        kata_baru = re.sub(r'^(mempel)', '', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru
        
        # Cek luluh -l
        kata_baru = re.sub(r'^(mempel)', 'l', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru

    # Awalan "menter-"
    if re.match(r'^(menter)\S{1,}', kata):
        kata_baru = re.sub(r'^(menter)', '', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru
        
        # Cek luluh -r
        kata_baru = re.sub(r'^(menter)', 'r', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru

    # Awalan "member-"
    if re.match(r'^(member)\S{1,}', kata):
        kata_baru = re.sub(r'^(member)', '', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru
        
        # Cek luluh -r
        kata_baru = re.sub(r'^(member)', 'r', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru

    # Awalan "diper-"
    if re.match(r'^(diper)\S{1,}', kata):
        kata_baru = re.sub(r'^(diper)', '', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru
        
        # Cek luluh -r
        kata_baru = re.sub(r'^(diper)', 'r', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru

    # Awalan "diter-"
    if re.match(r'^(diter)\S{1,}', kata):
        kata_baru = re.sub(r'^(diter)', '', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru
        
        # Cek luluh -r
        kata_baru = re.sub(r'^(diter)', 'r', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru

    # Awalan "dipel-"
    if re.match(r'^(dipel)\S{1,}', kata):
        kata_baru = re.sub(r'^(dipel)', 'l', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru
        
        # Cek luluh -l
        kata_baru = re.sub(r'^(dipel)', '', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru

    # Awalan "diber-"
    if re.match(r'^(diber)\S{1,}', kata):
        kata_baru = re.sub(r'^(diber)', '', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru
        
        # Cek luluh -l
        kata_baru = re.sub(r'^(diber)', 'r', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru

    # Awalan "keber-"
    if re.match(r'^(keber)\S{1,}', kata):
        kata_baru = re.sub(r'^(keber)', '', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru
        
        # Cek luluh -l
        kata_baru = re.sub(r'^(keber)', 'r', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru

    # Awalan "keter-"
    if re.match(r'^(keter)\S{1,}', kata):
        kata_baru = re.sub(r'^(keter)', '', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru
        
        # Cek luluh -l
        kata_baru = re.sub(r'^(keter)', 'r', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru

    # Awalan "berke-"
    if re.match(r'^(berke)\S{1,}', kata):
        kata_baru = re.sub(r'^(berke)', '', kata)
        if cekKamus(kata_baru):
            return kata_baru
        kata_baru = Del_Derivation_Suffixes(kata_baru)
        if cekKamus(kata_baru):
            return kata_baru

    # Cek ada tidaknya prefiks lainnya
    if re.match(r'^(di|[kstbmp]e)\S{1,}', kata) is None:
        return kata_asal  # Jika tidak ada awalan yang sesuai, kembalikan kata asli.

    return kata_asal  # Kembalikan kata asli jika tidak ada yang cocok

def Enhanced_CS(kata):
    kataAsal = kata

    # 1. Cek Kata di Kamus
    if cekKamus(kata):
        return kata  # Jika ada di kamus, kembalikan

    # 2. Buang Inflection Suffixes
    kata = Del_Inflection_Suffixes(kata)

    # 3. Buang Derivation Suffixes
    kata = Del_Derivation_Suffixes(kata)

    # 4. Buang Derivation Prefix
    kata = Del_Derivation_Prefix(kata)

    return kata
