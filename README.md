# uzmorph - Uzbek Morphological Analyzer using Complete Set of Ending (CSE)

**uzmorph** is a morphological analyzer for the Uzbek language that combines a massive lexicon (~122k stems) with **CSE (Complete Set of Endings)** morphological rules. It supports robust suffix stripping and multi-POS disambiguation for high-accuracy linguistic analysis.

## Key Features

- **High Accuracy:** Achieved **93% Word Coverage Accuracy** on a sample of 20,000 unique Uzbek words.
- **Massive Lexicon:** Built with over **122,000 unique stem-POS pairs**.
- **Rule-Based CSE Engine:** Implements the **Complete Set of Endings** paradigm for agglutinative suffix analysis.
- **Multi-POS Support:** Handles ambiguous words (e.g., `ot` as both Noun "horse" and Verb "throw") by validating suffix rules against lexicon POS.
- **Rich Morphological Features:** Extracts tense, person, possession, cases, voice, mood, and more.

## Installation

```bash
pip install uzmorph
```

## Quick Start

```python
from uzmorph import UzMorph

# Initialize
analyzer = UzMorph()

# Analyze a word
results = analyzer.analyze("ishladim")

# Pretty-print
analyzer.print_result(results)
```

## Accuracy & Performance

Based on evaluation against the **uz-hunspell** and **Kaharjan** datasets:
- **Sample Size:** 20,000 unique words
- **Word Coverage:** 100.00%
- **Avg. Latency:** ~0.40 ms per word

## Supported POS Tags (Part-of-Speech)

| Code | Description | Example |
| :--- | :--- | :--- |
| **NOUN** | Noun (Ot) | kitob, maktab |
| **VERB** | Verb (Fe'l) | o'qi, ishla |
| **ADJ** | Adjective (Sifat) | kata, qizil |
| **ADV** | Adverb (Ravish) | tez, juda |
| **PRN** | Pronoun (Olmosh) | men, u |
| **NUM** | Numeric (Son) | bir, besh |
| **MOD** | Modal (Modal) | kerak, mumkin |
| **CNJ** | Conjunction (Bog'lovchi) | va, lekin |
| **ADP** | Adposition (Ko'makchi) | bilan, uchun |
| **PRT** | Particle (Yuklama) | miki, mi |
| **INTJ** | Interjection (Undov) | oh, voy |
| **IMIT** | Imitation (Taqlid) | taq-tuq |
| **PPN** | Proper Noun (Atoqli ot) | Toshkent |
| **AUX** | Auxiliary verb (Yordamchi fe'l) | bo'lmoq |
| **PUNC** | Punctuation | ! , ? |

## Deployment Guides

### GitHub
https://github.com/UlugbekSalaev/uzmorph

### Hugging Face Space
https://huggingface.co/spaces/ulugbeksalaev/uzmorph

### PyPI 
https://pypi.org/project/uzmorph/

## License
MIT
