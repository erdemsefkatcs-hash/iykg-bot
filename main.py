import requests, time, json
from datetime import datetime

BASE  = "https://f20.macsonuclari1.net/iddaa26.asp"
ORAN  = "https://f20cdn.macsonuclari1.net/oranlar26.asp"
TOKEN = "8969091855:AAHYl1phtQkwQxyGyuxIsjo2iovUwPkXQPw"
CHAT  = "6131905264"

def get_oranlar(mid):
    try:
        r = requests.get(ORAN, params={"id": mid}, timeout=10)
        return r.json().get("data") or []
    except: return []

def gv(o, mId):
    for x in o:
        if x.get("mId") == mId:
            try: return round(float(x.get("o")), 2)
            except: pass
    return None

def gvmo(o, mId, moId):
    for x in o:
        if x.get("mId") == mId and x.get("moId") == moId:
            try: return round(float(x.get("o")), 2)
            except: pass
    return None

def send(text):
    try:
        requests.post(
            "https://api.telegram.org/bot" + TOKEN + "/sendMessage",
            json={"chat_id": CHAT, "text": text}, timeout=10)
    except: pass

# ================================================================
# IYKG FİLTRESİ
# 36,077 maç analizinden: IYKG genel %5.3
# Hedef: %10+ ihtimal (2x artış)
# ================================================================
def filtre_iykg(o):
    p = 0
    s = []

    # KG düşükse IYKG çok artıyor
    kg = gv(o, 8)
    if kg:
        if 1.05 <= kg <= 1.10:   p += 5; s.append("KG={} %14.75".format(kg))
        elif 1.10 <= kg <= 1.15: p += 4; s.append("KG={} %12.81".format(kg))
        elif 1.15 <= kg <= 1.20: p += 4; s.append("KG={} %11.32".format(kg))
        elif 1.20 <= kg <= 1.25: p += 3; s.append("KG={} %10.77".format(kg))
        elif 1.25 <= kg <= 1.30: p += 3; s.append("KG={} %9.44".format(kg))

    # AltUst_3.5 düşükse IYKG artıyor
    au35 = gv(o, 39)
    if au35:
        if 1.65 <= au35 <= 1.70: p += 5; s.append("AU35={} %13.11".format(au35))
        elif 1.90 <= au35 <= 2.00: p += 5; s.append("AU35={} %11.90".format(au35))
        elif 1.55 <= au35 <= 1.65: p += 4; s.append("AU35={} %10.17".format(au35))
        elif 1.70 <= au35 <= 1.75: p += 4; s.append("AU35={} %8.74".format(au35))

    # IY_AltUst_1.5 yüksekse IYKG artıyor
    iy15 = gv(o, 9)
    if iy15:
        if 1.90 <= iy15 <= 1.95: p += 5; s.append("IY15={} %15.38".format(iy15))
        elif 2.00 <= iy15 <= 2.10: p += 5; s.append("IY15={} %13.33".format(iy15))
        elif 2.10 <= iy15 <= 2.15: p += 4; s.append("IY15={} %13.95".format(iy15))
        elif 1.80 <= iy15 <= 1.90: p += 3; s.append("IY15={} %9.23".format(iy15))

    # Korner_9.5 2.05-2.10 → IYKG %14.74
    k95 = gv(o, 47)
    if k95 and 2.05 <= k95 <= 2.10:
        p += 4; s.append("K9.5={} %14.74".format(k95))

    # IY_AltUst_0.5 yüksekse (3.30+)
    iy05 = gv(o, 37)
    if iy05:
        if 3.30 <= iy05 <= 3.35: p += 4; s.append("IY05={} %21.62".format(iy05))
        elif 3.45 <= iy05 <= 3.50: p += 4; s.append("IY05={} %19.05".format(iy05))
        elif 3.00 <= iy05 <= 3.05: p += 3; s.append("IY05={} %15.56".format(iy05))

    # Dep_AltUst_1.5 yüksekse IYKG artıyor
    dep15 = gv(o, 15)
    if dep15:
        if 1.90 <= dep15 <= 1.95: p += 4; s.append("Dep15={} %11.00".format(dep15))
        elif 2.15 <= dep15 <= 2.20: p += 4; s.append("Dep15={} %11.32".format(dep15))
        elif 2.20 <= dep15 <= 2.25: p += 3; s.append("Dep15={} %12.28".format(dep15))

    # MS yüksekse (3.25+) IYKG artıyor
    ms_ev = gvmo(o, 1, 2)
    if ms_ev:
        if 3.25 <= ms_ev <= 3.30: p += 3; s.append("MS_EV={} %14.29".format(ms_ev))
        elif 3.50 <= ms_ev <= 3.60: p += 4; s.append("MS_EV={} %20.00".format(ms_ev))

    # IKILI KOMBO BONUSLARI (analizden çıkan güçlü çiftler)
    if iy15 and au35 and 1.90 <= iy15 <= 1.95 and 1.95 <= au35 <= 2.00:
        p += 6; s.append("KOMBO IY15+AU35 %35.29!")
    if kg and au35 and 1.05 <= kg <= 1.10 and 1.90 <= au35 <= 1.95:
        p += 5; s.append("KOMBO KG+AU35 %27.27!")
    if kg and dep15 and 1.15 <= kg <= 1.20 and 1.90 <= dep15 <= 1.95:
        p += 5; s.append("KOMBO KG+Dep15 %26.32!")

    return p, s

