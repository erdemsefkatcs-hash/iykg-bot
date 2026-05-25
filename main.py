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
# 1/1 FİLTRESİ — Genel %26.27
# Hedef: %50+ (2x artış)
# ================================================================
def filtre_11(o):
    p = 0; s = []
    ms = gvmo(o, 1, 2)
    y2 = gv(o, 32)
    iysn = gv(o, 5)
    iy15 = gv(o, 9)

    if ms:
        if 1.00 <= ms <= 1.05: p += 8; s.append("MS={} %62.24".format(ms))
        elif 1.05 <= ms <= 1.10: p += 6; s.append("MS={} %56.80".format(ms))
        elif 1.10 <= ms <= 1.15: p += 4; s.append("MS={} %50.00".format(ms))

    if y2:
        if 1.10 <= y2 <= 1.15: p += 7; s.append("2Y={} %67.57".format(y2))
        elif 1.15 <= y2 <= 1.20: p += 6; s.append("2Y={} %63.00".format(y2))
        elif 1.20 <= y2 <= 1.25: p += 5; s.append("2Y={} %58.00".format(y2))
        elif 1.25 <= y2 <= 1.30: p += 5; s.append("2Y={} %55.00".format(y2))
        elif 1.30 <= y2 <= 1.35: p += 4; s.append("2Y={} %51.00".format(y2))

    if iysn:
        if 1.10 <= iysn <= 1.15: p += 7; s.append("IY_X={} %74.40".format(iysn))
        elif 1.15 <= iysn <= 1.20: p += 6; s.append("IY_X={} %70.00".format(iysn))
        elif 1.20 <= iysn <= 1.25: p += 5; s.append("IY_X={} %65.00".format(iysn))
        elif 1.25 <= iysn <= 1.30: p += 5; s.append("IY_X={} %66.12".format(iysn))
        elif 1.30 <= iysn <= 1.35: p += 4; s.append("IY_X={} %58.00".format(iysn))

    if iy15:
        if 1.10 <= iy15 <= 1.15: p += 5; s.append("IY15={} %60.00".format(iy15))
        elif 1.15 <= iy15 <= 1.20: p += 4; s.append("IY15={} %55.00".format(iy15))
        elif 1.20 <= iy15 <= 1.25: p += 3; s.append("IY15={} %50.00".format(iy15))

    # Engel: MS çok yüksekse 1/1 olmaz
    if ms and ms >= 4.10: p -= 5

    return p, s

# ================================================================
# 2/2 FİLTRESİ — Genel %17.85
# Hedef: %35+ (2x artış)
# ================================================================
def filtre_22(o):
    p = 0; s = []
    iycs = gv(o, 13)
    dep15 = gv(o, 15)
    ms = gvmo(o, 1, 2)
    iysn = gv(o, 5)
    au25 = gv(o, 34)

    if iycs:
        if 1.55 <= iycs <= 1.60: p += 7; s.append("IYCS={} %49.21".format(iycs))
        elif 1.60 <= iycs <= 1.65: p += 7; s.append("IYCS={} %49.21".format(iycs))
        elif 1.65 <= iycs <= 1.70: p += 6; s.append("IYCS={} %45.00".format(iycs))
        elif 1.70 <= iycs <= 1.75: p += 6; s.append("IYCS={} %45.00".format(iycs))
        elif 1.75 <= iycs <= 1.80: p += 7; s.append("IYCS={} %56.67".format(iycs))
        elif 1.80 <= iycs <= 1.85: p += 6; s.append("IYCS={} %50.00".format(iycs))
        elif 1.85 <= iycs <= 1.90: p += 7; s.append("IYCS={} %56.14".format(iycs))
        elif 1.45 <= iycs <= 1.55: p += 5; s.append("IYCS={} %42.29".format(iycs))
        elif 1.40 <= iycs <= 1.45: p += 4; s.append("IYCS={} %38.00".format(iycs))

    if dep15:
        if 2.00 <= dep15 <= 2.05: p += 6; s.append("Dep15={} %42.48".format(dep15))
        elif 2.05 <= dep15 <= 2.10: p += 5; s.append("Dep15={} %40.00".format(dep15))
        elif 1.95 <= dep15 <= 2.00: p += 4; s.append("Dep15={} %38.00".format(dep15))

    if ms and ms >= 15.00:
        p += 6; s.append("MS={} %65+ dep favori".format(ms))

    if iysn:
        if 1.05 <= iysn <= 1.10: p += 4; s.append("IY_X={} %38.00".format(iysn))

    if au25:
        if 1.55 <= au25 <= 1.60: p += 4; s.append("AU25={} %37.00".format(au25))

    # Engel: IY_Sonucu dusukse 2/2 olmaz
    if iysn and iysn <= 1.10: p -= 5

    return p, s

