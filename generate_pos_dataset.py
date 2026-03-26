import os
import csv

def compile_dataset():
    source_dir = r"C:\Users\E-MaxPCShop\PycharmProjects\CSE_UzMorph\kaharjan_dataset"
    output_file = r"C:\Users\E-MaxPCShop\PycharmProjects\CSE_UzMorph\uzbek_pos_dataset.csv"
    
    # Mapping of filenames to our 16 exact tags
    pos_mapping = {
        'noun.txt': 'NOUN',
        'verb.txt': 'VERB',
        'adjective.txt': 'ADJ',
        'numeral.txt': 'NUM',
        'adverb.txt': 'ADV',
        'pronoun.txt': 'PRN',
        'conjunction.txt': 'CNJ',
        'particle.txt': 'PRT',
        'interjection.txt': 'INTJ',
        'modal.txt': 'MOD',
        'imitative.txt': 'IMIT',
        'auxiliary.txt': 'AUX',
        # As per user request: "o'tkazib bilmaydiganlaring bulsa NOUN qilib olaver"
        'unknown.txt': 'NOUN'
    }

    dataset = []
    
    for filename, pos_tag in pos_mapping.items():
        filepath = os.path.join(source_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        dataset.append({"word": word, "pos": pos_tag})
    
    # Save the consolidated dataset
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['word', 'pos'])
        writer.writeheader()
        writer.writerows(dataset)
        
    print(f"Successfully compiled {len(dataset)} words into {output_file}")

if __name__ == '__main__':
    compile_dataset()
