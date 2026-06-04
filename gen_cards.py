#!/usr/bin/env python3
"""Generate Obsidian sentence cards from WK24.xlsx without external APIs."""

import os
import re
import openpyxl

EXCEL_PATH = "/home/user/48wk_spanish/WK24.xlsx"
OUTPUT_DIR = "/home/user/48wk_spanish/output3"
WEEK_DIR = "M6-W24"

# ── helpers ──────────────────────────────────────────────────────────────────

STOPWORDS = {
    "el","la","los","las","un","una","unos","unas",
    "de","del","en","a","al","con","por","para","sin","sobre",
    "que","si","no","ya","muy","más","se","le","lo","les","me","te",
    "su","sus","mi","mis","tu","tus","es","son","ha","han","hay",
    "esto","eso","esto","esta","estos","estas",
    "y","o","pero","sino","porque","cuando","donde","como",
    "ser","estar","haber","tener",  # auxiliary-ish; keep content verbs
}

def extract_content_words(spanish: str) -> list[str]:
    """Return unique content words (nouns/verbs in base-like form) from Spanish text."""
    # strip punctuation
    text = re.sub(r"[¿?¡!,;:\"'«»\(\)]", " ", spanish)
    tokens = text.split()
    seen = set()
    result = []
    for t in tokens:
        w = t.lower().strip(".,;:")
        if len(w) < 3:
            continue
        if w in STOPWORDS:
            continue
        if w not in seen:
            seen.add(w)
            result.append(w)
    # Keep max ~8 words
    return result[:8]


# ── per-row analysis ──────────────────────────────────────────────────────────

def analyze(tipo: str, num: str, es: str, zh: str, grammar: str) -> str:
    """Build the full card markdown for one row."""
    new_id = num.replace("M24-", "M6-W24-")

    phrases = [p.strip() for p in grammar.split("/")]
    content_words = extract_content_words(es)

    breakdown_lines = build_breakdown(tipo, es, zh, grammar, phrases)
    words_str = " ".join(f"[[{w}]]" for w in content_words)

    lines = [
        f"{tipo} | {new_id}",
        "",
        f"ES：{es}",
        f"ZH：{zh}",
        f"核心語法：{grammar}",
        "拆解：",
    ]
    lines += breakdown_lines
    lines.append(f"核心單字：{words_str}")
    return "\n".join(lines)


def build_breakdown(tipo: str, es: str, zh: str, grammar: str, phrases: list[str]) -> list[str]:
    """Generate breakdown bullet points."""
    lines = []

    # ── 1. 句型結構 ──
    struct = detect_structure(tipo, es)
    lines.append(f"【句型結構】{struct}")

    # ── 2. 片語拆解 ──
    for ph in phrases:
        lines.append(f"【片語拆解】{phrase_explanation(ph, es)}")

    # ── 3. 語法細節（conditional / subjunctive / special tense） ──
    detail = detect_grammar_detail(es, grammar)
    if detail:
        lines.append(f"【語法細節】{detail}")

    return lines


# ── structure detection ───────────────────────────────────────────────────────

def detect_structure(tipo: str, es: str) -> str:
    es_lower = es.lower()

    if es.startswith("¿"):
        # Question type
        if " si " in es_lower:
            return "主句為疑問句（¿Por qué / ¿A quién 等引導），後接 si 條件從句，形成「為何還要...如果已經...」的對比疑問結構；疑問句中動詞通常先於主詞（倒裝語序）。"
        if " que " in es_lower and ("cree" in es_lower or "opina" in es_lower or "piensa" in es_lower):
            return "主句為疑問句，後接 que 引導的名詞子句，詢問對某事的看法或意見。"
        if " cuando " in es_lower:
            return "主句為疑問句，包含 cuando 引導的時間副詞子句，說明動作發生的時間背景。"
        return "主句為疑問句，以疑問詞（¿Quién / ¿Qué / ¿Cómo / ¿Cuándo 等）引導，動詞先於主詞為正常倒裝語序。"

    if es.startswith("Si ") or es.startswith("si "):
        if "ara " in es_lower or "iera " in es_lower or "ase " in es_lower:
            return "全句為條件句結構：si + 虛擬式過去未完成時（條件從句），主句接條件式（condicional），表達與現實相反或假設性的情境（虛擬語氣第二類條件句）。"
        return "全句為條件句結構：si + 直陳式（條件從句），主句以直陳式或命令式回應，表達真實或可能發生的條件（第一類條件句）。"

    if "que" in es_lower and ("subjuntivo" in grammar.lower() or "subj" in grammar.lower()):
        return "主句為陳述句，後接 que 引導的名詞子句；主句動詞表達意願、情緒或評價，觸發子句使用虛擬式（Subjuntivo），為標準虛擬式結構。"

    if es.startswith("¡") or es.endswith("!"):
        return "全句為感嘆句或強調陳述，語氣強烈；若含 que + 動詞子句，則為「¡主句 + que 子句！」的強調結構。"

    # Identify compound sentences
    if "; " in es:
        return "全句由分號分隔兩個並列主句，前句提出情境或條件，後句表達結論或對比，形成遞進或因果關係的複合句結構。"

    if ", " in es and ("porque" in es_lower or "para" in es_lower or "aunque" in es_lower):
        return "主句為陳述句，後接副詞子句（porque / para / aunque 等引導），說明原因、目的或讓步關係，構成主從複合句。"

    if "en lugar de" in es_lower or "en vez de" in es_lower:
        return "主句為陳述句，後接「en lugar de / en vez de + 不定詞」表達對比或替代關係，意為「而不是做...」，強調行為的選擇取向。"

    return "主句為直陳式陳述句，敘述主詞的行為或狀態；若含從句，則為主從複合句結構，前句為主要訊息，後句補充細節或原因。"


