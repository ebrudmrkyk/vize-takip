import requests
import json
from datetime import datetime

def check_idata():
    url = "https://idata.com.tr/vi/control/check-appointment-status"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    # iDATA üzerindeki tüm ülkeler ve ofisleri
    sorgu_listesi = [
        # ALMANYA OFİSLERİ
        {"ulke": "Almanya", "ad": "İstanbul (Gayrettepe)", "city": "1", "office": "1", "type": "1"},
        {"ulke": "Almanya", "ad": "Ankara", "city": "2", "office": "3", "type": "1"},
        {"ulke": "Almanya", "ad": "İzmir", "city": "3", "office": "4", "type": "1"},
        # İTALYA OFİSLERİ
        {"ulke": "İtalya", "ad": "İstanbul (Gayrettepe)", "city": "1", "office": "1", "type": "2"},
        {"ulke": "İtalya", "ad": "Ankara", "city": "2", "office": "3", "type": "2"},
        {"ulke": "İtalya", "ad": "İzmir", "city": "3", "office": "4", "type": "2"}
    ]
    
    sonuclar = []
    su_an = datetime.now().strftime("%d/%m/%Y %H:%M")

    for madde in sorgu_listesi:
        try:
            # type=1 Almanya, type=2 İtalya (Genel temsil)
            params = {"city": madde["city"], "office": madde["office"], "type": madde["type"]}
            response = requests.get(url, params=params, headers=headers, timeout=10)
            res_text = response.text.lower()
            
            bulundu_mu = any(x in res_text for x in ["müsait", "available", "seçiniz", "2026"])
            
            sonuclar.append({
                "kimlik": f"{madde['ulke']}-{madde['ad']}",
                "ulke": madde["ulke"],
                "ofis": madde["ad"],
                "durum": "✅ RANDEVU VAR!" if bulundu_mu else "❌ Randevu Yok",
                "aktif": "aktif" if bulundu_mu else "pasif"
            })
        except:
            sonuclar.append({
                "kimlik": f"{madde['ulke']}-{madde['ad']}",
                "ulke": madde["ulke"],
                "ofis": madde["ad"],
                "durum": "⚠️ Bağlantı Hatası",
                "aktif": "pasif"
            })

    data = {"son_kontrol": su_an, "liste": sonuclar}
    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    check_idata()
