import csv
import os

def build_master_dataset():
    clean_kaharjan_csv = r"C:\Users\E-MaxPCShop\PycharmProjects\CSE_UzMorph\uzbek_pos_dataset_clean.csv"
    hunspell_dic = r"C:\Users\E-MaxPCShop\PycharmProjects\CSE_UzMorph\hunspell_dataset\uz-lat.dic"
    output_master_csv = r"C:\Users\E-MaxPCShop\PycharmProjects\CSE_UzMorph\master_uzbek_stem_pos.csv"

    # key: stem, value: set of POS tags
    master_dict = {}

    print("Loading Kaharjan golden dataset...")
    if os.path.exists(clean_kaharjan_csv):
        with open(clean_kaharjan_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['word'].strip().lower()
                pos = row['pos'].strip()
                if word and pos:
                    if word not in master_dict:
                        master_dict[word] = set()
                    master_dict[word].add(pos)

    print(f"Loaded {len(master_dict)} words from Kaharjan.")

    # Process Hunspell DIC
    print("Processing Hunspell database...")
    hunspell_added = 0

    if os.path.exists(hunspell_dic):
        with open(hunspell_dic, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:]: # Skip first line
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('/', 1)
                stem = parts[0].strip().lower()
                flag = parts[1] if len(parts) > 1 else ""

                if not stem:
                    continue
                
                # Infer POS from Hunspell Flags
                inferred_pos = 'VERB' if 'J' in flag else 'NOUN'
                
                if stem not in master_dict:
                    master_dict[stem] = set()
                    hunspell_added += 1
                
                master_dict[stem].add(inferred_pos)

    print(f"Aggregated {len(master_dict)} unique stems in total.")

    # Save to master CSV
    # Since CSV is flat, we write one row per (word, stem, pos)
    print(f"Saving golden master dataset...")
    count = 0
    with open(output_master_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['word', 'stem', 'pos'])
        
        for stem in sorted(master_dict.keys()):
            for pos in sorted(list(master_dict[stem])):
                writer.writerow([stem, stem, pos])
                count += 1
            
    print(f"Done! Saved {count} entries to {output_master_csv}")

if __name__ == "__main__":
    build_master_dataset()
