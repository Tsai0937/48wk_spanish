import os
import re
import json
import time
import openpyxl
from google import genai as google_genai

# ==================== 1. 基本設定 ====================
# Mac 用戶：iCloud 路徑如下
# Windows 用戶：改成 os.path.expanduser("~/iCloudDrive/Obsidian/西文48週X50句型解析")
OBSIDIAN_VAULT_PATH = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/西文48週X50句型解析"
)

client = google_genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
GEMINI_MODEL = "gemini-2.5-flash"

# ==================== 2. ES 斷句準則（系統化） ====================
# 以下準則決定 chunked_es 的 / 切割位置，AI 必須依序套用：
#
# [規則1] 主從句邊界：在以下連接詞「前」切割：
#         porque, si, que, cuando, aunque, para que, sino que,
#         mientras, a menos que, con tal de que, sin que
# [規則2] 介系詞片語：en/de/por/para/con/sin + 名詞組 獨立成群
#         例：en la seguridad / de nuestra plataforma digital
# [規則3] 不定詞補語：動詞固定搭配的 en/a/de + inf. 單獨成群
#         例：en revisar / a implementar / de actualizar
# [規則4] 關係子句：que/quien/donde/cuyo 引導的修飾從句前切割
# [規則5] 逗號位置：已有逗號的地方直接切（逗號保留在前段）
# [規則6] 長名詞片語：超過 4 個詞的名詞片語單獨成一群
#         例：las políticas de privacidad / nuestra plataforma digital
# [優先順序] 規則1 > 規則5 > 規則2 > 規則3 > 規則4 > 規則6
# [底線原則] 每個群組以「可以獨立理解的語意單位」為目標，
#            不可切斷「動詞+其直接受詞」的核心結構

# ==================== 3. API 提示詞（含所有格式規則） ====================
SYSTEM_PROMPT = """你是一位精通中西雙語的進階西班牙文（B1-B2）教學專家。
請針對使用者提供的西班牙文長難句，嚴格依照以下規則輸出 JSON。

=== ES 斷句規則（chunked_es）===
用 / 將句子切割成語意群組，依序套用以下規則：
1. 主從句邊界：在 porque / si / que / cuando / aunque / para que / sino que / mientras / a menos que 等連接詞「前」切割
2. 介系詞片語：en/de/por/para/con/sin + 名詞組 獨立成群
3. 不定詞補語：動詞固定搭配的 en/a/de + inf. 單獨成群
4. 關係子句：que/quien/donde/cuyo 引導的修飾從句前切割
5. 逗號位置：已有逗號的地方直接切，逗號保留在前段
6. 長名詞片語：超過 4 個詞的名詞片語單獨成群
優先順序：規則1 > 規則5 > 規則2 > 規則3 > 規則4 > 規則6
底線原則：不可切斷「動詞+其直接受詞」的核心結構

=== 句型解析規則（analysis）===
- 3 至 5 點
- 每點格式：【角色標籤】西文片段（中文對應）— 說明
- 角色標籤限用：主要子句、原因從句、條件從句、名詞子句、
  關係從句、介系詞片語、不定詞補語、讓步從句、時間從句、目的從句
- 第一點必須是整句的主要子句
- 說明需指出該結構在句中的語法功能

=== 文法規則（grammar）===
- 3 至 5 點
- 每點格式：文法術語（西文術語）— 說明（至少 2 句，含用法規則與限制）
- 必須涵蓋 Excel E欄的所有語法點
- 如有虛擬式、完成式、條件式等特殊時態，單獨列出說明

=== 例句規則（examples）===
- 必須恰好 2 個例句
- 例句句型結構須與原句相同（相同的語法框架）
- 例句主題須與本週主題相關（由使用者提供）
- 格式：西文句子（中文翻譯）

=== vocab_list 規則 ===
- 只列動詞（原形）、名詞（單數）、形容詞
- 略去：el/la/los/las/un/una、de/en/por/para/con、que/si/porque 等虛詞
- 每個詞附 pos（v./m./f./adj./exp.）和 meaning（繁體中文）

=== 通用規則 ===
- 全程繁體中文
- 絕對不可有粗體（**）、斜體（*）、圖示

輸出 JSON 格式（不含任何 markdown 標記）：
{
  "chunked_es": "斷句後的句子，使用 / 分隔",
  "analysis": [
    "【主要子句】...",
    "【介系詞片語】..."
  ],
  "grammar": [
    "Insistir en（Régimen preposicional）— 說明第一句。說明第二句。",
    "..."
  ],
  "examples": [
    "西文例句1（中文翻譯1）",
    "西文例句2（中文翻譯2）"
  ],
  "vocab_list": [
    {"word": "insistir", "pos": "v.", "meaning": "堅持"}
  ]
}"""