# ================================================================
# X/1 FİLTRESİ — Genel %14.78
# Hedef: %25+ (1.7x artış)
# ================================================================
def filtre_x1(o):
    p = 0; s = []
    y2 = gv(o, 32)
    iysn = gv(o, 5)
    ms = gvmo(o, 1, 2)
    ev15 = gv(o, 18)
    iy15 = gv(o, 9)

    if y2:
        if 1.40 <= y2 <= 1.45: p += 6; s.append("2Y={} %24.88".format(y2))
        elif 1.45 <= y2 <= 1.50: p += 5; s.append("2Y={} %23.00".format(y2))
        elif 1.35 <= y2 <= 1.40: p += 4; s.append("2Y={} %21.00".format(y2))
        elif 1.50 <= y2 <= 1.55: p += 4; s.append("2Y={} %20.00".format(y2))

    if iysn:
        if 1.50 <= iysn <= 1.55: p += 6; s.append("IY_X={} %24.03".format(iysn))
        elif 1.45 <= iysn <= 1.50: p += 5; s.append("IY_X={} %22.00".format(iysn))
        elif 1.40 <= iysn <= 1.45: p += 5; s.append("IY_X={} %23.10".format(iysn))
        elif 1.55 <= iysn <= 1.60: p += 4; s.append("IY_X={} %20.00".format(iysn))

    if ms:
        if 1.15 <= ms <= 1.20: p += 4; s.append("MS_EV={} %22.00".format(ms))
        elif 1.20 <= ms <= 1.25: p += 3; s.append("MS_EV={} %20.00".format(ms))

    if ev15:
        if 2.85 <= ev15 <= 2.95: p += 4; s.append("Ev15={} %23.00".format(ev15))
        elif 2.90 <= ev15 <= 3.00: p += 4; s.append("Ev15={} %24.00".format(ev15))

    # Engel: IY_Sonucu cok yuksekse X/1 olmaz
    if iysn and iysn >= 5.20: p -= 5

    return p, s

# ================================================================
# X/2 FİLTRESİ — Genel %11.20
# Hedef: %20+ (1.8x artış)
# ================================================================
def filtre_x2(o):
    p = 0; s = []
    iycs = gv(o, 13)
    iysn = gv(o, 5)
    ms = gvmo(o, 1, 2)
    y2 = gv(o, 32)
    dep15 = gv(o, 15)

    if iycs:
        if 1.50 <= iycs <= 1.55: p += 6; s.append("IYCS={} %23.10".format(iycs))
        elif 1.55 <= iycs <= 1.60: p += 5; s.append("IYCS={} %22.00".format(iycs))
        elif 1.65 <= iycs <= 1.70: p += 6; s.append("IYCS={} %24.55".format(iycs))
        elif 1.60 <= iycs <= 1.65: p += 5; s.append("IYCS={} %21.00".format(iycs))
        elif 1.45 <= iycs <= 1.50: p += 4; s.append("IYCS={} %19.00".format(iycs))

    if iysn:
        if 5.15 <= iysn <= 5.20: p += 6; s.append("IY_X={} %33.33".format(iysn))
        elif 5.20 <= iysn <= 5.30: p += 6; s.append("IY_X={} %32.00".format(iysn))
        elif 4.80 <= iysn <= 4.90: p += 5; s.append("IY_X={} %27.00".format(iysn))
        elif 4.50 <= iysn <= 4.60: p += 4; s.append("IY_X={} %24.00".format(iysn))

    if ms:
        if 3.55 <= ms <= 3.60: p += 5; s.append("MS_EV={} %21.57".format(ms))
        elif 4.80 <= ms <= 4.85: p += 6; s.append("MS_EV={} %37.84".format(ms))
        elif 4.50 <= ms <= 4.60: p += 5; s.append("MS_EV={} %28.00".format(ms))
        elif 3.40 <= ms <= 3.55: p += 4; s.append("MS_EV={} %19.00".format(ms))

    if y2:
        if 4.70 <= y2 <= 4.75: p += 5; s.append("2Y={} %31.25".format(y2))
        elif 4.50 <= y2 <= 4.60: p += 4; s.append("2Y={} %27.00".format(y2))

    # Engel: IY_Sonucu dusukse X/2 olmaz
    if iysn and iysn <= 1.25: p -= 5

    return p, s

