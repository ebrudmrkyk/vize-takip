import requests
import json
from datetime import datetime

def kontrol():
    # iDATA Almanya Sorgu Taklidi
    url = "https://idata.com.tr/vi/control/check-appointment-status"
    print("Almanya randevuları taranıyor...")
    
    su_an = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Şimdilik simülasyon yapıyoruz, gerçek iDATA verisi gelmiş gibi davranalım
    # Eğer randevu bulursak 'durum' kısmını değiştireceğiz
    veriler = {
        "ulke": "Almanya",
        "tarih": "Şu an randevu yok",
        "son_kontrol": su_an,
        "durum": "pasif" 
    }
    
    # Bu veriyi bir dosyaya kaydediyoruz
    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump(veriler, f, ensure_ascii=False, indent=4)
    
    print(f"Sonuç kaydedildi: {su_an}")

if __name__ == "__main__":
    kontrol()
