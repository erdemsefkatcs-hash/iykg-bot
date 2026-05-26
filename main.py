import requests, time
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

def gv(o, mId, moId):
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
# 1/1 — Genel %26.36 | Hedef %60+
# ================================================================
def filtre_11(o):
    p=0; s=[]
    iy_ev = gv(o,5,22)
    ms_dep = gv(o,1,3)
    iycs_x2 = gv(o,13,203)

    if iy_ev:
        if 1.05<=iy_ev<=1.10: p+=9; s.append("IY_EV={} %76.09".format(iy_ev))
        elif 1.10<=iy_ev<=1.15: p+=10; s.append("IY_EV={} %79.03".format(iy_ev))
        elif 1.15<=iy_ev<=1.20: p+=8; s.append("IY_EV={} %66.67".format(iy_ev))
        elif 1.20<=iy_ev<=1.25: p+=7; s.append("IY_EV={} %63.00".format(iy_ev))
        elif 1.25<=iy_ev<=1.30: p+=7; s.append("IY_EV={} %65.45".format(iy_ev))

    if ms_dep:
        if 17.10<=ms_dep<=17.15: p+=9; s.append("MS_DEP={} %75.00".format(ms_dep))
        elif 17.40<=ms_dep<=17.45: p+=9; s.append("MS_DEP={} %73.24".format(ms_dep))
        elif 15.00<=ms_dep<=17.10: p+=6; s.append("MS_DEP={} ~%65".format(ms_dep))

    if iycs_x2:
        if 1.95<=iycs_x2<=2.00: p+=7; s.append("IYCS_X2={} %67.31".format(iycs_x2))
        elif 2.10<=iycs_x2<=2.15: p+=7; s.append("IYCS_X2={} %68.12".format(iycs_x2))
        elif 2.25<=iycs_x2<=2.35: p+=6; s.append("IYCS_X2={} %65+".format(iycs_x2))

    # Engel: dep favori ise 1/1 olmaz
    iy_dep = gv(o,5,23)
    if iy_dep and iy_dep<=1.30: p-=8; s.append("ENGEL IY_DEP={} dep favori".format(iy_dep))

    return p, s

# ================================================================
# 2/2 — Genel %17.85 | Hedef %55+
# ================================================================
def filtre_22(o):
    p=0; s=[]
    iy_dep = gv(o,5,23)
    iycs_12 = gv(o,13,34)
    ms_ev = gv(o,1,2)
    dep15_ust = gv(o,15,37)

    if iy_dep:
        if 1.05<=iy_dep<=1.10: p+=8; s.append("IY_DEP={} %66.67".format(iy_dep))
        elif 1.10<=iy_dep<=1.15: p+=8; s.append("IY_DEP={} %65.71".format(iy_dep))
        elif 1.15<=iy_dep<=1.20: p+=8; s.append("IY_DEP={} %68.57".format(iy_dep))
        elif 1.20<=iy_dep<=1.25: p+=9; s.append("IY_DEP={} %76.74".format(iy_dep))
        elif 1.25<=iy_dep<=1.30: p+=8; s.append("IY_DEP={} %66.67".format(iy_dep))
        elif 1.30<=iy_dep<=1.35: p+=7; s.append("IY_DEP={} %60.00".format(iy_dep))

    if iycs_12:
        if 2.00<=iycs_12<=2.05: p+=8; s.append("IYCS_12={} %70.27".format(iycs_12))
        elif 1.95<=iycs_12<=2.00: p+=6; s.append("IYCS_12={} ~%65".format(iycs_12))

    if ms_ev and ms_ev>=17.00:
        p+=8; s.append("MS_EV={} %64+ dep favori".format(ms_ev))

    if dep15_ust and 2.35<=dep15_ust<=2.40:
        p+=6; s.append("DEP15_UST={} %64.86".format(dep15_ust))

    # Engel: ev favori ise 2/2 olmaz
    iy_ev = gv(o,5,22)
    if iy_ev and iy_ev<=1.30: p-=8; s.append("ENGEL IY_EV={} ev favori".format(iy_ev))

    return p, s

