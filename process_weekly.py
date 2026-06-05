import os
import re
import json
import time
import openpyxl
from google import genai as google_genai

# ── 設定 ──────────────────────────────────────────────
# Mac iCloud 路徑；Windows 改成 ~/iCloudDrive/Obsidian/...
OBSIDIAN_VAULT_PATH = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/西文48週X50句型解析"
)
client = google_genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
GEMINI_MODEL = "gemini-2.5-flash"

# ── System Prompt ──────────────────────────────────────
SYSTEM_PROMPT = """你是進階西班牙文（B1-B2）教學專家，請對每個句子輸出 JSON。

ES 斷句（chunked_es）：用 / 切割語意群組，優先順序：
1. 主從句邊界（porque/si/que/cuando/aunque/para que 等連接詞前）
2. 逗號處（逗號保留在前段）
3. 介系詞片語（en/de/por/para/con/sin + 名詞組）
4. 不定詞補語（動詞搭配的 en/a/de + inf.）
5. 關係子句（que/quien/donde/cuyo 前）
6. 長名詞片語（超過4詞）
禁止切斷「動詞+直接受詞」核心結構。

analysis：3-5點，格式「【標籤】西文片段（中文）— 說明」
標籤限用：主要子句、原因從句、條件從句、名詞子句、關係從句、介系詞片語、不定詞補語、讓步從句、時間從句、目的從句
第一點必須是主要子句。

grammar：3-5點，格式「術語（西文術語）— 說明（含用法與限制，至少2句）」
必須涵蓋輸入中的語法重點；虛擬式/完成式/條件式須單獨列出。

examples：恰好2句，結構與原句相同，主題與本週主題相關。格式：西文（中文）

vocab_list：只列動詞原形、名詞單數、形容詞；略去冠詞、介系詞、連接詞。
每詞附 pos（v./m./f./adj./exp.）和 meaning（繁體中文）。

全程繁體中文，禁用粗體（**）、斜體（*）、圖示。

輸出純 JSON 陣列（處理多句時）或單一 JSON 物件：
{"chunked_es":"...","analysis":[...],"grammar":[...],"examples":[...],"vocab_list":[{"word":"...","pos":"...","meaning":"..."}]}"""


# ── API 呼叫（每批 25 句，1次呼叫）──────────────────────
def analyze_all_sentences(sentences, topic):
    """sentences: list of (es, zh, grammar)；回傳等長 list，失敗項為 None"""
    numbered = ""
    for i, (es, zh, gr) in enumerate(sentences, 1):
        numbered += f"[{i}] 原句：{es}\n中文：{zh}\n語法重點：{gr}\n\n"

    prompt = (
        f"本週主題：{topic}\n"
        f"以下 {len(sentences)} 句，請依序解析，回傳長度恰好為 {len(sentences)} 的 JSON 陣列。\n\n"
        f"{numbered}"
    )

    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "temperature": 0.2,
                    "system_instruction": SYSTEM_PROMPT,
                    "max_output_tokens": 65536,
                }
            )
            text = re.sub(r'^```json\s*|\s*```$', '', response.text.strip())
            results = json.loads(text)
            if isinstance(results, list) and len(results) == len(sentences):
                return results
            print(f"  回傳筆數不符（期望 {len(sentences)}，得到 {len(results) if isinstance(results, list) else '非陣列'}），重試...")
        except Exception as e:
            err = str(e)
            if attempt < 4 and ('429' in err or '503' in err):
                wait = 15 * (attempt + 1)
                print(f"  暫時失敗，等待 {wait} 秒後重試...")
                time.sleep(wait)
            else:
                print(f"  API 失敗: {e}")
                return [None] * len(sentences)
    return [None] * len(sentences)


# ── 卡片寫入 ───────────────────────────────────────────
def write_card(path, tipo, card_id, result, zh_meaning, week_index_id):
    chunked_es = result.get("chunked_es", "")
    analysis   = result.get("analysis", [])
    grammar    = result.get("grammar", [])
    examples   = result.get("examples", [])
    vocab_list = result.get("vocab_list", [])
    ghost_links = ", ".join(f"[[{v['word']}]]" for v in vocab_list)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"[[{week_index_id}]]\n\n")
        f.write(f"{tipo} | {card_id}\n\n")
        f.write(f"ES：{chunked_es}\n")
        f.write(f"ZH：{zh_meaning}\n\n")
        f.write("句型解析：\n")
        for i, line in enumerate(analysis, 1):
            f.write(f"{i}. {line}\n")
        f.write("\n文法：\n")
        for i, line in enumerate(grammar, 1):
            f.write(f"{i}. {line}\n")
        f.write("\n例句：\n")
        for i, ex in enumerate(examples, 1):
            f.write(f"{i}. {ex}\n")
        f.write(f"\n核心單字：{ghost_links}\n")


# ── 課程查找表 ─────────────────────────────────────────
def load_curriculum(curriculum_xlsx="input/SET_UP.xlsx"):
    """回傳 {week_num: (month_num, topic)}，從 SET_UP.xlsx 第16行起讀取"""
    wb = openpyxl.load_workbook(curriculum_xlsx)
    sheet = wb.active
    lookup = {}
    current_month = ""
    for row in range(16, sheet.max_row + 1):
        a = str(sheet[f'A{row}'].value or "").strip()
        b = str(sheet[f'B{row}'].value or "").strip()
        c = str(sheet[f'C{row}'].value or "").strip()
        if not b:
            break
        if a:
            current_month = a
        week_num  = int(b.replace("Week", "").strip())
        month_num = int(current_month.replace("第", "").replace("月", "").strip())
        lookup[week_num] = (month_num, c)
    return lookup


