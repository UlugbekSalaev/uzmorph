"""
VERB (Fe'l) o'zaklaridan -moq qo'shimchasini olib tashlash.
Morfologik analizatorda fe'l o'zagi (stem) -moq dan xoli bo'lishi kerak.
Multi-POS qo'llab-quvvatlaydi.
"""
import csv
import os

INPUT = r"c:\Users\E-MaxPCShop\PycharmProjects\CSE_UzMorph\uzmorph\data\root.csv"
OUTPUT = r"c:\Users\E-MaxPCShop\PycharmProjects\CSE_UzMorph\uzmorph\data\root.csv"

# List to store final rows
final_rows = []
seen_pairs = set()

def process_file():
    count_moq = 0
    with open(INPUT, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stem = (row["stem"] or "").strip().lower()
            pos = (row["pos"] or "").strip()
            desc = (row["description"] or "").strip()
            
            # Agar fe'l bo'lsa va -moq bilan tugasa, -moq ni olib tashlaymiz
            if pos == "VERB" and stem.endswith("moq"):
                stem = stem[:-3]
                count_moq += 1
                desc = "Verb {Fe'l}"
            
            if not stem:
                continue
                
            # Deduplicate (stem, pos) pairs just in case
            if (stem, pos) not in seen_pairs:
                final_rows.append({"stem": stem, "pos": pos, "description": desc})
                seen_pairs.add((stem, pos))
                
    return count_moq

moq_removed = process_file()

# Yozish
with open(OUTPUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["stem", "pos", "description"])
    writer.writeheader()
    writer.writerows(final_rows)

print(f"=== Fe'l o'zaklarini tuzatish natijalari ===")
print(f"  -moq qo'shimchasi olib tashlandi: {moq_removed} ta so'zdan")
print(f"  Jami o'zaklar soni:              {len(final_rows)} ta")
print(f"\nroot.csv muvaffaqiyatli yangilandi!")