# ================================================================
# X/X — Genel %15.46 | Hedef %30+
# ================================================================
def filtre_xx(o):
    p=0; s=[]
    y2_x = gv(o,10,196)
    au25_ust = gv(o,34,53)
    iy05_ust = gv(o,37,58)
    hyg_2y = gv(o,22,237)
    hyg_esi = gv(o,22,238)
    ms_x = gv(o,1,1)

    if y2_x:
        if 2.50<=y2_x<=2.55: p+=9; s.append("2Y_X={} %58.06".format(y2_x))
        elif 2.55<=y2_x<=2.60: p+=8; s.append("2Y_X={} %36.67".format(y2_x))

    if au25_ust:
        if 1.10<=au25_ust<=1.20: p+=7; s.append("AU25_UST={} %32.49".format(au25_ust))
        elif 1.05<=au25_ust<=1.10: p+=8; s.append("AU25_UST={} %39.02".format(au25_ust))

    if iy05_ust:
        if 1.80<=iy05_ust<=1.90: p+=7; s.append("IY05_UST={} %29.64".format(iy05_ust))
        elif 1.70<=iy05_ust<=1.80: p+=7; s.append("IY05_UST={} %31.39".format(iy05_ust))

    if hyg_2y and 2.20<=hyg_2y<=2.30:
        p+=7; s.append("HYG_2Y={} %43.40".format(hyg_2y))
    elif hyg_2y and 2.40<=hyg_2y<=2.50:
        p+=6; s.append("HYG_2Y={} %30.77".format(hyg_2y))

    if hyg_esi and 2.10<=hyg_esi<=2.20:
        p+=7; s.append("HYG_ESI={} %47.06".format(hyg_esi))

    if ms_x and 2.10<=ms_x<=2.20:
        p+=5; s.append("MS_X={} %30.00".format(ms_x))
    elif ms_x and 2.20<=ms_x<=2.25:
        p+=6; s.append("MS_X={} %39.39".format(ms_x))

    # Engel
    iy_ev = gv(o,5,22)
    if iy_ev and iy_ev<=1.20: p-=7
    iy_dep = gv(o,5,23)
    if iy_dep and iy_dep<=1.20: p-=7

    return p, s

# ================================================================
# X/1 — Genel %14.74 | Hedef %28+
# ================================================================
def filtre_x1(o):
    p=0; s=[]
    y2_ev = gv(o,10,32)
    ms_dep = gv(o,1,3)
    iy_dep = gv(o,5,23)
    ev15_ust = gv(o,18,39)

    if y2_ev:
        if 1.65<=y2_ev<=1.70: p+=7; s.append("2Y_EV={} %34.21".format(y2_ev))
        elif 1.60<=y2_ev<=1.65: p+=6; s.append("2Y_EV={} %30.00".format(y2_ev))
        elif 1.55<=y2_ev<=1.60: p+=5; s.append("2Y_EV={} %26.00".format(y2_ev))

    if ms_dep:
        if 7.40<=ms_dep<=7.45: p+=7; s.append("MS_DEP={} %31.82".format(ms_dep))
        elif 8.40<=ms_dep<=8.45: p+=7; s.append("MS_DEP={} %34.15".format(ms_dep))
        elif 7.00<=ms_dep<=7.50: p+=5; s.append("MS_DEP={} ~%30".format(ms_dep))
        elif 7.50<=ms_dep<=8.50: p+=5; s.append("MS_DEP={} ~%30".format(ms_dep))

    if iy_dep:
        if 4.85<=iy_dep<=4.90: p+=6; s.append("IY_DEP={} %29.56".format(iy_dep))
        elif 6.90<=iy_dep<=6.95: p+=6; s.append("IY_DEP={} %30.23".format(iy_dep))
        elif 7.55<=iy_dep<=7.60: p+=6; s.append("IY_DEP={} %31.82".format(iy_dep))

    if ev15_ust and 2.90<=ev15_ust<=2.95:
        p+=6; s.append("EV15_UST={} %31.25".format(ev15_ust))

    # Engel
    iy_ev = gv(o,5,22)
    if iy_ev and iy_ev>=5.20: p-=6

    return p, s