# ── phrase explanation ────────────────────────────────────────────────────────

# Pre-built explanations for common verb+prep patterns
PHRASE_DB = {
    "insistir en": "動詞 insistir 後固定接介詞 en，再加不定詞或名詞，表示堅持要做某事或堅持某立場。",
    "confiar en": "動詞 confiar 後接介詞 en，表示信任某人或某事物。",
    "enterarse de": "動詞 enterarse（反身）後接介詞 de，表示得知、獲悉某件事。",
    "sufrir por": "動詞 sufrir 後接介詞 por，表示因某事而受苦或遭受痛苦。",
    "arriesgarse a": "動詞 arriesgar 以反身形式使用，後接介詞 a 加不定詞，表示冒險去做某事。",
    "olvidarse de": "動詞 olvidar 以反身形式使用，後接介詞 de 加不定詞或名詞，表示忘記做某事。",
    "advertir de": "動詞 advertir 後接介詞 de，表示警告某人注意某事或告知某情況。",
    "carecer de": "動詞 carecer 後接介詞 de，表示缺乏某物或缺少某種特質，為書面語常用詞。",
    "oponerse a": "動詞 oponer 以反身形式使用，後接介詞 a，表示反對某人、某事或某提案。",
    "negarse a": "動詞 negar 以反身形式使用，後接介詞 a 加不定詞，表示拒絕做某事。",
    "atentar contra": "動詞 atentar 後接介詞 contra，表示侵犯、危害或攻擊某權益或某人。",
    "preocuparse por": "動詞 preocupar 以反身形式使用，後接介詞 por，表示擔心或重視某事。",
    "centrarse en": "動詞 centrar 以反身形式使用，後接介詞 en，表示專注於或集中注意力在某事上。",
    "depender de": "動詞 depender 後接介詞 de，表示依賴或取決於某人或某事物。",
    "tardar en": "動詞 tardar 後接介詞 en 加不定詞，表示花費時間去做某事，含「遲早」的語氣。",
    "recurrir a": "動詞 recurrir 後接介詞 a，表示求助於某人或訴諸某種方式、資源。",
    "contribuir a": "動詞 contribuir 後接介詞 a 加不定詞或名詞，表示對某事做出貢獻或有助於某目標。",
    "quejarse de": "動詞 quejar 以反身形式使用，後接介詞 de，表示抱怨某事或對某事感到不滿。",
    "acostumbrarse a": "動詞 acostumbrar 以反身形式使用，後接介詞 a 加不定詞，表示習慣於做某事。",
    "comprometerse a": "動詞 comprometer 以反身形式使用，後接介詞 a 加不定詞，表示承諾去做某事。",
    "renunciar a": "動詞 renunciar 後接介詞 a，表示放棄某事物或辭去某職位。",
    "aspirar a": "動詞 aspirar 後接介詞 a 加不定詞或名詞，表示渴望、立志達到某目標。",
    "atreverse a": "動詞 atrever 以反身形式使用，後接介詞 a 加不定詞，表示敢於去做某事。",
    "esforzarse por": "動詞 esforzar 以反身形式使用，後接介詞 por 加不定詞，表示努力去做某事。",
    "aprovecharse de": "動詞 aprovechar 以反身形式使用，後接介詞 de，表示利用某人或某機會（含負面意涵）。",
    "beneficiarse de": "動詞 beneficiar 以反身形式使用，後接介詞 de，表示從某事中獲益。",
    "alejarse de": "動詞 alejar 以反身形式使用，後接介詞 de，表示遠離某人或某地。",
    "acercarse a": "動詞 acercar 以反身形式使用，後接介詞 a，表示靠近或接近某人、某地或某事。",
    "resistirse a": "動詞 resistir 以反身形式使用，後接介詞 a 加不定詞，表示抗拒去做某事。",
    "negarse a": "動詞 negar 以反身形式使用，後接介詞 a 加不定詞，表示拒絕去做某事。",
    "informarse de": "動詞 informar 以反身形式使用，後接介詞 de，表示了解或獲取關於某事的資訊。",
    "hablar de": "動詞 hablar 後接介詞 de，表示談論或討論某個話題。",
    "tratar de": "動詞 tratar 後接介詞 de 加不定詞，表示試圖或嘗試做某事。",
    "acabar de": "動詞 acabar 後接介詞 de 加不定詞，表示剛剛完成某動作（近過去式用法）。",
    "dejar de": "動詞 dejar 後接介詞 de 加不定詞，表示停止做某事。",
    "tratar de": "動詞 tratar 後接介詞 de 加不定詞，表示嘗試做某事。",
    "encargarse de": "動詞 encargar 以反身形式使用，後接介詞 de，表示負責或承擔某項任務。",
    "darse cuenta de": "片語動詞 darse cuenta 後接介詞 de，表示意識到或察覺某事。",
    "querer": "情態動詞 querer 後直接加不定詞，表示想要或希望做某事，無需介詞。",
    "poder": "情態動詞 poder 後直接加不定詞，表示能夠或有能力做某事。",
    "deber": "情態動詞 deber 後直接加不定詞，表示應當或必須做某事，含義務感。",
    "soler": "情態動詞 soler 後接不定詞，表示習慣上或通常會做某事。",
    "subjuntivo": "本句含有觸發虛擬式（Subjuntivo）的結構，動詞子句中使用虛擬式，表達主觀意願、情緒評價或不確定性。",
    "condicional": "主句動詞使用條件式（Condicional），表達假設情境下可能發生的結果，通常與 si 條件句搭配。",
    "imperativo": "動詞使用命令式（Imperativo），直接對聽者發出指令或請求，為直接命令句型。",
    "futuro": "動詞使用未來式（Futuro），表達將來的動作或預測，也可用於表達語氣較強的推測。",
    "pretérito perfecto": "動詞使用現在完成時（Pretérito Perfecto：haber + 過去分詞），表達與現在有關聯的已完成動作。",
    "pretérito indefinido": "動詞使用簡單過去時（Pretérito Indefinido），表達過去某一特定時間點已完成的動作。",
    "imperfecto": "動詞使用過去未完成時（Imperfecto），描述過去持續的狀態、習慣或背景情境。",
    "pluscuamperfecto": "動詞使用過去完成時（Pluscuamperfecto：había + 過去分詞），表達在另一個過去動作之前已完成的動作。",
    "gerundio": "動詞以現在分詞形式（Gerundio）出現，用於表達進行中的動作或作為副詞修飾主動詞。",
    "pasiva": "句子使用被動態結構（ser + 過去分詞），主詞為動作的承受者，施事者若出現則以 por 引導。",
    "pasiva refleja": "句子使用反身被動結構（se + 第三人稱動詞），為西班牙語常見的非人稱或被動表達方式。",
}