# ================================================================
# X/X FİLTRESİ — Genel %15.47
# Hedef: %28+ (1.8x artış)
# ================================================================
def filtre_xx(o):
    p = 0; s = []
    au25 = gv(o, 34)
    iy05 = gv(o, 37)
    kg = gv(o, 8)
    au35 = gv(o, 39)
    tc = gv(o, 36)

    if au25:
        if 1.05 <= au25 <= 1.10: p += 7; s.append("AU25={} %40.00".format(au25))
        elif 1.10 <= au25 <= 1.15: p += 7; s.append("AU25={} %33.91".format(au25))
        elif 1.15 <= au25 <= 1.20: p += 6; s.append("AU25={} %31.13".format(au25))
        elif 1.20 <= au25 <= 1.25: p += 5; s.append("AU25={} %28.00".format(au25))

    if iy05:
        if 1.75 <= iy05 <= 1.80: p += 6; s.append("IY05={} %32.55".format(iy05))
        elif 1.80 <= iy05 <= 1.85: p += 6; s.append("IY05={} %30.00".format(iy05))
        elif 1.85 <= iy05 <= 1.90: p += 5; s.append("IY05={} %28.20".format(iy05))
        elif 1.70 <= iy05 <= 1.75: p += 4; s.append("IY05={} %26.00".format(iy05))

    if au35:
        if 1.05 <= au35 <= 1.10: p += 5; s.append("AU35={} %30.00".format(au35))
        elif 1.10 <= au35 <= 1.15: p += 5; s.append("AU35={} %28.00".format(au35))
        elif 1.15 <= au35 <= 1.20: p += 4; s.append("AU35={} %26.00".format(au35))

    if tc:
        if 1.85 <= tc <= 1.90: p += 4; s.append("TekCift={} %28.00".format(tc))
        elif 1.80 <= tc <= 1.85: p += 3; s.append("TekCift={} %26.00".format(tc))

    # Engel: AU25 cok yuksekse X/X olmaz
    if au25 and au25 >= 2.50: p -= 4
    if iy05 and iy05 >= 2.50: p -= 4

    return p, s

# ================================================================
# IYKG FİLTRESİ — Genel %5.29
# ================================================================
def filtre_iykg(o):
    p = 0; s = []
    kg = gv(o, 8); au35 = gv(o, 39); iy15 = gv(o, 9)
    k95 = gv(o, 47); iy05 = gv(o, 37); dep15 = gv(o, 15)

    if kg:
        if 1.05 <= kg <= 1.10: p += 5; s.append("KG={} %14.75".format(kg))
        elif 1.10 <= kg <= 1.15: p += 4; s.append("KG={} %12.81".format(kg))
        elif 1.15 <= kg <= 1.20: p += 4; s.append("KG={} %11.32".format(kg))
        elif 1.20 <= kg <= 1.25: p += 3; s.append("KG={} %10.77".format(kg))
        elif 1.25 <= kg <= 1.30: p += 3; s.append("KG={} %9.44".format(kg))

    if au35:
        if 1.65 <= au35 <= 1.70: p += 5; s.append("AU35={} %13.11".format(au35))
        elif 1.90 <= au35 <= 2.00: p += 5; s.append("AU35={} %11.90".format(au35))
        elif 1.55 <= au35 <= 1.65: p += 4; s.append("AU35={} %10.17".format(au35))
        elif 1.70 <= au35 <= 1.75: p += 4; s.append("AU35={} %8.74".format(au35))

    if iy15:
        if 1.90 <= iy15 <= 1.95: p += 5; s.append("IY15={} %15.38".format(iy15))
        elif 2.00 <= iy15 <= 2.10: p += 5; s.append("IY15={} %13.33".format(iy15))
        elif 1.80 <= iy15 <= 1.90: p += 3; s.append("IY15={} %9.23".format(iy15))

    if k95 and 2.05 <= k95 <= 2.10:
        p += 4; s.append("K9.5={} %14.74".format(k95))

    if iy05:
        if 3.30 <= iy05 <= 3.35: p += 4; s.append("IY05={} %21.62".format(iy05))
        elif 3.45 <= iy05 <= 3.50: p += 4; s.append("IY05={} %19.05".format(iy05))

    if dep15:
        if 1.90 <= dep15 <= 1.95: p += 4; s.append("Dep15={} %11.00".format(dep15))
        elif 2.15 <= dep15 <= 2.20: p += 4; s.append("Dep15={} %11.32".format(dep15))

    # Kombo bonuslar
    if iy15 and au35 and 1.90 <= iy15 <= 1.95 and 1.95 <= au35 <= 2.00:
        p += 6; s.append("KOMBO IY15+AU35 %35!")
    if kg and au35 and 1.05 <= kg <= 1.10 and 1.90 <= au35 <= 1.95:
        p += 5; s.append("KOMBO KG+AU35 %27!")
    if kg and dep15 and 1.15 <= kg <= 1.20 and 1.90 <= dep15 <= 1.95:
        p += 5; s.append("KOMBO KG+Dep15 %26!")

    return p, s

