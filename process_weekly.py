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
GEMINI_MODEL = "gemini-2.5-flash-lite"

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


# ==================== 4. API 呼叫 ====================
def analyze_sentence(es_sentence, zh_meaning, grammar_tag, topic):
    prompt = (
        f"原句：{es_sentence}\n"
        f"中文：{zh_meaning}\n"
        f"語法重點：{grammar_tag}\n"
        f"本週主題：{topic}\n\n"
        f"請依照指定 JSON 格式解析。"
    )
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "temperature": 0.2,
                    "system_instruction": SYSTEM_PROMPT
                }
            )
            text = response.text.strip()
            text = re.sub(r'^```json\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
            return json.loads(text)
        except Exception as e:
            if '429' in str(e) and attempt < 4:
                wait = 15 * (attempt + 1)
                print(f"  速率限制，等待 {wait} 秒後重試...")
                time.sleep(wait)
            else:
                print(f"  API 解析失敗: {e}")
                return None


# ==================== 5. 卡片寫入 ====================
def write_card(path, tipo, card_id, result, zh_meaning):
    chunked_es  = result.get("chunked_es", "")
    analysis    = result.get("analysis", [])
    grammar     = result.get("grammar", [])
    examples    = result.get("examples", [])
    vocab_list  = result.get("vocab_list", [])

    ghost_links = " ".join([f"[[{v['word']}]]" for v in vocab_list])

    with open(path, "w", encoding="utf-8") as f:
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
def process_weekly_excel(file_path, month, week, title_name):
    """
    month:      int，第幾個月，例如 6
    week:       int，第幾週，例如 24
    title_name: str，主題名稱，例如 "社交媒體與隱私"

    Excel 欄位（數據從第 12 行開始，第 11 行為標題）：
      A: 類型（Q/A/R/D）
      B: 原始編號（M24-001）
      C: 西班牙文句子
      D: 中文意思
      E: 核心語法重點

    輸出路徑結構（Obsidian vault）：
      vault/Spanish/
        ES_00_總覽.md         ← 主 INDEX（由 generate_master_index 產生）
        M{MM}/
          ES_W{WW}_index.md  ← 週 INDEX（清單格式）
          ES_W{WW}-001.md    ← 句型卡
          ...
    """
    week_str  = f"W{week:02d}"          # e.g. W24
    month_str = f"M{month:02d}"         # e.g. M06
    card_prefix = f"ES_{week_str}"      # e.g. ES_W24

    vault_spanish = os.path.join(OBSIDIAN_VAULT_PATH, "Spanish")
    week_dir = os.path.join(vault_spanish, month_str)
    os.makedirs(week_dir, exist_ok=True)

    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    index_entries = []

    for row in range(12, sheet.max_row + 1):
        tipo        = sheet[f'A{row}'].value
        raw_no      = sheet[f'B{row}'].value
        es_phrase   = sheet[f'C{row}'].value
        zh_meaning  = sheet[f'D{row}'].value
        grammar_tag = sheet[f'E{row}'].value

        if not raw_no or not es_phrase:
            continue

        seq = raw_no.split('-')[-1]
        card_id = f"{card_prefix}-{seq}"   # e.g. ES_W24-001
        print(f"正在處理: {card_id}...")

        result = analyze_sentence(es_phrase, zh_meaning, grammar_tag, title_name)
        if not result:
            print(f"  跳過 {card_id}（API 失敗）")
            continue

        card_path = os.path.join(week_dir, f"{card_id}.md")
        write_card(card_path, tipo, card_id, result, zh_meaning)

        chunked_es = result.get("chunked_es", es_phrase)
        index_entries.append((card_id, tipo, chunked_es, zh_meaning))

    # 週 INDEX（清單格式）
    index_path = os.path.join(week_dir, f"{card_prefix}_index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"# {card_prefix}：{title_name}\n\n")
        f.write(f"[[ES_00_總覽]]\n\n")
        f.write("---\n\n")
        for card_id, tipo, chunked_es, zh_meaning in index_entries:
            f.write(f"[[{card_id}]]  {tipo}\n")
            f.write(f"ES：{chunked_es}\n")
            f.write(f"ZH：{zh_meaning}\n\n")
            f.write("---\n\n")

    print(f"\n完成！共 {len(index_entries)} 張卡片。")
    print(f"檔案位置：{week_dir}")


# ==================== 7. 主 INDEX 產生器 ====================
def generate_master_index(curriculum_xlsx):
    """
    從 WK25.xlsx 的課程規劃表（第 15 行起）產生 ES_00_總覽.md。
    輸出至 vault/Spanish/ES_00_總覽.md。
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
    out_path = os.path.join(vault_spanish, "ES_00_總覽.md")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# 48週西班牙文學習總覽\n\n")
        current_month = 0
        for month_num, week_num, topic in curriculum:
            if month_num != current_month:
                current_month = month_num
                f.write(f"## 第 {month_num} 月\n\n")
            week_str = f"W{week_num:02d}"
            f.write(f"- [[ES_{week_str}_index|{week_str}：{topic}]]\n")
        f.write("\n")

    print(f"主 INDEX 已產生：{out_path}")


# ==================== 8. 執行入口 ====================
if __name__ == "__main__":
    # 產生主 INDEX（從 WK25.xlsx 課程規劃表）
    # generate_master_index("input/WK25.xlsx")

    # 處理每週句型（month=第幾個月, week=第幾週, title_name=主題名稱）
    process_weekly_excel("input/WK24.xlsx", month=6, week=24, title_name="社交媒體與隱私")
