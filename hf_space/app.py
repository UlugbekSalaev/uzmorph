import gradio as gr
import json
from uzmorph import UzMorph

# Initialize analyzer once at startup
import uzmorph
analyzer = UzMorph()
VERSION = getattr(uzmorph, "__version__", "1.1.7")
print(f"UzMorph Version: {VERSION}")

# POS filter options
POS_OPTIONS = ["Barchasi"] + [
    f"{code}: {desc}" for code, desc in analyzer.POS.DESCRIPTIONS.items()
]

FEATURE_COLUMNS = analyzer.get_features_list()

def analyze_word(word, pos_selection):
    if not word or not word.strip():
        return "Iltimos, so'z kiriting.", ""

    word = word.strip().lower()

    # Extract POS filter
    pos_filter = None
    if pos_selection and pos_selection != "Barchasi":
        pos_filter = pos_selection.split(":")[0].strip()

    results = analyzer.analyze(word, pos_filter=pos_filter)

    if not results:
        return "Natija topilmadi.", ""

    # Build markdown output
    md = f"## Natijalar: `{word}`\n"
    md += f"Topilgan variantlar soni: **{len(results)}**\n\n"

    for i, r in enumerate(results, 1):
        star = " (eng yaxshi)" if i == 1 else ""
        md += f"### Variant #{i}{star}\n"
        md += "| Maydon | Qiymat |\n|:---|:---|\n"
        md += f"| **So'z** | `{r.get('word', '')}` |\n"
        md += f"| **Stem (O'zak)** | `{r.get('stem', '')}` |\n"
        md += f"| **Lemma** | `{r.get('lemma', '')}` |\n"
        md += f"| **POS** | `{r.get('pos', '')}` |\n"

        if r.get('cse'):
            md += f"| **Suffix (CSE)** | `{r['cse']}` |\n"
        if r.get('cse_formula'):
            md += f"| **CSE Formula** | `{r['cse_formula']}` |\n"

        # Morphological features
        features = []
        skip = {'word', 'stem', 'lemma', 'pos', 'cse', 'cse_formula', 'note', 'ball'}
        for k, v in r.items():
            if k in skip or not v:
                continue
            features.append(f"| {k} | `{v}` |")

        if features:
            md += "\n**Morfologik xususiyatlar:**\n\n"
            md += "| Xususiyat | Qiymat |\n|:---|:---|\n"
            md += "\n".join(features) + "\n"

        if r.get('note'):
            md += f"\n*Izoh: {r['note']}*\n"
        md += "\n---\n"

    # JSON output
    json_out = json.dumps(results, ensure_ascii=False, indent=2)
    return md, json_out


def get_pos_info():
    return analyzer.get_pos_list()

def get_features_info():
    return ", ".join(FEATURE_COLUMNS)


# ── Theme ──
custom_theme = gr.themes.Base(
    primary_hue="teal",
    secondary_hue="slate",
    neutral_hue="slate",
    font=gr.themes.GoogleFont("Inter"),
    font_mono=gr.themes.GoogleFont("JetBrains Mono"),
)