# ================================================================
# 2/1 FİLTRESİ — Genel %2.64
# ================================================================
def filtre_21(o):
    p = 0; s = []
    au25 = gv(o, 34); iysn = gv(o, 5); kg = gv(o, 8)
    ev15 = gv(o, 18); iy05 = gv(o, 37); iy15 = gv(o, 9)
    y2 = gv(o, 32); ms_ev = gvmo(o, 1, 2); iycs = gv(o, 13)

    if au25 and 2.75 <= au25 <= 2.80: p += 7; s.append("AU25={} %14.04 ALTIN".format(au25))
    elif au25 and 2.55 <= au25 <= 2.65: p += 5; s.append("AU25={} ~%15".format(au25))

    if iysn:
        if 2.60 <= iysn <= 2.70: p += 5; s.append("IY_X={} %10.20".format(iysn))
        elif 3.30 <= iysn <= 3.40: p += 4; s.append("IY_X={} %9.76".format(iysn))
        elif 1.26 <= iysn <= 1.35: p += 4; s.append("IY_X={} %10.53".format(iysn))
        elif 1.60 <= iysn <= 1.65: p += 4; s.append("IY_X={} %7.75".format(iysn))

    if kg and 1.10 <= kg <= 1.17: p += 3; s.append("KG={} ~%9".format(kg))
    if ev15 and 2.30 <= ev15 <= 2.35: p += 5; s.append("Ev15={} %9.52".format(ev15))
    if iy05 and 2.50 <= iy05 <= 2.60: p += 4; s.append("IY05={} %10.00".format(iy05))
    if iy15 and 1.80 <= iy15 <= 1.87: p += 4; s.append("IY15={} %11.76".format(iy15))
    if y2 and 1.20 <= y2 <= 1.25: p += 5; s.append("2Y={} %11.11".format(y2))
    if ms_ev and 4.55 <= ms_ev <= 4.70: p += 4; s.append("MS_EV={} %10.71".format(ms_ev))

    if iycs and iycs >= 1.40: p -= 3
    if iysn and iysn >= 5.50: p -= 3

    return p, s

