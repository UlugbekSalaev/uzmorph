import csv
import re
import os

cyrillic_to_latin = {
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'J',
    'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
    'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'X', 'Ц': 'Ts',
    'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': "'", 'Ы': 'I', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'j',
    'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
    'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'x', 'ц': 'ts',
    'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': "'", 'ы': 'i', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'Ў': "O'", 'ў': "o'", 'Қ': 'Q', 'қ': 'q', 'Ғ': "G'", 'ғ': "g'", 'Ҳ': 'H', 'ҳ': 'h'
}

def transliterate(text):
    for cyr, lat in cyrillic_to_latin.items():
        text = text.replace(cyr, lat)
    return text

def is_valid_uzbek_latin(word):
    # Valid characters: a-z, A-Z, standard apostrophes, and basic hyphens
    # No numbers, no Russian-only characters, no weird symbols
    # We replace common curly apostrophes with standard straight quotes for uniform processing
    word = word.replace('‘', "'").replace('’', "'").replace('`', "'")
    
    # Check if the word strictly contains only valid letters/apostrophe/hyphen
    # And it shouldn't just be an apostrophe
    if not re.match(r"^[a-zA-Z\'-]+$", word) or len(word.strip("'-")) == 0:
        return False, word
    
    return True, word

def process_dataset():
    input_file = r"C:\Users\E-MaxPCShop\PycharmProjects\CSE_UzMorph\uzbek_pos_dataset.csv"
    output_file = r"C:\Users\E-MaxPCShop\PycharmProjects\CSE_UzMorph\uzbek_pos_dataset_clean.csv"
    
    clean_data = []
    dropped_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['word'].strip()
            pos = row['pos']
            
            # Step 1: Detect and Convert Cyrillic to Latin
            latin_word = transliterate(word)
            
            # Step 2: Validate against foreign/unknown structural characters
            is_valid, final_word = is_valid_uzbek_latin(latin_word)
            
            if is_valid:
                # To lowercase for normalization (standard for our models)
                clean_data.append({'word': final_word.lower(), 'pos': pos})
            else:
                dropped_count += 1
                
    # Save the cleaned dataset
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['word', 'pos'])
        writer.writeheader()
        writer.writerows(clean_data)
        
    print(f"Original Words: {len(clean_data) + dropped_count}")
    print(f"Clean, Valid, Latin Words Saved: {len(clean_data)}")
    print(f"Dropped Invalid/Unknown Words: {dropped_count}")

if __name__ == '__main__':
    process_dataset()
