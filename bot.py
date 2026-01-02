import requests
import json
from datetime import datetime

def check_appointments():
    # Daha geniş bir tarayıcı kimliği listesi kullanıyoruz
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    sorgu_listesi = [
        # ALMANYA ve İTALYA bölümleri aynı kalabilir...
        {"ulke": "Almanya", "ad": "İstanbul", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "1", "office": "1", "type": "1"}},
        {"ulke": "İtalya", "ad": "İstanbul", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "1", "office": "1", "type": "2"}},
        # İSPANYA (BLS) - URL'leri daha doğrudan hale getirdik
        {"ulke": "İspanya", "ad": "İstanbul", "url": "https://turkey.blsspainvisa.com/istanbul/index.php", "params": None},
        {"ulke": "İspanya", "ad": "Ankara", "url": "https://turkey.blsspainvisa.com/ankara/index.php", "params": None}
    ]
    
    sonuclar = []
    su_an = datetime.now().strftime("%d/%m/%Y %H:%M")

    for madde in sorgu_listesi:
        try:
            # timeout süresini 30 saniyeye çıkardık ki site yavaşsa hata vermesin
            if madde["ulke"] == "İspanya":
                response = requests.get(madde["url"], headers=headers, timeout=30)
            else:
                response = requests.get(madde["url"], params=madde["params"], headers=headers, timeout=20)
            
            res_text = response.text.lower()
            
            # BLS için anahtar kelimeleri genişlettik
            bulundu_mu = any(x in res_text for x in ["appointment available", "randevu uygun", "tarih seç", "booking", "müsait"])
            
            sonuclar.append({
                "kimlik": f"{madde['ulke']}-{madde['ad']}",
                "ulke": madde["ulke"],
                "ofis": madde["ad"],
                "durum": "✅ RANDEVU VAR!" if bulundu_mu else "❌ Randevu Yok",
                "aktif": "aktif" if bulundu_mu else "pasif"
            })
        except Exception as e:
            # Hatanın ne olduğunu GitHub Actions loglarında görmek için:
            print(f"Hata detayı ({madde['ulke']}-{madde['ad']}): {e}")
            sonuclar.append({
                "kimlik": f"{madde['ulke']}-{madde['ad']}",
                "ulke": madde["ulke"],
                "ofis": madde["ad"],
                "durum": "⚠️ Site Erişilemez",
                "aktif": "pasif"
            })

    # Kayıt işlemi...
    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump({"son_kontrol": su_an, "liste": sonuclar}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    check_appointments()