# ================================================================
# 2/1 FİLTRESİ
# 36,077 maç analizinden: 2/1 genel %2.64
# Hedef: %7+ ihtimal (2.5x artış)
# ================================================================
def filtre_21(o):
    p = 0
    s = []

    # AltUst_2.5 = 2.75-2.80 → %14.04 EN GÜÇLÜ
    au25 = gv(o, 34)
    if au25:
        if 2.75 <= au25 <= 2.80: p += 7; s.append("AU25={} %14.04 ALTIN".format(au25))
        elif 2.55 <= au25 <= 2.65: p += 5; s.append("AU25={} %14-18%".format(au25))
        elif 2.60 <= au25 <= 2.70: p += 4; s.append("AU25={} %6.17".format(au25))

    # IY_Sonucu = 2.64 → %10.20 (98 maç, EN GÜVENİLİR)
    iysn = gv(o, 5)
    if iysn:
        if 2.60 <= iysn <= 2.70: p += 5; s.append("IY_X={} %10.20".format(iysn))
        elif 3.30 <= iysn <= 3.40: p += 4; s.append("IY_X={} %9.76".format(iysn))
        elif 3.60 <= iysn <= 3.80: p += 4; s.append("IY_X={} %8.82".format(iysn))
        elif 1.26 <= iysn <= 1.35: p += 4; s.append("IY_X={} %10.53".format(iysn))
        elif 1.60 <= iysn <= 1.65: p += 4; s.append("IY_X={} %7.75".format(iysn))
        elif 1.88 <= iysn <= 1.95: p += 3; s.append("IY_X={} %7.62".format(iysn))

    # KG = 1.14 → %11.86 (59 maç)
    kg = gv(o, 8)
    if kg:
        if kg == 1.14: p += 5; s.append("KG=1.14 %11.86")
        elif 1.10 <= kg <= 1.17: p += 3; s.append("KG={} ~%9".format(kg))

    # Ev_AltUst_1.5 = 2.30-2.35 → %9.52
    ev15 = gv(o, 18)
    if ev15:
        if 2.30 <= ev15 <= 2.35: p += 5; s.append("Ev15={} %9.52".format(ev15))
        elif 2.95 <= ev15 <= 3.00: p += 4; s.append("Ev15={} %9.52".format(ev15))
        elif 2.55 <= ev15 <= 2.60: p += 4; s.append("Ev15={} %8.00".format(ev15))
        elif 2.00 <= ev15 <= 2.15: p += 3; s.append("Ev15={} %7.65".format(ev15))

    # IY_AltUst_0.5 = 2.54 → %10.00 (80 maç)
    iy05 = gv(o, 37)
    if iy05:
        if 2.50 <= iy05 <= 2.60: p += 4; s.append("IY05={} %10.00".format(iy05))
        elif 4.25 <= iy05 <= 4.30: p += 4; s.append("IY05={} %12.50".format(iy05))
        elif 2.99 <= iy05 <= 3.05: p += 3; s.append("IY05={} %9.09".format(iy05))

    # IY_AltUst_1.5 = 1.82-1.86 → %11.76
    iy15 = gv(o, 9)
    if iy15:
        if 1.80 <= iy15 <= 1.87: p += 4; s.append("IY15={} %11.76".format(iy15))
        elif 1.90 <= iy15 <= 1.95: p += 3; s.append("IY15={} %10.00".format(iy15))

    # 2Y_Sonucu = 1.23 → %11.11 (27 maç)
    y2 = gv(o, 32)
    if y2:
        if 1.20 <= y2 <= 1.25: p += 5; s.append("2Y={} %11.11".format(y2))
        elif 1.50 <= y2 <= 1.55: p += 4; s.append("2Y={} %7.34".format(y2))
        elif 1.80 <= y2 <= 1.85: p += 3; s.append("2Y={} %5.97".format(y2))

    # MS_EV = 4.62 → %10.71
    ms_ev = gvmo(o, 1, 2)
    if ms_ev:
        if 4.55 <= ms_ev <= 4.70: p += 4; s.append("MS_EV={} %10.71".format(ms_ev))
        elif 3.50 <= ms_ev <= 3.55: p += 3; s.append("MS_EV={} %9.09".format(ms_ev))
        elif 3.85 <= ms_ev <= 3.95: p += 3; s.append("MS_EV={} %8.70".format(ms_ev))

    # Korner_9.5 = 2.04 → %9.80
    k95 = gv(o, 47)
    if k95:
        if 2.00 <= k95 <= 2.08: p += 3; s.append("K9.5={} %9.80".format(k95))
        elif 1.65 <= k95 <= 1.70: p += 3; s.append("K9.5={} %8.16".format(k95))

    # NEGATIF SINYALLER (2/1 olma ihtimali düşüyor)
    iycs = gv(o, 13)
    if iycs and iycs >= 1.40: p -= 3; s.append("ENGEL IYCS={} (2/1 az)".format(iycs))
    if iysn and iysn >= 5.50: p -= 3; s.append("ENGEL IY_X={} (2/1 sifir)".format(iysn))

    return p, s

