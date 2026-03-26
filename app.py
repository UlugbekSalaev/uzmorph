import streamlit as st
import pandas as pd
from uzmorph import UzMorph

# Page config
st.set_page_config(
    page_title="UzMorph - Uzbek Morphological Analyzer",
    page_icon="🇺🇿",
    layout="wide"
)

# Initialize Analyzer
@st.cache_resource
def load_analyzer():
    return UzMorph()

analyzer = load_analyzer()

# Title
st.title("🇺🇿 UzMorph: Uzbek Morphological Analyzer")
st.markdown("""
Professional morphological analyzer for the Uzbek language based on **CSE (Complete Set of Endings)** rules and a massive lexicon (~122k stems).
""")

# Sidebar info
st.sidebar.title("About UzMorph")
st.sidebar.info("""
- **Lexicon:** 122,000+ unique stem-POS pairs.
- **Rules:** Complete Set of Endings (CSE) paradigm.
- **Author:** Ulugbek Salaev
""")

# Input Area
st.subheader("Input")
word_input = st.text_input("Enter an Uzbek word to analyze:", "ishladim")

if st.button("Analyze") or word_input:
    results = analyzer.analyze(word_input)
    
    if results:
        st.subheader("Results")
        
        for i, res in enumerate(results):
            with st.expander(f"Analysis #{i+1}: {res.get('pos')} (Score: {res.get('ball')})", expanded=(i==0)):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Core Information**")
                    st.write(f"**Stem:** `{res.get('stem')}`")
                    st.write(f"**Lemma:** `{res.get('lemma')}`")
                    st.write(f"**POS:** `{res.get('pos')}`")
                    st.write(f"**Suffix (CSE):** `{res.get('cse')}`")
                    st.write(f"**CSE Formula:** `{res.get('cse_formula')}`")
                
                with col2:
                    st.write("**Morphological Features**")
                    features = {k: v for k, v in res.items() if v and k not in ['word', 'stem', 'lemma', 'pos', 'cse', 'cse_formula', 'ball', 'note']}
                    if features:
                        st.json(features)
                    else:
                        st.write("No additional features identified.")
        
        # Table view
        st.subheader("Comparison Table")
        df = pd.DataFrame(results)
        # Reorder columns for better view
        main_cols = ['word', 'stem', 'pos', 'ball', 'cse']
        other_cols = [c for c in df.columns if c not in main_cols]
        df = df[main_cols + other_cols]
        st.dataframe(df)
        
    else:
        st.error("No analysis possible for this word.")

# POS List
with st.expander("Supported POS Tag List"):
    pos_data = [
        {"Code": "NOUN", "Description": "Noun (Ot)"},
        {"Code": "VERB", "Description": "Verb (Fe'l)"},
        {"Code": "ADJ", "Description": "Adjective (Sifat)"},
        {"Code": "ADV", "Description": "Adverb (Ravish)"},
        {"Code": "PRN", "Description": "Pronoun (Olmosh)"},
        {"Code": "NUM", "Description": "Numeric (Son)"},
        {"Code": "MOD", "Description": "Modal (Modal)"},
        {"Code": "CNJ", "Description": "Conjunction (Bog'lovchi)"},
        {"Code": "ADP", "Description": "Adposition (Ko'makchi)"},
        {"Code": "PRT", "Description": "Particle (Yuklama)"},
        {"Code": "INTJ", "Description": "Interjection (Undov)"},
        {"Code": "IMIT", "Description": "Imitation (Taqlid)"},
        {"Code": "PPN", "Description": "Proper Noun (Atoqli ot)"},
        {"Code": "AUX", "Description": "Auxiliary verb (Yordamchi fe'l)"},
        {"Code": "PUNC", "Description": "Punctuation"},
    ]
    st.table(pd.DataFrame(pos_data))

st.markdown("---")
st.caption("Developed by Ulugbek Salaev. Powered by UzMorph Engine.")
