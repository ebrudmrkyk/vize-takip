import requests
import json
from datetime import datetime

def check_appointments():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    # SORGULANACAK TAM LİSTE
    sorgu_listesi = [
        # ALMANYA (iDATA - type: 1)
        {"ulke": "Almanya", "ad": "İstanbul (Gayrettepe)", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "1", "office": "1", "type": "1"}},
        {"ulke": "Almanya", "ad": "İstanbul (Altunizade)", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "1", "office": "2", "type": "1"}},
        {"ulke": "Almanya", "ad": "Ankara", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "2", "office": "3", "type": "1"}},
        {"ulke": "Almanya", "ad": "İzmir", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "3", "office": "4", "type": "1"}},
        {"ulke": "Almanya", "ad": "Bursa", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "1", "office": "5", "type": "1"}},
        
        # İTALYA (iDATA - type: 2)
        {"ulke": "İtalya", "ad": "İstanbul (Gayrettepe)", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "1", "office": "1", "type": "2"}},
        {"ulke": "İtalya", "ad": "İstanbul (Altunizade)", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "1", "office": "2", "type": "2"}},
        {"ulke": "İtalya", "ad": "Ankara", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "2", "office": "3", "type": "2"}},
        {"ulke": "İtalya", "ad": "İzmir", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "3", "office": "4", "type": "2"}},
        
        # İSPANYA (BLS)
        {"ulke": "İspanya", "ad": "İstanbul", "url": "https://turkey.blsspainvisa.com/istanbul/index.php", "params": None},
        {"ulke": "İspanya", "ad": "Ankara", "url": "https://turkey.blsspainvisa.com/ankara/index.php", "params": None}
    ]
    
    sonuclar = []
    su_an = datetime.now().strftime("%d/%m/%Y %H:%M")

    for madde in sorgu_listesi:
        try:
            if madde["ulke"] == "İspanya":
                response = requests.get(madde["url"], headers=headers, timeout=15)
                res_text = response.text.lower()
                bulundu_mu = any(x in res_text for x in ["appointment available", "randevu uygun", "tarih seç"])
            else:
                response = requests.get(madde["url"], params=madde["params"], headers=headers, timeout=10)
                res_text = response.text.lower()
                bulundu_mu = any(x in res_text for x in ["müsait", "available", "seçiniz", "2026"])
            
            sonuclar.append({
                "kimlik": f"{madde['ulke']}-{madde['ad']}-{madde.get('params', {}).get('type', '')}",
                "ulke": madde["ulke"],
                "ofis": madde["ad"],
                "durum": "✅ RANDEVU VAR!" if bulundu_mu else "❌ Randevu Yok",
                "aktif": "aktif" if bulundu_mu else "pasif"
            })
        except:
            sonuclar.append({
                "kimlik": f"{madde['ulke']}-{madde['ad']}-hata",
                "ulke": madde["ulke"],
                "ofis": madde["ad"],
                "durum": "⚠️ Hata",
                "aktif": "pasif"
            })

    data = {"son_kontrol": su_an, "liste": sonuclar}
    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    check_appointments()