# ================================================================
# 1/2 FİLTRESİ
# 36,077 maç analizinden: 1/2 genel %2.13
# Hedef: %5+ ihtimal (2.5x artış)
# ================================================================
def filtre_12(o):
    p = 0
    s = []

    # Dep_AltUst_1.5 = 1.70-1.75 → %5.52 (453 maç EN GÜVENİLİR)
    dep15 = gv(o, 15)
    if dep15:
        if 1.70 <= dep15 <= 1.75: p += 5; s.append("Dep15={} %5.52 453mac".format(dep15))
        elif 2.10 <= dep15 <= 2.15: p += 5; s.append("Dep15={} %6.45".format(dep15))
        elif 2.45 <= dep15 <= 2.50: p += 5; s.append("Dep15={} %11.54".format(dep15))
        elif 1.60 <= dep15 <= 1.70: p += 4; s.append("Dep15={} %4.41".format(dep15))
        elif 2.25 <= dep15 <= 2.30: p += 4; s.append("Dep15={} %6.90".format(dep15))
        elif 2.00 <= dep15 <= 2.10: p += 3; s.append("Dep15={} %7.14".format(dep15))

    # MS_DEP yüksek → dep favori değil ama 1/2 olasılığı artıyor
    ms_dep = gvmo(o, 1, 3)
    if ms_dep:
        if 4.90 <= ms_dep <= 4.95: p += 6; s.append("MS_DEP={} %13.51".format(ms_dep))
        elif 5.45 <= ms_dep <= 5.50: p += 6; s.append("MS_DEP={} %12.50".format(ms_dep))
        elif 3.80 <= ms_dep <= 3.85: p += 4; s.append("MS_DEP={} %6.94".format(ms_dep))
        elif 3.50 <= ms_dep <= 3.55: p += 4; s.append("MS_DEP={} %6.72".format(ms_dep))
        elif 2.70 <= ms_dep <= 2.80: p += 4; s.append("MS_DEP={} %4.57".format(ms_dep))
        elif 2.45 <= ms_dep <= 2.50: p += 3; s.append("MS_DEP={} %8.00".format(ms_dep))

    # IY_AltUst_1.5 = 1.78 → %13.16
    iy15 = gv(o, 9)
    if iy15:
        if 1.78 <= iy15 <= 1.82: p += 6; s.append("IY15={} %13.16".format(iy15))
        elif 1.93 <= iy15 <= 1.95: p += 4; s.append("IY15={} %10.53".format(iy15))
        elif 1.70 <= iy15 <= 1.78: p += 3; s.append("IY15={} %3.72".format(iy15))

    # IY_Cifte_Sans = 1.55 → %12.90
    iycs = gv(o, 13)
    if iycs:
        if 1.55 <= iycs <= 1.58: p += 6; s.append("IYCS={} %12.90".format(iycs))
        elif 1.61 <= iycs <= 1.70: p += 5; s.append("IYCS={} %9.52".format(iycs))
        elif 1.48 <= iycs <= 1.55: p += 4; s.append("IYCS={} %8.57".format(iycs))
        elif 1.40 <= iycs <= 1.48: p += 3; s.append("IYCS={} %7.04".format(iycs))

    # 2Y_Sonucu = 4.28 → %15.00 EN GÜÇLÜ
    y2 = gv(o, 32)
    if y2:
        if 4.25 <= y2 <= 4.30: p += 7; s.append("2Y={} %15.00 ALTIN".format(y2))
        elif 3.85 <= y2 <= 3.95: p += 5; s.append("2Y={} %13.33".format(y2))
        elif 3.10 <= y2 <= 3.20: p += 4; s.append("2Y={} %9.76".format(y2))
        elif 3.30 <= y2 <= 3.45: p += 4; s.append("2Y={} %9.09".format(y2))
        elif 2.85 <= y2 <= 2.95: p += 3; s.append("2Y={} %3.89".format(y2))

    # IY_Sonucu yüksekse (4.10+) 1/2 artıyor
    iysn = gv(o, 5)
    if iysn:
        if 4.10 <= iysn <= 4.15: p += 4; s.append("IY_X={} %12.50".format(iysn))
        elif 4.40 <= iysn <= 4.45: p += 4; s.append("IY_X={} %12.00".format(iysn))
        elif 5.35 <= iysn <= 5.40: p += 4; s.append("IY_X={} %10.00".format(iysn))
        elif 3.80 <= iysn <= 3.90: p += 3; s.append("IY_X={} %8.77".format(iysn))

    # IY_AltUst_0.5 = 4.10-4.15 → %13.64
    iy05 = gv(o, 37)
    if iy05:
        if 4.10 <= iy05 <= 4.15: p += 5; s.append("IY05={} %13.64".format(iy05))
        elif 3.60 <= iy05 <= 3.65: p += 4; s.append("IY05={} %12.50".format(iy05))
        elif 3.40 <= iy05 <= 3.45: p += 3; s.append("IY05={} %10.53".format(iy05))

    # KG = 1.05 → %11.76
    kg = gv(o, 8)
    if kg:
        if 1.05 <= kg <= 1.07: p += 4; s.append("KG={} %11.76".format(kg))
        elif 1.20 <= kg <= 1.25: p += 3; s.append("KG={} %4.97".format(kg))

    # HYG = 3.15-3.20 → %8.00
    hyg = gv(o, 22)
    if hyg and 3.15 <= hyg <= 3.20:
        p += 3; s.append("HYG={} %8.00".format(hyg))

    # NEGATIF - IY_Sonucu düşükse (1.10-1.20) 1/2 OLMAZ
    if iysn and 1.10 <= iysn <= 1.20: p -= 4; s.append("ENGEL IY_X={} (1/2 sifir)".format(iysn))

    return p, s