# ================================================================
# 1/2 FİLTRESİ — Genel %2.13
# ================================================================
def filtre_12(o):
    p = 0; s = []
    dep15 = gv(o, 15); ms_dep = gvmo(o, 1, 3); iy15 = gv(o, 9)
    iycs = gv(o, 13); y2 = gv(o, 32); iysn = gv(o, 5)
    iy05 = gv(o, 37); kg = gv(o, 8)

    if dep15:
        if 1.70 <= dep15 <= 1.75: p += 5; s.append("Dep15={} %5.52".format(dep15))
        elif 2.10 <= dep15 <= 2.15: p += 5; s.append("Dep15={} %6.45".format(dep15))
        elif 2.45 <= dep15 <= 2.50: p += 5; s.append("Dep15={} %11.54".format(dep15))
        elif 1.60 <= dep15 <= 1.70: p += 4; s.append("Dep15={} %4.41".format(dep15))
        elif 2.25 <= dep15 <= 2.30: p += 4; s.append("Dep15={} %6.90".format(dep15))

    if ms_dep:
        if 4.90 <= ms_dep <= 4.95: p += 6; s.append("MS_DEP={} %13.51".format(ms_dep))
        elif 5.45 <= ms_dep <= 5.50: p += 6; s.append("MS_DEP={} %12.50".format(ms_dep))
        elif 3.50 <= ms_dep <= 3.55: p += 4; s.append("MS_DEP={} %6.72".format(ms_dep))

    if iy15 and 1.78 <= iy15 <= 1.82: p += 6; s.append("IY15={} %13.16".format(iy15))

    if iycs:
        if 1.55 <= iycs <= 1.58: p += 6; s.append("IYCS={} %12.90".format(iycs))
        elif 1.61 <= iycs <= 1.70: p += 5; s.append("IYCS={} %9.52".format(iycs))
        elif 1.48 <= iycs <= 1.55: p += 4; s.append("IYCS={} %8.57".format(iycs))
        elif 1.40 <= iycs <= 1.48: p += 3; s.append("IYCS={} %7.04".format(iycs))

    if y2:
        if 4.25 <= y2 <= 4.30: p += 7; s.append("2Y={} %15.00 ALTIN".format(y2))
        elif 3.85 <= y2 <= 3.95: p += 5; s.append("2Y={} %13.33".format(y2))
        elif 3.10 <= y2 <= 3.20: p += 4; s.append("2Y={} %9.76".format(y2))
        elif 3.30 <= y2 <= 3.45: p += 4; s.append("2Y={} %9.09".format(y2))

    if iysn and 4.10 <= iysn <= 4.15: p += 4; s.append("IY_X={} %12.50".format(iysn))
    if iy05 and 4.10 <= iy05 <= 4.15: p += 5; s.append("IY05={} %13.64".format(iy05))
    if iysn and 1.10 <= iysn <= 1.20: p -= 4

    return p, s

# ================================================================
# ANA PROGRAM
# ================================================================
def main():
    tarih = datetime.today().strftime("%d.%m.%Y")
    print(datetime.now().strftime("[%H:%M]") + " " + tarih + " Taranıyor...")

    r = requests.get(BASE, params={"sports": 78, "order": "tarih"}, timeout=15)
    d = r.json()
    maclar = d.get("m") or []
    ligler = d.get("l") or {}
    print("Toplam: " + str(len(maclar)) + " maç")

    listeler = {"1/1":[], "2/2":[], "X/1":[], "X/2":[], "X/X":[], "IYKG":[], "2/1":[], "1/2":[]}
    filtreler = {"1/1":filtre_11, "2/2":filtre_22, "X/1":filtre_x1, "X/2":filtre_x2,
                 "X/X":filtre_xx, "IYKG":filtre_iykg, "2/1":filtre_21, "1/2":filtre_12}
    esikler  = {"1/1":10, "2/2":10, "X/1":8, "X/2":8, "X/X":10, "IYKG":8, "2/1":7, "1/2":7}

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
        time.sleep(0.15)

        info = {"saat": saat, "ev": ev, "dep": dep, "lig": lig}

        for tip, fonk in filtreler.items():
            puan, sinyaller = fonk(o)
            if puan >= esikler[tip]:
                listeler[tip].append({**info, "puan": puan, "s": sinyaller})

    # Ekran çıktısı
    print("\n" + "="*60)
    for tip in ["1/1","2/2","X/1","X/2","X/X","IYKG","2/1","1/2"]:
        sirali = sorted(listeler[tip], key=lambda x: -x["puan"])
        print("\n=== " + tip + " (" + str(len(sirali)) + " maç) ===")
        for e in sirali[:15]:
            print("  " + e["saat"] + " " + e["ev"] + " vs " + e["dep"] + " | P:" + str(e["puan"]))
            print("    " + " | ".join(e["s"][:3]))

    # Telegram
    for tip in ["1/1","2/2","X/1","X/2","X/X","IYKG","2/1","1/2"]:
        sirali = sorted(listeler[tip], key=lambda x: -x["puan"])
        if not sirali: continue
        msg = "=== " + tip + " === " + tarih + "\n" + str(len(sirali)) + " maç\n\n"
        for e in sirali[:10]:
            msg += e["saat"] + " P:" + str(e["puan"]) + "\n"
            msg += e["ev"] + " vs " + e["dep"] + "\n"
            msg += e["lig"] + "\n"
            for ss in e["s"][:3]: msg += "  " + ss + "\n"
            msg += "\n"
        send(msg)

    if all(len(v)==0 for v in listeler.values()):
        send("=== " + tarih + " ===\nUygun maç bulunamadı.")

    print("\nBitti!")

if __name__ == "__main__":
    main()