# ================================================================
# X/2 — Genel %11.15 | Hedef %25+
# ================================================================
def filtre_x2(o):
    p=0; s=[]
    iy_ev = gv(o,5,22)
    ms_ev = gv(o,1,2)
    y2_dep = gv(o,10,197)
    iycs_12 = gv(o,13,34)
    y2_ev = gv(o,10,32)

    if iy_ev:
        if 5.20<=iy_ev<=5.30: p+=8; s.append("IY_EV={} %31.19".format(iy_ev))
        elif 5.10<=iy_ev<=5.20: p+=7; s.append("IY_EV={} %30.59".format(iy_ev))
        elif 4.80<=iy_ev<=4.90: p+=7; s.append("IY_EV={} %28.32".format(iy_ev))
        elif 4.90<=iy_ev<=5.00: p+=6; s.append("IY_EV={} ~%27".format(iy_ev))

    if ms_ev:
        if 4.80<=ms_ev<=4.90: p+=7; s.append("MS_EV={} %24.68".format(ms_ev))
        elif 5.10<=ms_ev<=5.20: p+=7; s.append("MS_EV={} %26.79".format(ms_ev))
        elif 5.00<=ms_ev<=5.10: p+=6; s.append("MS_EV={} %24.00".format(ms_ev))
        elif 5.50<=ms_ev<=5.60: p+=7; s.append("MS_EV={} %23.88".format(ms_ev))

    if y2_dep and 1.90<=y2_dep<=2.00:
        p+=7; s.append("2Y_DEP={} %26.32".format(y2_dep))

    # Kombo bonus
    if iy_ev and iycs_12:
        if 4.80<=iy_ev<=4.90 and 1.50<=iycs_12<=1.60:
            p+=6; s.append("KOMBO IY_EV+IYCS_12 %33.33!")
    if ms_ev and iycs_12:
        if 5.00<=ms_ev<=5.10 and 1.50<=iycs_12<=1.60:
            p+=6; s.append("KOMBO MS_EV+IYCS_12 %33.33!")
        elif 5.50<=ms_ev<=5.60 and 1.50<=iycs_12<=1.60:
            p+=5; s.append("KOMBO MS_EV+IYCS_12 %29.63!")

    if y2_dep and iycs_12 and 1.90<=y2_dep<=2.00 and 1.50<=iycs_12<=1.60:
        p+=5; s.append("KOMBO 2Y_DEP+IYCS_12 %22.73!")

    # Engel
    iy_dep = gv(o,5,23)
    if iy_dep and iy_dep<=1.25: p-=7

    return p, s

# ================================================================
# 2/X — Genel %4.84 | Hedef %12+
# ================================================================
def filtre_2x(o):
    p=0; s=[]
    y2_dep = gv(o,10,197)
    iy_ev = gv(o,5,22)

    if y2_dep:
        if 6.00<=y2_dep<=6.05: p+=6; s.append("2Y_DEP={} %29.17".format(y2_dep))
        elif 5.70<=y2_dep<=5.75: p+=5; s.append("2Y_DEP={} %14.29".format(y2_dep))
        elif 5.50<=y2_dep<=5.65: p+=5; s.append("2Y_DEP={} ~%12".format(y2_dep))

    if iy_ev:
        if 3.95<=iy_ev<=4.00: p+=5; s.append("IY_EV={} ~%12".format(iy_ev))

    return p, s

# ================================================================
# 1/X — Genel %4.83 | Hedef %12+
# ================================================================
def filtre_1x(o):
    p=0; s=[]
    y2_ev = gv(o,10,32)
    iy_dep = gv(o,5,23)

    if y2_ev:
        if 3.95<=y2_ev<=4.05: p+=5; s.append("2Y_EV={} ~%12".format(y2_ev))

    if iy_dep:
        if 4.00<=iy_dep<=4.10: p+=5; s.append("IY_DEP={} ~%12".format(iy_dep))

    return p, s

# ================================================================
# 2/1 — Genel %2.64 | Hedef %10+
# ================================================================
def filtre_21(o):
    p=0; s=[]
    au25_ust = gv(o,34,53)
    iy_x = gv(o,5,21)
    ev15_ust = gv(o,18,39)
    y2_x = gv(o,10,196)
    dep15_alt = gv(o,15,207)
    ms_dep = gv(o,1,3)

    if au25_ust and 2.75<=au25_ust<=2.80:
        p+=8; s.append("AU25_UST={} %14.58".format(au25_ust))
    elif au25_ust and 2.70<=au25_ust<=2.75:
        p+=6; s.append("AU25_UST={} ~%12".format(au25_ust))

    if iy_x and 3.05<=iy_x<=3.10:
        p+=7; s.append("IY_X={} %11.90".format(iy_x))

    if ev15_ust and 2.30<=ev15_ust<=2.35:
        p+=5; s.append("EV15_UST={} %7.69".format(ev15_ust))
    elif ev15_ust and 2.25<=ev15_ust<=2.30:
        p+=4; s.append("EV15_UST={} ~%7".format(ev15_ust))

    if y2_x and 6.50<=y2_x<=6.55:
        p+=7; s.append("2Y_X={} %13.16".format(y2_x))

    if dep15_alt and 3.95<=dep15_alt<=4.00:
        p+=6; s.append("DEP15_ALT={} %11.67".format(dep15_alt))

    if ms_dep:
        if 5.95<=ms_dep<=6.00: p+=5; s.append("MS_DEP={} %8.33".format(ms_dep))
        elif 7.00<=ms_dep<=7.05: p+=5; s.append("MS_DEP={} %8.33".format(ms_dep))

    # Engel: dep çok favori ise 2/1 olmaz
    iy_dep = gv(o,5,23)
    if iy_dep and iy_dep<=1.30: p-=6

    return p, s