def phrase_explanation(ph: str, es: str) -> str:
    key = ph.lower().strip()
    if key in PHRASE_DB:
        return f"{ph}：{PHRASE_DB[key]}"

    # Fallback: detect pattern
    parts = key.split()
    if len(parts) == 1:
        return f"{ph}：動詞 {ph}，為本句核心動詞，後接相關補語或從句完成句義。"

    verb = parts[0]
    prep = parts[1] if len(parts) > 1 else ""

    prep_meanings = {
        "en": "介詞 en",
        "de": "介詞 de",
        "a": "介詞 a",
        "por": "介詞 por",
        "con": "介詞 con",
        "contra": "介詞 contra",
        "para": "介詞 para",
        "sobre": "介詞 sobre",
    }
    prep_zh = prep_meanings.get(prep, f"介詞 {prep}")

    # Check if reflexive (ends in -se stripped)
    if verb.endswith("se") or "rse" in verb:
        base = verb.replace("rse","r").replace("se","")
        return f"{ph}：動詞 {base} 以反身形式使用，後固定接{prep_zh}加不定詞或名詞，表達主詞對自身行為的主動性或固定介詞搭配。"

    return f"{ph}：動詞 {verb} 後固定接{prep_zh}，形成「{ph}」固定搭配，後可接名詞或不定詞完成句義。"


