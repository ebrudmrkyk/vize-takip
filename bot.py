import requests
import json
from datetime import datetime

def check_idata():
    # Kontrol etmek istediğin ofislerin listesi
    ofisler = [
        {"id": "1", "ad": "İstanbul (Gayrettepe)"},
        {"id": "2", "ad": "İstanbul (Altunizade)"},
        {"id": "3", "ad": "Ankara"},
        {"id": "4", "ad": "İzmir"},
        {"id": "5", "ad": "Bursa"}
    ]
    
    sonuclar = []
    su_an = datetime.now().strftime("%d/%m/%Y %H:%M")
    genel_durum = "pasif"

    print(f"{su_an} - iDATA Taraması Başladı...")

    for ofis in ofisler:
        # Gerçek iDATA sorgu simülasyonu
        # Not: iDATA gerçekte POST isteği ve güvenlik anahtarı ister.
        # Şimdilik yapıyı kuruyoruz.
        durum_metni = "Randevu Yok" 
        
        # Eğer bir ofiste randevu bulunursa 'aktif' yap
        ofis_durumu = "pasif" 
        
        sonuclar.append({
            "ofis": ofis["ad"],
            "durum": durum_metni,
            "aktif": ofis_durumu
        })

    # Veriyi kaydet
    data = {
        "son_kontrol": su_an,
        "liste": sonuclar
    }
    
    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    check_idata()
