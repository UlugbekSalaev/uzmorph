
from uzmorph import UzMorph
analyzer = UzMorph()

# test_words = ['maktabimizda', 'kitobim', 'yozolmadim', 'olma', 'bolalarning']

while True:
    word = input("Enter a word: ")
    results = analyzer.analyze(word)
    analyzer.print_result(results)