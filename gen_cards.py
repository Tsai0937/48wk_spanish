#!/usr/bin/env python3
import openpyxl
import anthropic
import os
import re
import time

client = anthropic.Anthropic()

SYSTEM_PROMPT = """你是一位西班牙語教學專家，專門為台灣學習者製作 Obsidian 句子學習卡片。
你的分析必須準確、詳細，使用繁體中文，不使用粗體或斜體。
週主題：社交媒體與隱私（第24週）。"""

def make_card_prompt(tipo, numero_new, es, zh, grammar_hint):
    return f"""請為以下西班牙語句子製作學習卡片。

類型：{tipo}
編號：{numero_new}
ES：{es}
ZH：{zh}
語法重點：{grammar_hint}

請嚴格按照以下格式輸出（不要加任何其他文字）：

{tipo} | {numero_new}

ES：[原句，用 / 做語意斷句，依主從句、介系詞片語、副詞子句等分割，每個語意單位間加 /]
ZH：{zh}

句型解析：
[3-5點，每點格式：序號. 【角色標籤】原文片段（中文解釋）— 說明。角色標籤包含：主要子句、原因從句、名詞子句/事情內容、介系詞片語/原因與地點、條件從句、讓步從句、目的從句、關係子句等]

文法：
[3-5點，每點含西文術語，詳細說明用法，每點至少2句說明。格式：序號. 西文術語（中文術語）— 說明。]

例句：
[2個與社交媒體與隱私主題相關的例句，句型結構與原句相同，附完整中文翻譯。格式：序號. 西班牙文。（中文翻譯。）]

核心單字：[[單字1]] [[單字2]] [[單字3]] ...
[只列實詞，略去虛詞，從ES句子中選取核心動詞、名詞、形容詞]"""


def generate_card(tipo, numero_new, es, zh, grammar_hint):
    prompt = make_card_prompt(tipo, numero_new, es, zh, grammar_hint)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def convert_number(num_str):
    m = re.match(r'M24-(\d+)', num_str)
    if m:
        return f"M6-W24-{m.group(1)}"
    return num_str


def main():
    wb = openpyxl.load_workbook('/home/user/48wk_spanish/WK24.xlsx')
    ws = wb.active

    rows = []
    for row in ws.iter_rows(min_row=12, values_only=True):
        if row[0] is not None:
            rows.append(row)

    print(f"Total sentences: {len(rows)}")

    output_dir = '/home/user/48wk_spanish/output5'
    os.makedirs(output_dir, exist_ok=True)

    index_rows = []

    for i, row in enumerate(rows):
        tipo, numero, es, zh, grammar = row[0], row[1], row[2], row[3], row[4]
        numero_new = convert_number(numero)
        filename = f"{numero_new}.md"
        filepath = os.path.join(output_dir, filename)

        print(f"[{i+1}/{len(rows)}] Generating {numero_new}...")

        try:
            card_content = generate_card(tipo, numero_new, es, zh, grammar or '')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(card_content)
            zh_short = zh[:30] + ('...' if len(zh) > 30 else '')
            index_rows.append((numero_new, tipo, zh_short))
            print(f"  -> Saved {filename}")
            if i < len(rows) - 1:
                time.sleep(0.3)
        except Exception as e:
            print(f"  ERROR: {e}")
            time.sleep(3)
            try:
                card_content = generate_card(tipo, numero_new, es, zh, grammar or '')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(card_content)
                zh_short = zh[:30] + ('...' if len(zh) > 30 else '')
                index_rows.append((numero_new, tipo, zh_short))
                print(f"  -> Saved {filename} (retry)")
            except Exception as e2:
                print(f"  FAILED: {e2}")

    # Generate index file
    index_path = os.path.join(output_dir, 'M6-W24_index.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# M6-W24 索引：社交媒體與隱私\n\n")
        f.write("| 編號 | 類型 | 中文句意 |\n")
        f.write("|---|---|---|\n")
        for num, t, zh_s in index_rows:
            f.write(f"| [[{num}]] | {t} | {zh_s} |\n")

    print(f"\nDone! Generated {len(index_rows)} card files + 1 index file")
    print(f"Total files: {len(index_rows) + 1}")


if __name__ == '__main__':
    main()
