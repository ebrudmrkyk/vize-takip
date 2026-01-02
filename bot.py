import requests
import json
from datetime import datetime, timedelta

def check_appointments():
    # Gerçek bir tarayıcı kimliği
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }

    # TÜRKİYE SAATİ AYARI (UTC + 3)
    tr_saati = datetime.utcnow() + timedelta(hours=3)
    su_an = tr_saati.strftime("%d/%m/%Y %H:%M")

    # SORGULANACAK TÜM ÜLKELER VE OFİSLER (ANKARA ÖNCELİKLİ)
    sorgu_listesi = [
        {"ulke": "Macaristan", "ad": "Ankara", "type": "vfs", "url": "https://visa.vfsglobal.com/tur/tr/hun/interim"},
        {"ulke": "Danimarka", "ad": "Ankara", "type": "vfs", "url": "https://visa.vfsglobal.com/tur/tr/dnk/interim"},
        {"ulke": "Romanya", "ad": "Ankara", "type": "vfs", "url": "https://visa.vfsglobal.com/tur/tr/rou/interim"},
        {"ulke": "Almanya", "ad": "Ankara", "type": "idata", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "2", "office": "3", "type": "1"}},
        {"ulke": "İtalya", "ad": "Ankara", "type": "idata", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "2", "office": "3", "type": "2"}},
        {"ulke": "İspanya", "ad": "Ankara", "type": "bls", "url": "https://turkey.blsspainvisa.com/ankara/index.php"},
        {"ulke": "Yunanistan", "ad": "İstanbul", "type": "vfs", "url": "https://visa.vfsglobal.com/tur/tr/grc/interim"},
        {"ulke": "Fransa", "ad": "İstanbul", "type": "vfs", "url": "https://visa.vfsglobal.com/tur/tr/fra/interim"},
        {"ulke": "Hollanda", "ad": "İstanbul", "type": "vfs", "url": "https://visa.vfsglobal.com/tur/tr/nld/interim"}
    ]
    
    sonuclar = []

    for madde in sorgu_listesi:
        try:
            if madde["type"] == "vfs":
                response = requests.get(madde["url"], headers=headers, timeout=25)
                res_text = response.text.lower()
                bulundu_mu = any(x in res_text for x in ["available", "tarih seç", "randevu al"]) and "no slots" not in res_text
            
            elif madde["type"] == "bls":
                response = requests.get(madde["url"], headers=headers, timeout=20)
                bulundu_mu = any(x in response.text.lower() for x in ["available", "randevu uygun", "booking"])
            
            else: # idata
                response = requests.get(madde["url"], params=madde["params"], headers=headers, timeout=15)
                bulundu_mu = any(x in response.text.lower() for x in ["müsait", "available", "2026"])
            
            sonuclar.append({
                "kimlik": f"{madde['ulke']}-{madde['ad']}",
                "ulke": madde["ulke"],
                "ofis": madde["ad"],
                "durum": "✅ RANDEVU VAR!" if bulundu_mu else "❌ Randevu Yok",
                "aktif": "aktif" if bulundu_mu else "pasif"
            })
        except:
            sonuclar.append({"kimlik": f"{madde['ulke']}-{madde['ad']}", "ulke": madde["ulke"], "ofis": madde["ad"], "durum": "⚠️ Hata", "aktif": "pasif"})

    # Dosyaya Yazma
    data = {"son_kontrol": su_an, "liste": sonuclar}
    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    check_appointments()
