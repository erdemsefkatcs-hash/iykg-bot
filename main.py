import requests, time, json
from datetime import datetime

BASE = "https://f20.macsonuclari1.net/iddaa26.asp"
ORAN = "https://f20cdn.macsonuclari1.net/oranlar26.asp"

TELEGRAM_TOKEN = "8969091855:AAHYl1phtQkwQxyGyuxIsjo2iovUwPkXQPw"
CHAT_ID = "6131905264"

# Market ID haritası
MID = {
    "MS": 1, "IY": 5, "KG": 8,
    "AU15": 38, "AU25": 34, "AU35": 39,
    "IY15": 9, "IY25": 28,
    "TEKCIFTE": 36,
    "IY_CIFTE": 13,
    "2Y": 32,
    "HANGI_YARI": 22,
    "KORNER95": 47,
    "DEP_AU15": 15,
}

def get_oran(data, mId, moId):
    if not data or not isinstance(data, list):
        return None
    for x in data:
        if x.get("mId") == mId and x.get("moId") == moId:
            return x.get("o")
    return None

def get_oranlar(mid):
    try:
        r = requests.get(ORAN, params={"id": mid}, timeout=10)
        return r.json().get("data") or []
    except:
        return []

def skor_analiz(mac):
    u = mac.get("u") or {}
    s = u.get("s", "0")
    iy = u.get("iy", "")
    evs = u.get("evs", "0")
    deps = u.get("deps", "0")
    return s, iy, evs, deps

def puan(o):
    """Oranı ver, bu oranda kaç puan (sinyal gücü)"""
    if o is None:
        return 0, ""
    # Her market için eşik kontrolleri
    return o

def sinyal_kontrol(oranlar, hl):
    """Tüm kurallara göre puanlama yap"""
    sinyaller = []
    puan = 0

    # 1. KG Var: 1.09-1.35 arası ✅
    kg_var = get_oran(oranlar, 8, 13)
    if kg_var:
        if 1.09 <= kg_var <= 1.35:
            sinyaller.append(f"✅ KG Var: {kg_var}")
            puan += 3
        elif 1.35 < kg_var <= 1.42:
            sinyaller.append(f"⚠️ KG Var: {kg_var} (sınırda)")
            puan += 1
        elif kg_var >= 1.42:
            sinyaller.append(f"❌ KG Var: {kg_var} (yüksek)")
            puan -= 2

    # 2. IY X: 2.00-2.40 ✅
    iy_x = get_oran(oranlar, 5, 21)
    if iy_x:
        if 2.00 <= iy_x <= 2.40:
            sinyaller.append(f"✅ IY X: {iy_x}")
            puan += 2
        elif iy_x < 1.90:
            sinyaller.append(f"❌ IY X: {iy_x} (düşük)")
            puan -= 1

    # 3. AltUst 3.5 Üst: 1.39-1.74 ✅
    au35_ust = get_oran(oranlar, 39, 289)  # moId 289 = 3.5 üst
    if au35_ust is None:
        # alternatif moId dene
        for item in (oranlar or []):
            if item.get("mId") == 39 and item.get("o") and 1.30 <= float(item.get("o",0)) <= 2.00:
                au35_ust = item.get("o")
                break
    if au35_ust:
        if 1.39 <= au35_ust <= 1.74:
            sinyaller.append(f"✅ AU3.5Üst: {au35_ust}")
            puan += 3
        elif au35_ust < 1.39:
            sinyaller.append(f"⚠️ AU3.5Üst: {au35_ust} (çok düşük)")

    # 4. IY AltUst 1.5 Üst: 1.31-1.74 ✅
    iy15_ust = get_oran(oranlar, 9, 29)  # moId 29 = IY 1.5 üst
    if iy15_ust:
        if 1.31 <= iy15_ust <= 1.74:
            sinyaller.append(f"✅ IY1.5Üst: {iy15_ust}")
            puan += 2
        elif iy15_ust <= 1.22:
            sinyaller.append(f"❌ IY1.5Üst: {iy15_ust} (düşük)")
            puan -= 1

    # 5. IY Cifte Sans: 1.17-1.30 ✅
    iy_cs = None
    for item in (oranlar or []):
        if item.get("mId") == 13 and item.get("o"):
            o = float(item.get("o", 0))
            if 1.05 <= o <= 1.60:
                iy_cs = o
                break
    if iy_cs:
        if 1.17 <= iy_cs <= 1.30:
            sinyaller.append(f"✅ IY ÇŞ: {iy_cs}")
            puan += 2
        elif iy_cs >= 1.43:
            sinyaller.append(f"❌ IY ÇŞ: {iy_cs} (yüksek)")
            puan -= 1

    # 6. Tek/Cift: 1.57-1.66 ✅
    tekcifte = None
    for item in (oranlar or []):
        if item.get("mId") == 36 and item.get("o"):
            o = float(item.get("o", 0))
            if 1.50 <= o <= 1.80:
                tekcifte = o
                break
    if tekcifte:
        if 1.57 <= tekcifte <= 1.66:
            sinyaller.append(f"✅ Tek/Çift: {tekcifte}")
            puan += 2
        elif tekcifte <= 1.51 or tekcifte >= 1.68:
            sinyaller.append(f"❌ Tek/Çift: {tekcifte}")
            puan -= 1

    # 7. MS X oranı (hl'den)
    ms_x = get_oran(hl, 1, 1)
    if ms_x:
        if ms_x >= 2.90:
            sinyaller.append(f"✅ MS X: {ms_x}")
            puan += 1

    # 8. Korner 9.5 Üst: ~1.62 ✅
    k95 = None
    for item in (oranlar or []):
        if item.get("mId") == 47 and item.get("o"):
            k95 = float(item.get("o"))
            break
    if k95 and 1.55 <= k95 <= 1.70:
        sinyaller.append(f"✅ Korner9.5: {k95}")
        puan += 1

    return puan, sinyaller