# ==================== 4. API 呼叫（全批次，1次呼叫處理所有句子）====================
def analyze_all_sentences(sentences, topic):
    """
    sentences: list of (es_phrase, zh_meaning, grammar_tag)
    回傳: list of result dict，順序與輸入相同；失敗的項目為 None
    """
    numbered = ""
    for i, (es, zh, gr) in enumerate(sentences, 1):
        numbered += f"[{i}]\n原句：{es}\n中文：{zh}\n語法重點：{gr}\n\n"

    prompt = (
        f"本週主題：{topic}\n\n"
        f"以下共 {len(sentences)} 個句子，請依序解析，"
        f"回傳一個 JSON 陣列，陣列長度必須恰好為 {len(sentences)}，"
        f"每個元素的格式與 system prompt 中的單句格式完全相同。\n\n"
        f"{numbered}"
        f"請依照指定 JSON 格式解析，直接回傳陣列，不需要其他說明。"
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
            text = response.text.strip()
            text = re.sub(r'^```json\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            results = json.loads(text)
            if isinstance(results, list) and len(results) == len(sentences):
                return results
            print(f"  回傳筆數不符（期望 {len(sentences)}，得到 {len(results) if isinstance(results, list) else '非陣列'}），重試...")
        except Exception as e:
            err = str(e)
            if attempt < 4 and ('429' in err or '503' in err):
                wait = 15 * (attempt + 1)
                print(f"  暫時失敗（{429 if '429' in err else 503}），等待 {wait} 秒後重試...")
                time.sleep(wait)
            else:
                print(f"  API 解析失敗: {e}")
                return [None] * len(sentences)
    return [None] * len(sentences)


# ==================== 5. 卡片寫入 ====================
def write_card(path, tipo, card_id, result, zh_meaning, week_index_id):
    chunked_es  = result.get("chunked_es", "")
    analysis    = result.get("analysis", [])
    grammar     = result.get("grammar", [])
    examples    = result.get("examples", [])
    vocab_list  = result.get("vocab_list", [])

    ghost_links = " ".join([f"[[{v['word']}]]" for v in vocab_list])

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"[[{week_index_id}]]\n\n")   # 雙向連結回週INDEX
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


# ==================== 6. 主程式 ====================
def process_weekly_excel(file_path, curriculum_xlsx="input/SET_UP.xlsx"):
    """
    file_path: 每週句型 Excel，例如 "input/WK24.xlsx"
               週次從檔名自動解析（WK24 → week=24）
               月份與主題從 SET_UP.xlsx 自動查詢

    Excel 欄位（數據從第 12 行開始，第 11 行為標題）：
      A: 類型（Q/A/R/D）
      B: 原始編號（M24-001）
      C: 西班牙文句子
      D: 中文意思
      E: 核心語法重點

    輸出路徑結構（Obsidian vault）：
      vault/Spanish/
        ES_00_index.md         ← 主 INDEX（由 generate_master_index 產生）
        M{MM}/
          ES_W{WW}_index.md  ← 週 INDEX（清單格式）
          ES_W{WW}-001.md    ← 句型卡
          ...
    """
    # 從檔名解析週次（WK24.xlsx → 24）
    basename = os.path.basename(file_path)
    match = re.search(r'WK(\d+)', basename, re.IGNORECASE)
    if not match:
        raise ValueError(f"無法從檔名解析週次：{basename}，請確認格式為 WK24.xlsx")
    week = int(match.group(1))

    # 從 SET_UP.xlsx 查詢月份與主題
    curriculum = load_curriculum(curriculum_xlsx)
    if week not in curriculum:
        raise ValueError(f"SET_UP.xlsx 中找不到第 {week} 週的資料")
    month, title_name = curriculum[week]
    print(f"第 {week} 週：第 {month} 月 / {title_name}")

    week_str  = f"W{week:02d}"          # e.g. W24
    month_str = f"M{month:02d}"         # e.g. M06
    card_prefix = f"ES_{week_str}"      # e.g. ES_W24

    vault_spanish = os.path.join(OBSIDIAN_VAULT_PATH, "Spanish")
    week_dir = os.path.join(vault_spanish, month_str)
    os.makedirs(week_dir, exist_ok=True)

    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    # 讀取所有句子
    rows_data = []
    for row in range(12, sheet.max_row + 1):
        tipo        = sheet[f'A{row}'].value
        raw_no      = sheet[f'B{row}'].value
        es_phrase   = sheet[f'C{row}'].value
        zh_meaning  = sheet[f'D{row}'].value
        grammar_tag = sheet[f'E{row}'].value
        if not raw_no or not es_phrase:
            continue
        seq = raw_no.split('-')[-1]
        card_id = f"{card_prefix}_{seq}"   # e.g. ES_W01_001
        rows_data.append((tipo, card_id, es_phrase, zh_meaning, grammar_tag))

    # 分批處理（每批 25 句，避免輸出超過 token 上限）
    # start_batch: 從第幾批開始（0-based），用於補跑失敗批次
    BATCH_SIZE = 25
    total_batches = (len(rows_data) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"共讀取 {len(rows_data)} 句，分 {total_batches} 批送出...")

    results = [None] * len(rows_data)
    for b in range(total_batches):
        batch = rows_data[b * BATCH_SIZE:(b + 1) * BATCH_SIZE]
        sentences = [(es, zh, gr) for _, _, es, zh, gr in batch]
        print(f"  第 {b+1}/{total_batches} 批（{len(sentences)} 句）...")
        batch_results = analyze_all_sentences(sentences, title_name)
        for i, r in enumerate(batch_results):
            results[b * BATCH_SIZE + i] = r

    index_entries = []
    for i, (tipo, card_id, es_phrase, zh_meaning, _) in enumerate(rows_data):
        card_path = os.path.join(week_dir, f"{card_id}.md")
        result = results[i]
        if not result:
            # 若卡片已存在（上次成功），讀取 chunked_es 加入 index
            if os.path.exists(card_path):
                with open(card_path, encoding="utf-8") as f:
                    first_es = ""
                    for line in f:
                        if line.startswith("ES："):
                            first_es = line[3:].strip()
                            break
                index_entries.append((card_id, tipo, first_es, zh_meaning))
            else:
                print(f"  跳過 {card_id}（API 失敗）")
            continue
        print(f"  寫入: {card_id}")
        week_index_id = f"{card_prefix}_index"
        write_card(card_path, tipo, card_id, result, zh_meaning, week_index_id)
        chunked_es = result.get("chunked_es", es_phrase)
        index_entries.append((card_id, tipo, chunked_es, zh_meaning))

    # 週 INDEX
    index_path = os.path.join(week_dir, f"{card_prefix}_index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"[[ES_00_index]]\n\n")   # 雙向連結回主INDEX
        f.write(f"# {card_prefix}：{title_name}\n\n")
        for card_id, tipo, chunked_es, zh_meaning in index_entries:
            f.write(f"[[{card_id}]] | {tipo}\n")
            f.write(f"ES：{chunked_es}\n")
            f.write(f"ZH：{zh_meaning}\n\n")

    print(f"\n完成！共 {len(index_entries)} 張卡片。")
    print(f"檔案位置：{week_dir}")


# ==================== 7. 課程查找表 ====================
def load_curriculum(curriculum_xlsx="input/SET_UP.xlsx"):
    """
    從 SET_UP.xlsx 建立週次查找表。
    回傳 dict: {week_num: (month_num, topic)}
    例如: {24: (6, "社交媒體與隱私 (Redes Sociales y Privacidad)"), ...}
    """
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
        week_num = int(b.replace("Week", "").strip())
        month_num = int(current_month.replace("第", "").replace("月", "").strip())
        lookup[week_num] = (month_num, c)
    return lookup


# ==================== 8. 主 INDEX 產生器 ====================
def generate_master_index(curriculum_xlsx="input/SET_UP.xlsx"):
    """
    從 SET_UP.xlsx 的課程規劃表（第 15 行起）產生 ES_00_index.md。
    輸出至 vault/Spanish/ES_00_index.md。
    """
    wb = openpyxl.load_workbook(curriculum_xlsx)
    sheet = wb.active

    # 讀取課程表（月份/週次/主題，從第 16 行到第 63 行）
    curriculum = []
    current_month = ""
    for row in range(16, sheet.max_row + 1):
        a = str(sheet[f'A{row}'].value or "").strip()
        b = str(sheet[f'B{row}'].value or "").strip()
        c = str(sheet[f'C{row}'].value or "").strip()
        if not b:
            break
        if a:
            current_month = a
        # 取週次數字
        week_num = int(b.replace("Week", "").strip())
        # 取月份數字
        month_num = int(current_month.replace("第", "").replace("月", "").strip())
        curriculum.append((month_num, week_num, c))

    vault_spanish = os.path.join(OBSIDIAN_VAULT_PATH, "Spanish")
    os.makedirs(vault_spanish, exist_ok=True)
    out_path = os.path.join(vault_spanish, "ES_00_index.md")  # 主INDEX檔名

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# 48週西班牙文學習總覽\n\n")
        current_month = 0
        for month_num, week_num, topic in curriculum:
            if month_num != current_month:
                current_month = month_num
                f.write(f"## 第 {month_num} 月\n\n")
            week_str = f"W{week_num:02d}"
            f.write(f"[[ES_{week_str}_index]] {topic}\n")
        f.write("\n")

    print(f"主 INDEX 已產生：{out_path}")


# ==================== 9. 執行入口 ====================
if __name__ == "__main__":
    # 產生主 INDEX（從 SET_UP.xlsx，只需第一次或課程規劃更新時執行）
    # generate_master_index()

    # 處理每週句型：只需指定檔案，月份/主題自動從 SET_UP.xlsx 查詢
    process_weekly_excel("input/WK24.xlsx")
