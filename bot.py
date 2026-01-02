import requests
import json
from datetime import datetime, timedelta

# --- AYARLAR ---
# Senin verdiğin tokenı buraya ekledim
EXPO_PUSH_TOKEN = "ExponentPushToken[BeKUMCJEQBR7tm0J_v2JvE]"

def send_push_notification(title, body):
    """Expo üzerinden telefona anlık bildirim gönderir."""
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
        print(f"Bildirim durumu: {response.status_code} - Yanıt: {response.text}")
    except Exception as e:
        print(f"Bildirim hatası: {e}")

def check_appointments():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }

    # TÜRKİYE SAATİ (UTC+3)
    tr_saati = datetime.utcnow() + timedelta(hours=3)
    su_an = tr_saati.strftime("%d/%m/%Y %H:%M")

    # SORGULANACAK LİSTE
    sorgu_listesi = [
        {"ulke": "Macaristan", "ad": "Ankara", "type": "vfs", "url": "https://visa.vfsglobal.com/tur/tr/hun/interim"},
        {"ulke": "Danimarka", "ad": "Ankara", "type": "vfs", "url": "https://visa.vfsglobal.com/tur/tr/dnk/interim"},
        {"ulke": "Almanya", "ad": "Ankara", "type": "idata", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "2", "office": "3", "type": "1"}},
        {"ulke": "İtalya", "ad": "Ankara", "type": "idata", "url": "https://idata.com.tr/vi/control/check-appointment-status", "params": {"city": "2", "office": "3", "type": "2"}},
        {"ulke": "İspanya", "ad": "Ankara", "type": "bls", "url": "https://turkey.blsspainvisa.com/ankara/index.php"},
        {"ulke": "Fransa", "ad": "İstanbul", "type": "vfs", "url": "https://visa.vfsglobal.com/tur/tr/fra/interim"}
    ]
    
    sonuclar = []

    for madde in sorgu_listesi:
        try:
            bulundu_mu = False
            
            # VFS, BLS ve iDATA Kontrolleri
            if madde["type"] == "vfs":
                response = requests.get(madde["url"], headers=headers, timeout=25)
                bulundu_mu = any(x in response.text.lower() for x in ["available", "tarih seç", "randevu al"]) and "no slots" not in response.text.lower()
            elif madde["type"] == "bls":
                response = requests.get(madde["url"], headers=headers, timeout=20)
                bulundu_mu = "available" in response.text.lower()
            else:
                response = requests.get(madde["url"], params=madde["params"], headers=headers, timeout=15)
                bulundu_mu = any(x in response.text.lower() for x in ["müsait", "available", "2026"])

            # --- TEST MODU AKTİF ---
            # Macaristan'ı her zaman randevu varmış gibi gösterip bildirim gönderiyoruz
            if madde["ulke"] == "Macaristan":
                bulundu_mu = True 

            if bulundu_mu:
                send_push_notification(
                    f"🚨 RANDEVU BULDUM: {madde['ulke']}",
                    f"{madde['ad']} ofisinde randevu uygun! Saat: {su_an}"
                )
            
            sonuclar.append({
                "kimlik": f"{madde['ulke']}-{madde['ad']}",
                "ulke": madde["ulke"],
                "ofis": madde["ad"],
                "durum": "✅ RANDEVU VAR!" if bulundu_mu else "❌ Randevu Yok",
                "aktif": "aktif" if bulundu_mu else "pasif"
            })
            
        except Exception as e:
            sonuclar.append({"kimlik": f"{madde['ulke']}-{madde['ad']}", "ulke": madde["ulke"], "ofis": madde["ad"], "durum": "⚠️ Hata", "aktif": "pasif"})

    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump({"son_kontrol": su_an, "liste": sonuclar}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    check_appointments()
