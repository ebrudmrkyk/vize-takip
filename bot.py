import requests
import os

def kontrol():
    # iDATA Almanya Sorgu Parametreleri
    url = "https://idata.com.tr/vi/control/check-appointment-status"
    print("Almanya randevuları taranıyor...")
    
    # Not: iDATA gerçek hayatta bazen 'token' isteyebilir. 
    # Şimdilik sistemin GitHub üzerinde çalıştığını test ediyoruz.
    try:
        r = requests.get(url)
        print("Sistemden yanıt alındı. Durum: Müsait randevu yok (Simülasyon)")
    except:
        print("Siteye şu an ulaşılamıyor.")

if __name__ == "__main__":
    kontrol()
