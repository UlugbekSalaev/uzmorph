import csv
import sys
import os
import time
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from uzmorph import UzMorph

def evaluate_accuracy(limit=1000):
    analyzer = UzMorph()
    dataset_path = os.path.join(PROJECT_ROOT, "uzbek_pos_dataset_clean.csv")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset not found: {dataset_path}")
        return

    # Load and group dataset
    print(f"Loading and grouping dataset...")
    word_to_pos = defaultdict(set)
    with open(dataset_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            w = (row.get("word") or "").strip().lower()
            p = (row.get("pos") or "").strip().upper()
            if w and p:
                word_to_pos[w].add(p)

    correct_coverage = 0
    total = 0
    mismatches = []
    
    test_words = sorted(list(word_to_pos.keys()))[:limit]
    
    print(f"Starting accuracy evaluation (Testing {len(test_words)} unique words)...")
    start_time = time.time()

    for word in test_words:
        expected_pos_set = word_to_pos[word]
        results = analyzer.analyze(word)
        
        if not results:
            mismatches.append((word, expected_pos_set, ["NONE"]))
            total += 1
            continue

        found_pos_set = set(r["pos"] for r in results if r.get("pos"))
        
        # Coverage: Did the analyzer find at least one of the possible POS tags?
        # Actually, in a high-quality analyzer, all expected POS should be found.
        # But here we check if the analyzer's primary results overlap with truth.
        
        has_match = any(p in found_pos_set for p in expected_pos_set)
        
        if has_match:
            correct_coverage += 1
        else:
            mismatches.append((word, expected_pos_set, list(found_pos_set)))
        
        total += 1
        if total % 500 == 0:
            print(f"  Processed {total} unique words...")

    end_time = time.time()
    duration = end_time - start_time
    
    accuracy = (correct_coverage / total) * 100 if total > 0 else 0
    
    print("\n" + "="*50)
    print(f" EVALUATION RESULTS (Sample Size: {total} unique words)")
    print("="*50)
    print(f" Word Coverage Accuracy: {accuracy:.2f}%")
    print(f" Total Time:             {duration:.2f} seconds")
    print(f" Avg Time per word:      {(duration/total)*1000:.2f} ms")
    print("="*50)
    print(" Note: Coverage Accuracy means the analyzer successfully identified")
    print(" at least one of the valid POS tags for the word.")
    print("="*50)
    
    if mismatches:
        print("\nSAMPLE MISMATCHES (First 5):")
        for w, exp, found in mismatches[:5]:
            print(f"  Word: '{w}' | Expected: {exp} | Found: {found}")

if __name__ == "__main__":
    # Test on 20,000 unique words for a robust metric
    evaluate_accuracy(limit=20000)