# ================================================================
# 1/2 — Genel %2.14 | Hedef %8+
# ================================================================
def filtre_12(o):
    p=0; s=[]
    ms_ev = gv(o,1,2)
    kg_yok = gv(o,8,14)
    iy_ev = gv(o,5,22)
    y2_x = gv(o,10,196)
    y2_dep = gv(o,10,197)
    iy15_ust = gv(o,9,28)

    if ms_ev:
        if 4.90<=ms_ev<=5.00: p+=8; s.append("MS_EV={} %8.97".format(ms_ev))
        elif 5.40<=ms_ev<=5.50: p+=7; s.append("MS_EV={} %7.81".format(ms_ev))
        elif 5.00<=ms_ev<=5.10: p+=6; s.append("MS_EV={} ~%7".format(ms_ev))

    if kg_yok:
        if 2.90<=kg_yok<=3.00: p+=7; s.append("KG_YOK={} %8.70".format(kg_yok))
        elif 2.80<=kg_yok<=2.90: p+=6; s.append("KG_YOK={} ~%7".format(kg_yok))
        elif 2.95<=kg_yok<=3.00: p+=7; s.append("KG_YOK={} %9.38".format(kg_yok))

    if iy_ev and 5.35<=iy_ev<=5.40:
        p+=7; s.append("IY_EV={} %10.00".format(iy_ev))
    elif iy_ev and 5.30<=iy_ev<=5.35:
        p+=6; s.append("IY_EV={} ~%8".format(iy_ev))

    if y2_x and 5.70<=y2_x<=5.75:
        p+=6; s.append("2Y_X={} %7.94".format(y2_x))

    if y2_dep and 6.15<=y2_dep<=6.20:
        p+=6; s.append("2Y_DEP={} %8.82".format(y2_dep))

    if iy15_ust and 1.90<=iy15_ust<=1.95:
        p+=5; s.append("IY15_UST={} %7.27".format(iy15_ust))

    # Engel: ev çok favori ise 1/2 olmaz
    iy_ev2 = gv(o,5,22)
    if iy_ev2 and iy_ev2<=1.25: p-=6

    return p, s

# ================================================================
# IYKG — Genel %5.31 | Hedef %15+
# ================================================================
def filtre_iykg(o):
    p=0; s=[]
    kg_var = gv(o,8,13)
    kg_yok = gv(o,8,14)
    iy05_ust = gv(o,37,58)
    au35_ust = gv(o,39,59)
    au35_alt = gv(o,39,289)
    iy15_ust = gv(o,9,28)
    iy15_alt = gv(o,9,29)

    if kg_var and 1.00<=kg_var<=1.10:
        p+=6; s.append("KG_VAR={} %13.65".format(kg_var))

    if kg_yok:
        if 2.80<=kg_yok<=2.90: p+=7; s.append("KG_YOK={} %14.85".format(kg_yok))
        elif 3.00<=kg_yok<=3.10: p+=6; s.append("KG_YOK={} %13.73".format(kg_yok))
        elif 2.50<=kg_yok<=2.60: p+=6; s.append("KG_YOK={} %11.90".format(kg_yok))

    if iy05_ust and 1.00<=iy05_ust<=1.10:
        p+=6; s.append("IY05_UST={} %14.59".format(iy05_ust))

    if au35_ust and 1.90<=au35_ust<=2.00:
        p+=5; s.append("AU35_UST={} %11.75".format(au35_ust))

    if au35_alt and 1.30<=au35_alt<=1.40:
        p+=5; s.append("AU35_ALT={} %11.41".format(au35_alt))

    if iy15_ust and 2.00<=iy15_ust<=2.10:
        p+=5; s.append("IY15_UST={} %12.07".format(iy15_ust))
    elif iy15_ust and 1.90<=iy15_ust<=2.00:
        p+=5; s.append("IY15_UST={} %13.89".format(iy15_ust))

    if iy15_alt and 1.30<=iy15_alt<=1.40:
        p+=5; s.append("IY15_ALT={} %11.92".format(iy15_alt))

    # İkili kombolar
    if iy05_ust and kg_var and 1.00<=iy05_ust<=1.10 and 1.10<=kg_var<=1.20:
        p+=6; s.append("KOMBO IY05+KG_VAR %26.47!")
    if kg_var and au35_ust and 1.00<=kg_var<=1.10 and 1.90<=au35_ust<=2.00:
        p+=5; s.append("KOMBO KG_VAR+AU35_UST %20.59!")
    if au35_alt and iy15_ust and 1.30<=au35_alt<=1.40 and 1.90<=iy15_ust<=2.00:
        p+=5; s.append("KOMBO AU35_ALT+IY15_UST %19.35!")
    if au35_ust and iy15_ust and 1.90<=au35_ust<=2.00 and 1.90<=iy15_ust<=2.00:
        p+=5; s.append("KOMBO AU35_UST+IY15_UST %18.42!")

    return p, s

