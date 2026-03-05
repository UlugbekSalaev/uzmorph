# uzmorph

**uzmorph** is a professional morphological analyzer for the Uzbek language based on **CSE (Complete Set of Endings)** rules and comprehensive morphological tagging. It provides deep linguistic analysis by identifying stems, lemmas, and a wide array of annotated morphological features.

## Key Features

- **CSE-Based Analysis:** Employs advanced suffix stripping rules (**Complete Set of Endings**) for precise morphological segmentation.
- **Rich Morphological Tagging:** Extracts detailed features including part-of-speech (POS), tense, person, possession, case, and voice.
- **Flat JSON Output:** Returns analysis results in a developer-friendly, flattened JSON-compatible format.
- **Professional API:** Designed for easy integration with standard English-named methods and formatted terminal output.

## Installation

```bash
pip install uzmorph
```

## Quick Start

```python
from uzmorph import UzMorph

# Initialize the analyzer
analyzer = UzMorph()

# Analyze a word
results = analyzer.analyze("maktabimda")

# Formatted console print
analyzer.print_result(results)
```

## JSON Result Sample

Each analysis result is a dictionary containing the following structure:

```json
[
    {
        "word": "maktabimda",
        "stem": "maktab",
        "lemma": "maktab",
        "cse": "imda",
        "cse_formula": "(i)mda",
        "pos": "NOUN",
        "possession": "1",
        "cases": "Locative",
        "singular": "1",
        "syntactical_affixes": "(i)m da",
        "note": null,
        "ball": 108
    }
]
```

## API Reference

### `UzMorph` Class
- `analyze(word, pos_filter=None)`: Performs morphological analysis and returns a list of results.
- `print_result(results)`: Prints formatted output to the console.
- `get_pos_list()`: Returns a formatted string of all available POS tags.
- `get_features_list()`: Returns a list of all possible property keys in the result.

## License
MIT