# ── grammar detail detection ──────────────────────────────────────────────────

def detect_grammar_detail(es: str, grammar: str) -> str:
    es_lower = es.lower()
    grammar_lower = grammar.lower()

    details = []

    # Subjunctive
    if "subjuntivo" in grammar_lower or "subj" in grammar_lower:
        details.append("本句含虛擬式（Subjuntivo）結構。在 que 子句中，當主句表達意願、情緒、評價或懷疑時，子句動詞需改用虛擬式，主從句主詞通常不同。")

    # Si + subjunctive (counterfactual)
    if re.search(r"\bsi\b", es_lower) and re.search(r"\b\w+(ara|iera|ase|iese)\b", es_lower):
        details.append("條件從句使用「si + 虛擬式過去未完成時（imperfecto de subjuntivo）」，搭配主句條件式，構成與現實相反的假設句（虛擬語氣第二類條件句）。")
    elif re.search(r"\bsi\b", es_lower) and re.search(r"\b\w+(aría|ería|iría)\b", es_lower):
        details.append("主句動詞使用條件式（condicional simple），表達假設情境下的可能結果，與 si 條件從句共同構成假設句型。")

    # Pluperfect
    if re.search(r"\bhab[íi]a[n]?\s+\w+ado\b|\bhab[íi]a[n]?\s+\w+ido\b", es_lower):
        details.append("句中含過去完成時（Pluscuamperfecto：había/habían + 過去分詞），表達在另一過去動作之前已完成的事件，強調時間先後順序。")

    # Present perfect
    if re.search(r"\bha[n]?\s+\w+ado\b|\bha[n]?\s+\w+ido\b", es_lower):
        details.append("句中含現在完成時（Pretérito Perfecto：ha/han + 過去分詞），表達與現在有關聯的已完成動作或近期發生的事件。")

    # Passive
    if re.search(r"\bfue\b|\bfueron\b|\bsido\b", es_lower) and "sido" in es_lower:
        details.append("句子含被動態結構（fue/fueron + 過去分詞），主詞承受動作，強調事件結果而非施事者。")

    # Se pasiva
    if re.search(r"\bse\s+\w+(a|an|ó|aron)\b", es_lower):
        details.append("句中含反身被動結構（se + 動詞第三人稱），為西班牙語常見的非人稱或去人稱化表達，施事者不明確或不重要。")

    # Inversion in question
    if es.startswith("¿") and re.search(r"¿\w+\s+\w+\s+\w+", es):
        details.append("疑問句中動詞置於主詞之前（倒裝語序），為西班牙語疑問句的正常語法結構，不同於英語需助動詞的倒裝方式。")

    return " ".join(details) if details else ""


# ── index topic ───────────────────────────────────────────────────────────────

def get_topic(rows):
    """Guess a topic from first few rows' Spanish text."""
    # Based on the content we see - social media & privacy
    return "社交媒體與隱私"


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb.active

    rows = []
    for row in ws.iter_rows(min_row=12, values_only=True):
        if row[0] is not None:
            rows.append(row)

    out_week = os.path.join(OUTPUT_DIR, WEEK_DIR)
    os.makedirs(out_week, exist_ok=True)

    count = 0
    index_rows = []

    for row in rows:
        tipo, num, es, zh, grammar = row[0], row[1], row[2], row[3], row[4]
        new_id = num.replace("M24-", "M6-W24-")

        content = analyze(tipo, num, es, zh, grammar)
        fname = f"{new_id}.md"
        fpath = os.path.join(out_week, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1

        index_rows.append(f"| [[{WEEK_DIR}/{new_id}]] | {tipo} | {grammar} |")

    topic = get_topic(rows)
    index_content = f"# {WEEK_DIR} 索引：{topic}\n\n"
    index_content += "| 編號 | 類型 | 語法重點 |\n"
    index_content += "|---|---|---|\n"
    index_content += "\n".join(index_rows) + "\n"

    index_path = os.path.join(OUTPUT_DIR, f"{WEEK_DIR}_index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)

    print(f"Done. Generated {count} card files + 1 index file.")
    print(f"Cards: {out_week}/")
    print(f"Index: {index_path}")


if __name__ == "__main__":
    main()
