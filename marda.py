import requests
from datetime import datetime, timedelta
import uuid

min_lat = 39.0
max_lat = 42.5
min_lon = 26.0
max_lon = 30.8

SUPABASE_URL = "https://sqptktnuvccatyoueoma.supabase.co"
SUPABASE_API_KEY = "SUPABASE_API_KEY_GITHUB_SECRETS_ILE_GELECEK"
TABLE_NAME = "earthquakes"

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=ignore-duplicates"
}

def afad_son_depremleri_cek():
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=1)
    url = (
        "https://deprem.afad.gov.tr/apiv2/event/filter"
        f"?start={start_date.strftime('%Y-%m-%dT%H:%M:%S')}"
        f"&end={end_date.strftime('%Y-%m-%dT%H:%M:%S')}"
        f"&minlat={min_lat}&maxlat={max_lat}&minlon={min_lon}&maxlon={max_lon}"
        "&orderby=timedesc"
    )
    response = requests.get(url)
    data = response.json()
    depremler = []
    for event in data:
        try:
            tarih_saat = datetime.fromisoformat(event["date"])
            latitude = float(event["latitude"])
            longitude = float(event["longitude"])
            depth = float(event["depth"]) if event["depth"] else None
            magnitude = float(event["magnitude"])
            location = event["location"]

            depremler.append({
                "id": str(uuid.uuid4()),
                "occurred_at": tarih_saat.isoformat(),
                "latitude": latitude,
                "longitude": longitude,
                "depth": depth,
                "magnitude": magnitude,
                "location": location
            })
        except Exception as e:
            print(f"Hata: {e} - Veri: {event}")
    return depremler

def supabase_ekle(deprem_liste):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
    for deprem in deprem_liste:
        response = requests.post(url, json=deprem, headers=headers)
        if response.status_code not in [201, 409]:
            print("❌ Hata:", response.status_code, response.text)
        else:
            print(f"✅ Eklendi: {deprem['occurred_at']} - {deprem['location']}")

# Çalıştır
depremler = afad_son_depremleri_cek()
supabase_ekle(depremler)