def send_telegram(text):
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
        return r.ok
    except:
        return False

def main():
    print(f"[{datetime.now().strftime('%H:%M')}] Bugünün maçları taranıyor...")

    r = requests.get(BASE, params={"sports": 78, "order": "tarih"}, timeout=15)
    data = r.json()
    maclar = data.get("m") or []
    ligler = data.get("l") or {}

    print(f"Toplam maç: {len(maclar)}")

    sonuclar = []

    for m in maclar:
        u = m.get("u") or {}
        # Sadece başlamamış maçlar
        if u.get("s") != "0":
            continue

        mid = m.get("id")
        if not mid:
            continue

        ev = m.get("h", "?")
        dep = m.get("a", "?")
        t = m.get("t", 0)
        saat = datetime.fromtimestamp(t).strftime("%H:%M") if t else "--:--"
        hl = m.get("hl") or []

        lid = m.get("l")
        lig = (ligler.get(str(lid)) or ligler.get(lid) or {}).get("n", "?")

        # Detay oranları çek
        oranlar = get_oranlar(mid)
        time.sleep(0.2)

        # Sinyal kontrolü
        puan_val, sinyaller = sinyal_kontrol(oranlar, hl)

        if puan_val >= 4:  # En az 4 puan
            sonuclar.append({
                "saat": saat,
                "ev": ev,
                "dep": dep,
                "lig": lig,
                "puan": puan_val,
                "sinyaller": sinyaller,
            })
            print(f"  ✅ {saat} {ev} vs {dep} | Puan:{puan_val}")

    print(f"\nToplam uygun maç: {len(sonuclar)}")

    if not sonuclar:
        msg = "🔍 Bugün IYKG filtrelerine uygun maç bulunamadı."
        print(msg)
        send_telegram(msg)
        return

    # Telegram mesajı
    sonuclar.sort(key=lambda x: (-x["puan"], x["saat"]))
    msg = f"⚽ <b>IYKG FİLTRE — {datetime.today().strftime('%d.%m.%Y')}</b>\n"
    msg += f"✅ {len(sonuclar)} maç bulundu\n\n"

    for s in sonuclar:
        msg += f"⏰ <b>{s['saat']}</b> | Puan: <b>{s['puan']}</b>\n"
        msg += f"🏟 {s['ev']} vs {s['dep']}\n"
        msg += f"🏆 {s['lig']}\n"
        for sin in s['sinyaller']:
            msg += f"  {sin}\n"
        msg += "\n"

    msg += "─────────────\n🤖 IYKG Bot"

    print("\n" + msg)
    send_telegram(msg)
    print("\nTelegram'a gönderildi!")

if __name__ == "__main__":
    main()