# ── 主 INDEX 產生器 ────────────────────────────────────
def generate_master_index(curriculum_xlsx="input/SET_UP.xlsx"):
    """從 SET_UP.xlsx 產生 ES_00_index.md（只需執行一次）"""
    curriculum = load_curriculum(curriculum_xlsx)

    vault_spanish = os.path.join(OBSIDIAN_VAULT_PATH, "Spanish")
    os.makedirs(vault_spanish, exist_ok=True)
    out_path = os.path.join(vault_spanish, "ES_00_index.md")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# 48週西班牙文學習總覽\n\n")
        current_month = 0
        for week_num in sorted(curriculum):
            month_num, topic = curriculum[week_num]
            if month_num != current_month:
                current_month = month_num
                f.write(f"## 第 {month_num} 月\n\n")
            f.write(f"[[ES_W{week_num:02d}_index]] {topic}\n")
        f.write("\n")

    print(f"主 INDEX 已產生：{out_path}")


# ── 每週主程式 ─────────────────────────────────────────
def process_weekly_excel(file_path, curriculum_xlsx="input/SET_UP.xlsx"):
    """
    file_path: 每週句型 Excel，例如 "input/WK1.xlsx"
    週次從檔名自動解析（WK1 → week=1），月份與主題從 SET_UP.xlsx 查詢。

    Excel 欄位（第12行起，第11行為標題）：
      A: 類型（Q/A/R/D）  B: 編號  C: 西文  D: 中文  E: 語法重點

    輸出：vault/Spanish/M{MM}/ES_W{WW}_index.md + ES_W{WW}_001.md ...
    """
    match = re.search(r'WK(\d+)', os.path.basename(file_path), re.IGNORECASE)
    if not match:
        raise ValueError(f"檔名須含週次，例如 WK1.xlsx（收到：{file_path}）")
    week = int(match.group(1))

    curriculum = load_curriculum(curriculum_xlsx)
    if week not in curriculum:
        raise ValueError(f"SET_UP.xlsx 找不到第 {week} 週")
    month, title_name = curriculum[week]
    print(f"第 {week} 週：第 {month} 月 / {title_name}")

    card_prefix = f"ES_W{week:02d}"
    week_index_id = f"{card_prefix}_index"
    week_dir = os.path.join(OBSIDIAN_VAULT_PATH, "Spanish", f"M{month:02d}")
    os.makedirs(week_dir, exist_ok=True)

    # 讀取句子
    sheet = openpyxl.load_workbook(file_path).active
    rows_data = []
    for row in range(12, sheet.max_row + 1):
        tipo, raw_no, es, zh, gr = (sheet.cell(row, c).value for c in range(1, 6))
        if not raw_no or not es:
            continue
        card_id = f"{card_prefix}_{raw_no.split('-')[-1]}"
        rows_data.append((tipo, card_id, es, zh, gr))

    # 分批送出（每批 25 句，避免輸出超過 token 上限）
    BATCH_SIZE = 25
    total_batches = (len(rows_data) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"共 {len(rows_data)} 句，分 {total_batches} 批送出...")

    results = [None] * len(rows_data)
    for b in range(total_batches):
        batch = rows_data[b * BATCH_SIZE:(b + 1) * BATCH_SIZE]
        print(f"  第 {b+1}/{total_batches} 批（{len(batch)} 句）...")
        batch_results = analyze_all_sentences([(es, zh, gr) for _, _, es, zh, gr in batch], title_name)
        for i, r in enumerate(batch_results):
            results[b * BATCH_SIZE + i] = r

    # 寫入卡片
    index_entries = []
    for i, (tipo, card_id, es, zh, _) in enumerate(rows_data):
        card_path = os.path.join(week_dir, f"{card_id}.md")
        result = results[i]
        if not result:
            if os.path.exists(card_path):  # 上次已成功，讀取 ES 加入 index
                chunked_es = next(
                    (l[3:].strip() for l in open(card_path, encoding="utf-8") if l.startswith("ES：")), es
                )
                index_entries.append((card_id, tipo, chunked_es, zh))
            else:
                print(f"  跳過 {card_id}（API 失敗）")
            continue
        print(f"  寫入: {card_id}")
        write_card(card_path, tipo, card_id, result, zh, week_index_id)
        index_entries.append((card_id, tipo, result.get("chunked_es", es), zh))

    # 週 INDEX
    with open(os.path.join(week_dir, f"{week_index_id}.md"), "w", encoding="utf-8") as f:
        f.write(f"[[ES_00_index]]\n\n# {card_prefix}：{title_name}\n\n")
        for card_id, tipo, chunked_es, zh in index_entries:
            f.write(f"[[{card_id}]] | {tipo}\nES：{chunked_es}\nZH：{zh}\n\n")

    print(f"\n完成！共 {len(index_entries)} 張卡片。\n位置：{week_dir}")


# ── 執行入口 ───────────────────────────────────────────
if __name__ == "__main__":
    # 主 INDEX（只需第一次，或課程規劃更新時）
    # generate_master_index()

    # 每週執行：只需換檔名，其餘自動查詢
    process_weekly_excel("input/WK1.xlsx")
