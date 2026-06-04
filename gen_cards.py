#!/usr/bin/env python3
import openpyxl
import anthropic
import os
import time

client = anthropic.Anthropic()

OUTPUT_DIR = "/home/user/48wk_spanish/output5"
EXCEL_PATH = "/home/user/48wk_spanish/WK24.xlsx"
TOPIC = "社交媒體與隱私"
WEEK = "W24"
MODULE = "M6"

def convert_id(old_id):
    parts = old_id.split('-')
    num = parts[1]
    return f"{MODULE}-{WEEK}-{num}"

def make_prompt(type_code, new_id, es, zh, grammar_hint):
    return f"""你是一位西班牙語教學專家，請為以下句子製作 Obsidian 學習卡片。

資料：
- 類型：{type_code}
- 編號：{new_id}
- ES（西文）：{es}
- ZH（中文）：{zh}
- 語法重點提示：{grammar_hint}
- 週主題：{TOPIC}

請嚴格按照以下格式輸出，不要有任何額外說明，不要有粗體（**），不要有斜體（*），全用繁體中文：

{type_code} | {new_id}

ES：[將西文句子用 / 做語意斷句，依主從句、介系詞片語、副詞子句等分割，每個斷點加 / 並前後各一個空格]
ZH：{zh}

句型解析：
[3到5點，每點格式：數字. 【角色標籤】西文片語（中文解釋）— 說明。角色標籤用【主要子句】【原因從句】【名詞子句】【介系詞片語】【條件從句】【副詞子句】【補語從句】等]

文法：
[3到5點，每點格式：數字. 西文術語（中文術語）— 詳細說明，每點至少2句說明，結合語法重點提示]

例句：
[2個例句，與{TOPIC}主題相關，句型結構與原句相同，格式：數字.（西文例句）（中文翻譯）]

核心單字：[[單字1]] [[單字2]] [[單字3]] [只列實詞，略去虛詞，5個左右]

注意：
- ES 斷句用 / 分隔，/ 前後各一個空格
- 不要有「核心語法：」那一行
- 不要有粗體(**text**)或斜體(*text*)
- 文法點的西文術語寫在前，括號內寫中文術語
- 全部繁體中文
"""

def generate_card(type_code, new_id, es, zh, grammar_hint):
    prompt = make_prompt(type_code, new_id, es, zh, grammar_hint)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def main():
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb.active

    rows = []
    for row in ws.iter_rows(min_row=12, values_only=True):
        if row[0] is not None and row[1] is not None:
            rows.append(row)

    print(f"Found {len(rows)} rows")

    index_rows = []

    for i, row in enumerate(rows):
        type_code = row[0]
        old_id = row[1]
        es = row[2]
        zh = row[3]
        grammar_hint = row[4] if row[4] else ""

        new_id = convert_id(old_id)
        filename = f"{new_id}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        print(f"[{i+1}/{len(rows)}] Generating {new_id}...")

        for attempt in range(2):
            try:
                content = generate_card(type_code, new_id, es, zh, grammar_hint)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                zh_short = zh[:30] + "..." if len(zh) > 30 else zh
                index_rows.append((new_id, type_code, zh_short))
                print(f"  -> Saved {filename}")
                break
            except Exception as e:
                print(f"  ERROR attempt {attempt+1}: {e}")
                if attempt == 0:
                    time.sleep(10)
                else:
                    print(f"  FAILED {new_id}")

        time.sleep(0.5)

    # Generate index file
    index_path = os.path.join(OUTPUT_DIR, f"{MODULE}-{WEEK}_index.md")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(f"# {MODULE}-{WEEK} 索引：{TOPIC}\n\n")
        f.write("| 編號 | 類型 | 中文句意 |\n")
        f.write("|---|---|---|\n")
        for new_id, type_code, zh_short in index_rows:
            f.write(f"| [[{new_id}]] | {type_code} | {zh_short} |\n")

    print(f"\nDone! Generated {len(index_rows)} card files + 1 index file")
    print(f"Total files: {len(index_rows) + 1}")

if __name__ == "__main__":
    main()