# ================================================================
# 6+ GOL — Genel %6.63 | Hedef %25+
# ================================================================
def filtre_6gol(o):
    p=0; s=[]
    iy15_ust = gv(o,9,28)
    iy15_alt = gv(o,9,29)
    au35_ust = gv(o,39,59)
    au35_alt = gv(o,39,289)
    ms_ev = gv(o,1,2)
    iy_dep = gv(o,5,23)

    if iy15_ust:
        if 2.10<=iy15_ust<=2.20: p+=9; s.append("IY15_UST={} %36.62".format(iy15_ust))
        elif 1.90<=iy15_ust<=2.00: p+=8; s.append("IY15_UST={} %26.17".format(iy15_ust))
        elif 1.80<=iy15_ust<=1.90: p+=7; s.append("IY15_UST={} %25.50".format(iy15_ust))

    if iy15_alt:
        if 1.30<=iy15_alt<=1.40: p+=7; s.append("IY15_ALT={} %29.02".format(iy15_alt))
        elif 1.40<=iy15_alt<=1.50: p+=7; s.append("IY15_ALT={} %25.34".format(iy15_alt))

    if au35_ust and 1.90<=au35_ust<=2.00:
        p+=7; s.append("AU35_UST={} %30.56".format(au35_ust))

    if au35_alt and 1.30<=au35_alt<=1.40:
        p+=6; s.append("AU35_ALT={} %25.56".format(au35_alt))

    if ms_ev and ms_ev>=17.10:
        p+=7; s.append("MS_EV={} %30.68".format(ms_ev))

    if iy_dep and 1.10<=iy_dep<=1.20:
        p+=8; s.append("IY_DEP={} %28.57".format(iy_dep))

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
    print("Toplam: " + str(len(maclar)) + " mac")

    filtreler = {
        "1/1": (filtre_11, 10),
        "2/2": (filtre_22, 10),
        "X/X": (filtre_xx, 10),
        "X/1": (filtre_x1,  8),
        "X/2": (filtre_x2,  8),
        "2/X": (filtre_2x,  6),
        "1/X": (filtre_1x,  6),
        "2/1": (filtre_21,  8),
        "1/2": (filtre_12,  8),
        "IYKG":(filtre_iykg,8),
        "6GOL":(filtre_6gol,9),
    }

    listeler = {k: [] for k in filtreler}

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
        for tip, (fonk, esik) in filtreler.items():
            puan, sinyaller = fonk(o)
            if puan >= esik:
                listeler[tip].append({**info, "puan": puan, "s": sinyaller})

    # Ekran
    print("\n" + "="*60)
    for tip in filtreler:
        sirali = sorted(listeler[tip], key=lambda x: -x["puan"])
        print("\n=== " + tip + " (" + str(len(sirali)) + " mac) ===")
        for e in sirali[:15]:
            print("  " + e["saat"] + " " + e["ev"] + " vs " + e["dep"] + " P:" + str(e["puan"]))
            print("    " + " | ".join(e["s"][:3]))

    # Telegram
    for tip in filtreler:
        sirali = sorted(listeler[tip], key=lambda x: -x["puan"])
        if not sirali: continue
        msg = "=== " + tip + " === " + tarih + "\n" + str(len(sirali)) + " mac\n\n"
        for e in sirali[:10]:
            msg += e["saat"] + " P:" + str(e["puan"]) + "\n"
            msg += e["ev"] + " vs " + e["dep"] + "\n"
            msg += e["lig"] + "\n"
            for ss in e["s"][:3]: msg += "  " + ss + "\n"
            msg += "\n"
        send(msg)

    if all(len(v)==0 for v in listeler.values()):
        send("=== " + tarih + " ===\nUygun mac bulunamadi.")

    print("\nBitti!")

if __name__ == "__main__":
    main()
