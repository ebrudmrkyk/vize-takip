import requests
import json
from datetime import datetime, timedelta

# --- AYARLAR ---
# Uygulamayı açtığında ekranda görünen veya console'da yazan tokenı buraya yapıştır
EXPO_PUSH_TOKEN = "BeKUMCJEQBR7tm0J_v2JvE"

def send_push_notification(title, body):
    """Expo sunucuları üzerinden telefona bildirim gönderir."""
    if "ExponentPushToken" not in EXPO_PUSH_TOKEN:
        print("HATA: Geçerli bir Expo Push Token ayarlanmamış!")
        return

    url = "https://exp.host/--/api/v2/push/send"
    payload = {
        "to": EXPO_PUSH_TOKEN,
        "title": title,
        "body": body,
        "sound": "default",
        "priority": "high"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Bildirim Gönderim Durumu: {response.status_code}")
    except Exception as e:
        print(f"Bildirim gönderilirken hata oluştu: {e}")

def check_appointments():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }

    # TÜRKİYE SAATİ (UTC+3)
    tr_saati = datetime.utcnow() + timedelta(hours=3)
    su_an = tr_saati.strftime("%d/%m/%Y %H:%M")

    # SORGULANACAK LİSTE (ANKARA ÖNCELİKLİ)
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
            bulundu_mu = False
            
            # VFS Global Kontrolü
            if madde["type"] == "vfs":
                response = requests.get(madde["url"], headers=headers, timeout=25)
                res_text = response.text.lower()
                bulundu_mu = any(x in res_text for x in ["available", "tarih seç", "randevu al"]) and "no slots" not in res_text
            
            # BLS İspanya Kontrolü
            elif madde["type"] == "bls":
                response = requests.get(madde["url"], headers=headers, timeout=20)
                bulundu_mu = any(x in response.text.lower() for x in ["available", "randevu uygun", "booking"])
            
            # iDATA (Almanya/İtalya) Kontrolü
            else: 
                response = requests.get(madde["url"], params=madde["params"], headers=headers, timeout=15)
                bulundu_mu = any(x in response.text.lower() for x in ["müsait", "available", "2026"])
            
            # --- BİLDİRİM TETİKLEME ---
            if bulundu_mu:
                send_push_notification(
                    f"🚨 RANDEVU BULDUM: {madde['ulke']}",
                    f"{madde['ad']} ofisinde randevu uygun görünüyor! Saat: {su_an}"
                )
            
            sonuclar.append({
                "kimlik": f"{madde['ulke']}-{madde['ad']}",
                "ulke": madde["ulke"],
                "ofis": madde["ad"],
                "durum": "✅ RANDEVU VAR!" if bulundu_mu else "❌ Randevu Yok",
                "aktif": "aktif" if bulundu_mu else "pasif"
            })
            
        except Exception as e:
            print(f"Hata oluştu ({madde['ulke']}-{madde['ad']}): {e}")
            sonuclar.append({
                "kimlik": f"{madde['ulke']}-{madde['ad']}",
                "ulke": madde["ulke"],
                "ofis": madde["ad"],
                "durum": "⚠️ Hata",
                "aktif": "pasif"
            })

    # Veriyi JSON olarak kaydet
    data = {"son_kontrol": su_an, "liste": sonuclar}
    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    check_appointments()
