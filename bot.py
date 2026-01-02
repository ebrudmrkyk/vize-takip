import requests
import json
from datetime import datetime

def check_idata():
    # iDATA'nın gerçek sorgu adresi
    url = "https://idata.com.tr/vi/control/check-appointment-status"
    
    # Gerçek bir tarayıcı gibi görünmek için gerekli başlıklar
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"
    }

    ofisler = [
        {"id": "1", "ad": "İstanbul (Gayrettepe)", "city": "1", "office": "1"},
        {"id": "2", "ad": "İstanbul (Altunizade)", "city": "1", "office": "2"},
        {"id": "3", "ad": "Ankara", "city": "2", "office": "3"},
        {"id": "4", "ad": "İzmir", "city": "3", "office": "4"},
        {"id": "6", "ad": "Antalya", "city": "4", "office": "6"}
    ]
    
    sonuclar = []
    su_an = datetime.now().strftime("%d/%m/%Y %H:%M")

    for ofis in ofisler:
        try:
            # Burası iDATA'ya gerçek sorguyu attığımız yer
            params = {
                "city": ofis["city"],
                "office": ofis["office"],
                "type": "1" # 1 genellikle standart vizedir
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            # iDATA genellikle "no_appointment" veya benzeri bir JSON cevabı döner
            # Cevapta "available" veya tarih varsa 'aktif' diyeceğiz
            res_data = response.text.lower()
            
            bulundu_mu = "müsait" in res_data or "available" in res_data
            
            sonuclar.append({
                "ofis": ofis["ad"],
                "durum": "RANDEVU VAR!" if bulundu_mu else "Randevu Yok",
                "aktif": "aktif" if bulundu_mu else "pasif"
            })
            
        except Exception as e:
            sonuclar.append({
                "ofis": ofis["ad"],
                "durum": "Sistem Hatası",
                "aktif": "pasif"
            })

    data = {"son_kontrol": su_an, "liste": sonuclar}
    
    with open("sonuc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    check_idata()
