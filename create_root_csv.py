"""
Merge root1.csv + master_uzbek_stem_pos.csv → root.csv
Format: stem,pos,description  (matching root1.csv format)
Supports multiple POS tags per stem.
"""
import csv
import os

POS_DESC = {
    "NOUN": "Noun {Ot}", "VERB": "Verb {Fe'l}", "ADJ": "Adjective {Sifat}", "NUM": "Numeric {Son}",
    "ADV": "Adverb {Ravish}", "PRN": "Pronoun {Olmosh}", "CNJ": "Conjunction {Bog'lovchi}",
    "ADP": "Adposition {Ko'makchi}", "PRT": "Particle {Yuklama}", "INTJ": "Interjection {Undov}",
    "MOD": "Modal {Modal}", "IMIT": "Imitation {Taqlid}", "AUX": "Auxiliary verb {Yordamchi fe'l}",
    "PPN": "Proper noun {Atoqli ot}", "PUNC": "Punctuation {Tinish belgi}", "SYM": "Symbol {Belgi}"
}

BASE = r"C:\Users\E-MaxPCShop\PycharmProjects\CSE_UzMorph"
root1_path = os.path.join(BASE, "uzmorph", "data", "root1.csv")
master_path = os.path.join(BASE, "master_uzbek_stem_pos.csv")
output_path = os.path.join(BASE, "uzmorph", "data", "root.csv")

# key: (stem, pos), value: description
stems_data = {}

# 1) Load root1.csv — priority source
print("Loading root1.csv...")
with open(root1_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        stem = (row.get("stem") or "").strip().lower()
        pos = (row.get("pos") or "").strip()
        desc = (row.get("description") or "").strip()
        if stem and pos:
            stems_data[(stem, pos)] = desc
print(f"  root1.csv: {len(stems_data)} entries loaded")

# 2) Load master_uzbek_stem_pos.csv
print("Loading master_uzbek_stem_pos.csv...")
added = 0
with open(master_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        stem = (row.get("stem") or "").strip().lower()
        pos = (row.get("pos") or "").strip()
        if not stem or not pos:
            continue
        # Skip multi-word entries
        if " " in stem:
            continue
            
        if (stem, pos) not in stems_data:
            desc = POS_DESC.get(pos, pos)
            stems_data[(stem, pos)] = desc
            added += 1
print(f"  master: {added} new entries added")

# 3) Write root.csv
# We sort primarily by stem, then by pos
sorted_keys = sorted(stems_data.keys())

print(f"Writing {len(stems_data)} entries to root.csv...")
with open(output_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["stem", "pos", "description"])
    for stem, pos in sorted_keys:
        desc = stems_data[(stem, pos)]
        writer.writerow([stem, pos, desc])

print(f"Done! root.csv saved with {len(stems_data)} entries")
