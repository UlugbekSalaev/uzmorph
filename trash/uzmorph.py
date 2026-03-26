"""
uzmorph — O'zbek tili morfologik analizatori (Rule-Based + Lexicon)
"""

import csv
import re
import os
import sys

# ============================================================
#  1. MA'LUMOTLARNI YUKLASH
# ============================================================

def faylni_ochish(data_path, fayl_nomi):
    return os.path.join(data_path, fayl_nomi)

def root_lexicon_yuklash(data_path):
    lug = {}
    yo_l = faylni_ochish(data_path, "root.csv")
    if not os.path.exists(yo_l):
        return lug
    with open(yo_l, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for qator in reader:
            stem = (qator.get("stem") or "").strip().lower()
            pos = (qator.get("pos") or "").strip()
            if stem:
                lug[stem] = pos
    return lug

def non_affixed_yuklash(data_path):
    lug = {}
    yo_l = faylni_ochish(data_path, "non_affixed_stems.csv")
    if not os.path.exists(yo_l):
        return lug
    with open(yo_l, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for qator in reader:
            soz = (qator.get("stem") or "").strip().lower()
            turkum = (qator.get("pos") or "").strip()
            if soz:
                lug[soz] = turkum
    return lug

def exception_stems_yuklash(data_path):
    lug = {}
    yo_l = faylni_ochish(data_path, "exception_stems.csv")
    if not os.path.exists(yo_l):
        return lug
    with open(yo_l, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for qator in reader:
            stem = (qator.get("stem") or "").strip().lower()
            pos = (qator.get("pos") or "").strip()
            if stem:
                lug[stem] = pos
    return lug

def lemma_map_yuklash(data_path):
    roʻyxat = []
    yo_l = faylni_ochish(data_path, "lemma_map.csv")
    if not os.path.exists(yo_l):
        return roʻyxat
    with open(yo_l, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for qator in reader:
            word = (qator.get("word") or "").strip().lower()
            lemma = (qator.get("lemma") or "").strip().lower()
            affix = (qator.get("affix") or "").strip().lower()
            if word and lemma:
                roʻyxat.append((word, lemma, affix))
    roʻyxat.sort(key=lambda x: len(x[0]), reverse=True)
    return roʻyxat

def number_stems_yuklash(data_path):
    sonlar = set()
    yo_l = faylni_ochish(data_path, "number_stems.csv")
    if not os.path.exists(yo_l):
        return sonlar
    with open(yo_l, "r", encoding="utf-8") as f:
        for qator in f:
            s = qator.strip().lower()
            if s:
                sonlar.add(s)
    return sonlar

def small_stems_yuklash(data_path):
    kichik = set()
    yo_l = faylni_ochish(data_path, "small_stems.csv")
    if not os.path.exists(yo_l):
        return kichik
    with open(yo_l, "r", encoding="utf-8") as f:
        for qator in f:
            s = qator.strip().lower()
            if s:
                kichik.add(s)
    return kichik

def cse_yuklash(data_path):
    qoidalar = []
    yo_l = faylni_ochish(data_path, "cse.csv")
    if not os.path.exists(yo_l):
        return qoidalar
    with open(yo_l, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for qator in reader:
            qoidalar.append(qator)
    return qoidalar

# ============================================================
#  2. CSE FORMULASINI YOYISH
# ============================================================

def cse_yoyish(formula):
    formula = formula.replace("-", "")
    qismlar = re.split(r'(\(.*?\))', formula)
    natijalar = [""]
    for qism in qismlar:
        if not qism: continue
        if qism.startswith("(") and qism.endswith(")"):
            belgi = qism[1:-1]
            yangi_natijalar = []
            for oldingi in natijalar:
                if belgi == "S":
                    for buf in ["s", "y", "n"]: yangi_natijalar.append(oldingi + buf)
                elif belgi == "G":
                    for buf in ["g", "k", "q"]: yangi_natijalar.append(oldingi + buf)
                elif belgi == "T":
                    for buf in ["t", "d"]: yangi_natijalar.append(oldingi + buf)
                else:
                    yangi_natijalar.append(oldingi + belgi.lower())
                yangi_natijalar.append(oldingi)
            natijalar = yangi_natijalar
        else:
            natijalar = [n + qism.lower() for n in natijalar]
    return list(set(n for n in natijalar if n))

def allomorf_xaritasini_qurish(cse_qoidalar):
    xarita = {}
    for idx, qoida in enumerate(cse_qoidalar):
        formula = (qoida.get("affix") or "").strip()
        if not formula: continue
        allomorflar = cse_yoyish(formula)
        for allo in allomorflar:
            if allo not in xarita: xarita[allo] = []
            xarita[allo].append(idx)
    return xarita

# ============================================================
#  4. NATIJANI FORMATLASH
# ============================================================

XUSUSIYAT_USTUNLARI = [
    "pos", "tense", "person", "possession", "cases",
    "verb_voice1", "verb_voice2", "verb_voice3", "verb_func",
    "impulsion", "degree", "copula",
    "singular", "plural", "question", "negative", "polite",
    "lexical_affixes", "syntactical_affixes"
]
BOOLEAN_USTUNLAR = {"singular", "plural", "question", "negative", "polite", "copula"}

def xususiyatlar_chiqarish(qoida):
    natija = {}
    for ustun in XUSUSIYAT_USTUNLARI:
        qiymat = (qoida.get(ustun) or "").strip()
        if qiymat:
            natija[ustun] = qiymat
    return natija

def natija_chop_etish(soz, tahlillar):
    """(Legacy) Wrapper function to maintain backward compatibility."""
    temp_analyzer = UzMorph()
    temp_analyzer.print_result(tahlillar)

# ============================================================
#  5. ASOSIY TAHLIL ALGORITMI
# ============================================================

class PosTags:
    NOUN = "NOUN"
    VERB = "VERB"
    ADJ = "ADJ"
    NUM = "NUM"
    ADV = "ADV"
    PRN = "PRN"
    CNJ = "CNJ"
    ADP = "ADP"
    PRT = "PRT"
    INTJ = "INTJ"
    MOD = "MOD"
    IMIT = "IMIT"
    AUX = "AUX"
    PPN = "PPN"
    PUNC = "PUNC"
    SYM = "SYM"

    # Izohlar lug'ati
    DESCRIPTIONS = {
        "NOUN": "Noun {Ot}",
        "VERB": "Verb {Fe'l}",
        "ADJ": "Adjective {Sifat}",
        "NUM": "Numeric {Son}",
        "ADV": "Adverb {Ravish}",
        "PRN": "Pronoun {Olmosh}",
        "CNJ": "Conjunction {Bog'lovchi}",
        "ADP": "Adposition {Ko'makchi}",
        "PRT": "Particle {Yuklama}",
        "INTJ": "Interjection {Undov}",
        "MOD": "Modal {Modal}",
        "IMIT": "Imitation {Taqlid}",
        "AUX": "Auxiliary verb {Yordamchi fe'l}",
        "PPN": "Proper noun {Atoqli ot}",
        "PUNC": "Punctuation {Tinish belgi}",
        "SYM": "Symbol {Belgi}"
    }

class UzMorph:
    POS = PosTags

    def __init__(self, data_path=None):
        if data_path is None:
            # Get the directory where this script is located
            data_path = os.path.dirname(os.path.abspath(__file__))
            
        self.root_lexicon    = root_lexicon_yuklash(data_path)
        self.non_affixed     = non_affixed_yuklash(data_path)
        self.exception_stems = exception_stems_yuklash(data_path)
        self.lemma_map       = lemma_map_yuklash(data_path)
        self.number_stems    = number_stems_yuklash(data_path)
        self.small_stems     = small_stems_yuklash(data_path)
        self.cse_qoidalar    = cse_yuklash(data_path)
        self.allomorf_xarita = allomorf_xaritasini_qurish(self.cse_qoidalar)
        self.tartiblangan_allomorflar = sorted(self.allomorf_xarita.keys(), key=len, reverse=True)

    def get_pos_list(self):
        """Mavjud barcha POS (turkum) teglar va ularning izohlarini qator ko'rinishida qaytaradi."""
        return "\n".join([f"{code}: {desc}" for code, desc in self.POS.DESCRIPTIONS.items()])

    def get_features_list(self):
        """Natijada chiqishi mumkin bo'lgan barcha maydonlar (taglar) ro'yxatini qaytaradi."""
        return ["word", "stem", "lemma", "cse", "cse_formula"] + XUSUSIYAT_USTUNLARI + ["note", "ball"]

    def print_result(self, results):
        """Prints analysis results to the console in a human-readable format."""
        if not results:
            print(f"\n{'='*50}\n  No results to display.\n{'='*50}")
            return
            
        word = results[0].get('word', 'Unknown')
        print(f"\n{'='*50}\n  WORD:  {word.upper()}\n{'='*50}")
        
        for i, t in enumerate(results, 1):
            star = "★" if i == 1 else " "
            print(f"\n{star} Result #{i}:")
            # ... qolgan qismi o'zgarishsiz qoladi, lekin biz tahlilni davom ettiramiz
            print(f"  ├─ Word:            {t.get('word')}")
            print(f"  ├─ Stem:            {t.get('stem')}")
            print(f"  ├─ Lemma:           {t.get('lemma')}")
            
            if t.get("pos"):
                print(f"  ├─ POS Tag:         {t['pos']}")
                
            if t.get("cse"): print(f"  ├─ Suffix (cse):    {t['cse']}")
            if t.get("cse_formula"): print(f"  ├─ CSE Formula:     {t['cse_formula']}")
            if t.get("note"): print(f"  ├─ Note:            {t['note']}")
            
            # Print all available morphological features
            available_features = []
            for k in XUSUSIYAT_USTUNLARI:
                if k == "pos": continue
                if t.get(k):
                    available_features.append(k)
            
            for idx, k in enumerate(available_features):
                v = t.get(k)
                marker = "└─" if idx == len(available_features) - 1 else "├─"
                
                if k in BOOLEAN_USTUNLAR and v == "1":
                    print(f"  {marker} {k:<15} ✓")
                else:
                    print(f"  {marker} {k:<15} {v}")

            if not available_features:
                print(f"  └─ (no additional morphological features)")
        print(f"{'─'*50}")

    def analyze(self, word, pos_filter=None):
        """
        So'zni morfologik tahlil qiladi.
        Faqat bitta so'z (token) qabul qiladi.
        Natijani list of dict formatida qaytaradi (JSON formatiga mos).
        """
        word = word.lower().strip()
        results = []

        # 1. Lexicon check
        if word in self.root_lexicon:
            word_pos = self.root_lexicon[word]
            if not pos_filter or word_pos == pos_filter:
                res = {
                    "word": word, "stem": word, "lemma": word,
                    "cse": None, "cse_formula": None
                }
                res.update({k: "" for k in XUSUSIYAT_USTUNLARI})
                res["pos"] = word_pos
                res["note"] = "Lug'atdan topildi"
                res["ball"] = 300
                results.append(res)

        # 2. Non-affixed check
        if word in self.non_affixed:
            word_pos = self.non_affixed[word]
            if not pos_filter or word_pos == pos_filter:
                res = {
                    "word": word, "stem": word, "lemma": word,
                    "cse": None, "cse_formula": None
                }
                res.update({k: "" for k in XUSUSIYAT_USTUNLARI})
                res["pos"] = word_pos
                res["note"] = "Non-affixed"
                res["ball"] = 200
                results.append(res)

        # 3. Lemma map check
        results.extend(self._lemma_map_check(word, pos_filter))

        # 4. CSE stripping
        results.extend(self._cse_stripping(word, pos_filter))

        # Default fallback (always return at least one result)
        if not results:
            res = {
                "word": word, "stem": word, "lemma": word,
                "cse": None, "cse_formula": None
            }
            res.update({k: "" for k in XUSUSIYAT_USTUNLARI})
            res["pos"] = "UNKNOWN"
            res["note"] = "Fallback"
            res["ball"] = 0
            results.append(res)

        # Process results
        unique_results = self._process_results(results)
        
        return unique_results

    def _lemma_map_check(self, soz, pos_filter=None):
        results = []
        for (word, lemma, affix) in self.lemma_map:
            if not soz.startswith(word): continue
            qoldiq = soz[len(word):]
            toliq_cse = affix + qoldiq
            if not toliq_cse:
                lemma_pos = self.root_lexicon.get(lemma, "NOUN")
                if not pos_filter or lemma_pos == pos_filter:
                    res = {
                        "word": soz, "stem": lemma, "lemma": lemma,
                        "cse": None, "cse_formula": None
                    }
                    res.update({k: "" for k in XUSUSIYAT_USTUNLARI})
                    res["pos"] = lemma_pos
                    res["note"] = f"Lemma map: {word}"
                    res["ball"] = 150
                    results.append(res)
                continue
            if toliq_cse in self.allomorf_xarita:
                for qoida_idx in self.allomorf_xarita[toliq_cse]:
                    qoida = self.cse_qoidalar[qoida_idx]
                    qoida_pos = (qoida.get("pos") or "").strip()
                    if pos_filter and qoida_pos != pos_filter:
                        continue
                    res = {
                        "word": soz, "stem": lemma, "lemma": lemma,
                        "cse": toliq_cse, "cse_formula": (qoida.get("affix") or "").strip()
                    }
                    res.update({k: "" for k in XUSUSIYAT_USTUNLARI})
                    res.update(xususiyatlar_chiqarish(qoida))
                    res["note"] = f"Lemma map: {word}"
                    res["ball"] = 150 + len(toliq_cse)
                    results.append(res)
        return results

    def _cse_stripping(self, soz, pos_filter=None):
        results = []
        UNLILAR = set("aeiouo’u’")
        for allomorf in self.tartiblangan_allomorflar:
            if not soz.endswith(allomorf): continue
            stem = soz[:-len(allomorf)]
            if not stem: continue
            
            if len(stem) <= 2:
                if stem not in self.small_stems and stem not in self.root_lexicon: continue
            if len(stem) > 2:
                if not any(c in UNLILAR for c in stem) and stem not in self.root_lexicon: continue

            istisno = stem in self.exception_stems
            lugatda = stem in self.root_lexicon

            for qoida_idx in self.allomorf_xarita[allomorf]:
                qoida = self.cse_qoidalar[qoida_idx]
                qoida_pos = (qoida.get("pos") or "").strip()
                
                if pos_filter and qoida_pos != pos_filter:
                    continue

                if qoida_pos == "NUM" and stem not in self.number_stems and not lugatda: continue

                ball = len(allomorf) * 2
                if lugatda: ball += 100
                elif istisno: ball += 30
                
                res = {
                    "word": soz, "stem": stem, "lemma": stem, "cse": allomorf,
                    "cse_formula": (qoida.get("affix") or "").strip()
                }
                res.update({k: "" for k in XUSUSIYAT_USTUNLARI})
                res.update(xususiyatlar_chiqarish(qoida))
                res["note"] = None
                res["ball"] = ball
                results.append(res)
        return results

    def _process_results(self, results):
        seen = set()
        unique = []
        for r in results:
            # Flattened dict unique check using all values
            key = tuple(r.get(k) for k in r.keys() if k != "ball")
            if key not in seen:
                unique.append(r)
                seen.add(key)
        unique.sort(key=lambda x: x.get("ball", 0), reverse=True)
        return unique[:3]
