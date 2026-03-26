"""
PRN (Pronoun) tegini to'g'rilash skripti.
Hunspell lug'atidan kelgan so'zlar noto'g'ri PRN deb belgilangan.
Haqiqiy olmoshlarni saqlagan holda, qolganlarni to'g'ri POS ga o'tkazamiz.
"""
import csv

INPUT = r"c:\Users\E-MaxPCShop\PycharmProjects\CSE_UzMorph\uzmorph\data\root.csv"
OUTPUT = INPUT  # overwrite

# ===== HAQIQIY O'ZBEK OLMOSHLARI =====
REAL_PRONOUNS = {
    # Shaxs olmoshlari
    "men", "sen", "u", "biz", "siz", "ular",
    # Ko'rsatish olmoshlari
    "bu", "shu", "shubu", "o'sha", "ana", "mana", "anov", "anov-manov",
    "anavi", "anovi", "anovi-manovi", "manavi", "manovu",
    # So'roq olmoshlari
    "kim", "nima", "qayer", "qaysi", "qanday", "qancha", "necha",
    "nimaga", "nechta", "qayerda", "kimga", "kimdan", "nimadan",
    # Belgilash olmoshlari
    "barcha", "bari", "hamma", "har", "harkim", "harnima", "harnimsa",
    "harqayer", "harqaysi", "harqancha", "harqanday", "herchand",
    "butun", "barchasi",
    # Belgisizlik olmoshlari
    "ba'zi", "ba'zan", "biror", "birov", "biroz", "birnima", "birnimsa",
    "bir-birov", "boshqa", "qaysidir", "nimadir", "kimdir", "allakim",
    "allaqanday", "allaqaysi", "allaqachon", "allaqancha",
    "allanima", "allanarsa", "allanecha", "allanechuk",
    "allamahal", "allavaqt", "alla", "alla-palla",
    "nimaga", "kimga", "qayerga",
    # Bo'lishsizlik olmoshlari
    "hech", "hechkim", "hechnima", "hechqayer", "hechqaysi",
    "hechqanday", "hechqancha", "hechnarsa",
    # O'zlik olmoshlari
    "o'z", "o'zi", "o'zim", "o'zing",
    # Ko'rsatish
    "shu", "shunday", "shuncha", "shunda", "shundan",
    "bunday", "buncha", "bunda", "bundan",
    "unday", "u", "uning",
}

# ===== QO'SHIMCHAGA QARAB POS ANIQLASH =====
POS_DESC = {
    "NOUN": "Ot", "VERB": "Fe'l", "ADJ": "Sifat", "ADV": "Ravish",
    "PRN": "Olmosh", "MOD": "Modal", "AUX": "Yordamchi fe'l",
}

def detect_pos(word):
    """So'z qo'shimchasi va shakliga qarab to'g'ri POS ni aniqlash"""
    w = word.lower().strip()
    
    # -moq bilan tugasa — FE'L
    if w.endswith("moq"):
        return "VERB", "Fe'l"
    
    # -lik/-lik bilan tugasa — odatda ADJ yoki NOUN
    if w.endswith("lik") or w.endswith("liq"):
        return "NOUN", "Ot"
    
    # -chi bilan tugasa — NOUN
    if w.endswith("chi"):
        return "NOUN", "Ot"
    
    # -dor suffiks — NOUN (egador, sarvaqdor...)
    # lekin ba'zilari ADJ ham bo'lishi mumkin
    if w.endswith("dor"):
        return "NOUN", "Ot"
    
    # -kor suffiks — NOUN (ishtirokkor, hunarkor...)
    if w.endswith("kor"):
        return "NOUN", "Ot"
    
    # -tor suffiks — NOUN (dektor, inspektor, direktor...)
    if w.endswith("tor"):
        return "NOUN", "Ot"
    
    # -zor — NOUN (bog'zor, gulzor...)  
    if w.endswith("zor"):
        return "NOUN", "Ot"
    
    # -xon — NOUN
    if w.endswith("xon"):
        return "NOUN", "Ot"
    
    # -don — NOUN 
    if w.endswith("don"):
        return "NOUN", "Ot"
    
    # -bon — NOUN (darvozabon, posbbon...)
    if w.endswith("bon"):
        return "NOUN", "Ot"
    
    # -mon — NOUN yoki ADJ
    if w.endswith("mon"):
        return "NOUN", "Ot"
    
    # -ron — NOUN 
    if w.endswith("ron"):
        return "NOUN", "Ot"
    
    # -ton — NOUN
    if w.endswith("ton"):
        return "NOUN", "Ot"
    
    # -von — NOUN
    if w.endswith("von"):
        return "NOUN", "Ot"
    
    # -ion — NOUN
    if w.endswith("ion"):
        return "NOUN", "Ot"
    
    # -vor — NOUN
    if w.endswith("vor"):
        return "NOUN", "Ot"
    
    # -ov/-ov — ko'pincha NOUN (familiya yoki ot)
    if w.endswith("ov"):
        return "NOUN", "Ot"
    
    # -loq — NOUN yoki ADJ
    if w.endswith("loq"):
        return "NOUN", "Ot"
    
    # -oq — ko'pincha NOUN yoki ADJ
    if w.endswith("oq") or w.endswith("choq"):
        return "NOUN", "Ot"
    
    # -on — ko'pincha NOUN
    if w.endswith("on"):
        return "NOUN", "Ot"
    
    # -or — ko'pincha NOUN
    if w.endswith("or"):
        return "NOUN", "Ot"
    
    # -dir — ko'pincha NOUN
    if w.endswith("dir"):
        return "NOUN", "Ot"
    
    # -roq — ADV (ko'proq, kamroq...)
    if w.endswith("roq"):
        return "ADV", "Ravish"
    
    # Default — NOUN
    return "NOUN", "Ot"


# ===== ASOSIY SKRIPT =====
rows = []
stats = {"kept_prn": 0, "to_verb": 0, "to_noun": 0, "to_adj": 0, "to_adv": 0, "other": 0}

with open(INPUT, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["pos"] == "PRN":
            stem = row["stem"].lower().strip()
            if stem in REAL_PRONOUNS:
                stats["kept_prn"] += 1
            else:
                new_pos, new_desc = detect_pos(stem)
                row["pos"] = new_pos
                row["description"] = new_desc
                stats[f"to_{new_pos.lower()}"] = stats.get(f"to_{new_pos.lower()}", 0) + 1
        rows.append(row)

# Yozish
with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["stem", "pos", "description"])
    writer.writeheader()
    writer.writerows(rows)

print("=== PRN teg to'g'rilash natijalari ===")
print(f"  PRN sifatida qoldi:    {stats['kept_prn']}")
print(f"  VERB ga o'tkazildi:    {stats.get('to_verb', 0)}")
print(f"  NOUN ga o'tkazildi:    {stats.get('to_noun', 0)}")
print(f"  ADJ ga o'tkazildi:     {stats.get('to_adj', 0)}")
print(f"  ADV ga o'tkazildi:     {stats.get('to_adv', 0)}")
print(f"  Jami o'zgartirildi:    {sum(v for k,v in stats.items() if k != 'kept_prn')}")
print(f"\nroot.csv yangilandi!")