with gr.Blocks(
    title="UzMorph — Rule-Based Uzbek Morphological Analyzer",
    theme=custom_theme,
    css="""
        .gradio-container { max-width: 1000px; margin: auto; }
        footer { display: none !important; }
    """
) as demo:
    gr.Markdown(
        f"# UzMorph — Rule-Based Uzbek Morphological Analyzer (v{VERSION})\n"
        "O'zbek tilidagi so'zlarni CSE (Complete Set of Endings) qoidalari asosida morfologik tahlil qilish.  \n"
        'Based on: <a href="https://www.scopus.com/pages/publications/85212084325" target="_blank">Scientific Article (Scopus)</a>  \n'
        'Web: <a href="https://morph.uz" target="_blank">morph.uz</a> | '
        'Neural models: <a href="https://huggingface.co/spaces/UlugbekSalaev/UzMorph_NN" target="_blank">UzMorph_NN (HF Space)</a>\n'
    )

    with gr.Tabs():
        # ── Tab 1: Analyzer ──
        with gr.TabItem("Tahlil qilish"):
            with gr.Row():
                with gr.Column(scale=1):
                    word_input = gr.Textbox(
                        label="So'zni kiriting",
                        placeholder="maktabimizda",
                        lines=1
                    )
                    pos_filter = gr.Dropdown(
                        choices=POS_OPTIONS,
                        value="Barchasi",
                        label="POS filtri (ixtiyoriy)"
                    )
                    analyze_btn = gr.Button("Tahlil qilish", variant="primary")

                with gr.Column(scale=2):
                    result_md = gr.Markdown(label="Natijalar")

            with gr.Accordion("JSON natija", open=False):
                result_json = gr.Code(label="JSON", language="json")

            analyze_btn.click(
                fn=analyze_word,
                inputs=[word_input, pos_filter],
                outputs=[result_md, result_json]
            )
            word_input.submit(
                fn=analyze_word,
                inputs=[word_input, pos_filter],
                outputs=[result_md, result_json]
            )

        # ── Tab 2: POS Tags Reference ──
        with gr.TabItem("POS teglar ro'yxati"):
            gr.Markdown("## Mavjud POS (so'z turkumi) teglari\n")
            gr.Markdown(
                "| Kod | Tavsif |\n|:---|:---|\n" +
                "\n".join([
                    f"| `{code}` | {desc} |"
                    for code, desc in analyzer.POS.DESCRIPTIONS.items()
                ])
            )

        # ── Tab 3: Features Reference ──
        with gr.TabItem("Morfologik xususiyatlar"):
            gr.Markdown(
                "## Natijada chiqishi mumkin bo'lgan barcha maydonlar\n\n"
                "| # | Maydon nomi | Tavsif |\n|:--|:---|:---|\n"
                "| 1 | `word` | Kiritilgan so'z |\n"
                "| 2 | `stem` | O'zak (asosiy qism) |\n"
                "| 3 | `lemma` | Lug'aviy shakl |\n"
                "| 4 | `pos` | So'z turkumi (POS) |\n"
                "| 5 | `cse` | Qo'shimcha (suffix) |\n"
                "| 6 | `cse_formula` | CSE qoidasi formulasi |\n"
                "| 7 | `tense` | Zamon (Past, Present, Future) |\n"
                "| 8 | `person` | Shaxs (1, 2, 3) |\n"
                "| 9 | `possession` | Egalik (1, 2, 3) |\n"
                "| 10 | `cases` | Kelishik (Nominative, Genitive, Dative, Accusative, Locative, Ablative) |\n"
                "| 11 | `verb_voice1` | Fe'l nisbati (Active, Passive, Causative, Reflexive, Reciprocal) |\n"
                "| 12 | `verb_voice2` | Ikkinchi nisbat |\n"
                "| 13 | `verb_func` | Fe'l shakli (Finite, Infinitive, Participle, Adverbial) |\n"
                "| 14 | `impulsion` | Mayl (Imperative, Conditional, Message, Proposal) |\n"
                "| 15 | `degree` | Daraja (Comparative, Positive) |\n"
                "| 16 | `singular` | Birlik (1 = ha) |\n"
                "| 17 | `plural` | Ko'plik (1 = ha) |\n"
                "| 18 | `question` | So'roq (1 = ha) |\n"
                "| 19 | `negative` | Inkor (1 = ha) |\n"
                "| 20 | `polite` | Hurmat (1 = ha) |\n"
                "| 21 | `copula` | Bog'lama (1 = ha) |\n"
            )

        # ── Tab 4: Usage ──
        with gr.TabItem("Foydalanish"):
            gr.Markdown(
                "## pip orqali o'rnatish\n"
                "```bash\n"
                "pip install uzmorph\n"
                "```\n\n"
                "## Python dan foydalanish\n"
                "```python\n"
                "from uzmorph import UzMorph\n\n"
                "analyzer = UzMorph()\n"
                "results = analyzer.analyze('maktabimizda')\n"
                "analyzer.print_result(results)\n"
                "```\n\n"
                "## POS filter bilan\n"
                "```python\n"
                "# Faqat NOUN natijalarini olish\n"
                "results = analyzer.analyze('olma', pos_filter='NOUN')\n"
                "```\n\n"
                "## JSON natija\n"
                "```python\n"
                "import json\n"
                "results = analyzer.analyze('kitobim')\n"
                "print(json.dumps(results, ensure_ascii=False, indent=2))\n"
                "```\n\n"
                "## Mavjud metodlar\n"
                "| Metod | Tavsif |\n|:---|:---|\n"
                "| `analyze(word, pos_filter=None)` | So'zni tahlil qiladi, natijani list of dict qaytaradi |\n"
                "| `print_result(results)` | Natijani konsolda chop etadi |\n"
                "| `get_pos_list()` | Barcha POS teglar ro'yxatini qaytaradi |\n"
                "| `get_features_list()` | Barcha maydonlar ro'yxatini qaytaradi |\n"
            )

    gr.Markdown(
        "---\n"
        "**Muallif**: Ulugbek Salaev  \n"
        '<a href="https://morph.uz" target="_blank">morph.uz</a> | '
        '<a href="https://scholar.google.com/citations?user=-YxQf8AAAAAJ" target="_blank">Google Scholar</a> | '
        '<a href="https://www.researchgate.net/profile/Ulugbek-Salaev" target="_blank">ResearchGate</a> | '
        '<a href="https://www.scopus.com/authid/detail.uri?authorId=57702541100" target="_blank">Scopus</a> | '
        '<a href="https://www.webofscience.com/wos/author/record/IAP-0431-2023" target="_blank">Web of Science</a> | '
        '<a href="https://orcid.org/0000-0003-3020-7099" target="_blank">ORCID</a>\n'
    )

if __name__ == "__main__":
    demo.launch()