# ================================================================
# ANA PROGRAM
# ================================================================
def main():
    print(datetime.now().strftime("[%H:%M] %d.%m.%Y") + " Taranıyor...")

    r = requests.get(BASE, params={"sports": 78, "order": "tarih"}, timeout=15)
    d = r.json()
    maclar = d.get("m") or []
    ligler = d.get("l") or {}
    print("Toplam: " + str(len(maclar)) + " maç")

    iykg_list, list_21, list_12 = [], [], []

    for m in maclar:
        u = m.get("u") or {}
        if u.get("s") != "0": continue
        mid = m.get("id")
        if not mid: continue

        ev   = m.get("h", "?")
        dep  = m.get("a", "?")
        t    = m.get("t", 0)
        saat = datetime.fromtimestamp(t).strftime("%H:%M") if t else "--:--"
        lid  = m.get("l")
        lig  = (ligler.get(str(lid)) or ligler.get(lid) or {}).get("n", "?")

        o = get_oranlar(mid)
        time.sleep(0.18)

        pi, si = filtre_iykg(o)
        p2, s2 = filtre_21(o)
        p1, s1 = filtre_12(o)

        info = {"saat": saat, "ev": ev, "dep": dep, "lig": lig}
        if pi >= 10: iykg_list.append({**info, "puan": pi, "s": si})
        if p2 >= 10: list_21.append({**info, "puan": p2, "s": s2})
        if p1 >= 10: list_12.append({**info, "puan": p1, "s": s1})

    tarih = datetime.today().strftime("%d.%m.%Y")

    # Ekran çıktısı
    print("\n" + "="*60)
    for baslik, liste in [("IYKG", iykg_list), ("2/1", list_21), ("1/2", list_12)]:
        sirali = sorted(liste, key=lambda x: -x["puan"])
        print("\n=== " + baslik + " (" + str(len(sirali)) + " maç) ===")
        for e in sirali[:20]:
            print("  " + e["saat"] + " " + e["ev"] + " vs " + e["dep"] + " | P:" + str(e["puan"]))
            print("  " + " | ".join(e["s"][:4]))

    # Telegram
    for baslik, liste in [
        ("IYKG",                     iykg_list),
        ("2/1 (Dep 1Y => Ev kazanır)", list_21),
        ("1/2 (Ev 1Y => Dep kazanır)", list_12)
    ]:
        if not liste: continue
        sirali = sorted(liste, key=lambda x: -x["puan"])
        msg = "=== " + baslik + " " + tarih + " ===\n" + str(len(sirali)) + " maç\n\n"
        for e in sirali[:15]:
            msg += e["saat"] + " P:" + str(e["puan"]) + "\n"
            msg += e["ev"] + " vs " + e["dep"] + "\n"
            msg += e["lig"] + "\n"
            for ss in e["s"][:3]: msg += "  " + ss + "\n"
            msg += "\n"
        send(msg)

    if not iykg_list and not list_21 and not list_12:
        send("=== " + tarih + " ===\nUygun maç bulunamadı.")

    print("\nBitti!")

if __name__ == "__main__":
    main()
