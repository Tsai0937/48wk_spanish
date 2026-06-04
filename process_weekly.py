import os
import re
import json
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

# ==================== 2. API 提示詞 ====================
# 拆解（analysis）必須同時包含：
#   - 整句結構解析（主從句關係、語序、句型邏輯）
#   - 核心片語/動詞搭配解析（insistir en、confiar en 等）
#   - 任何值得注意的語法細節（虛擬式觸發、條件句、疑問句語序等）
# vocab_list 只列動詞、名詞、形容詞等實詞，略去 el/la/de/que 等虛詞
# grammar_list 只列核心語法點（對應 Excel E欄的片語搭配）

SYSTEM_PROMPT = """你是一位精通中西雙語的進階西班牙文（B1-B2）教學專家。
請針對使用者提供的西班牙文長難句進行深度解析。

你必須嚴格輸出 JSON 格式（不要包含任何 markdown 標記如 ```json），結構如下：
{
  "chunked_es": "將原句依據語意群組用 / 分隔。例如：Dudo que / el vuelo / salga / a tiempo",
  "analysis": [
    "【句型結構】說明整句的主從句結構、語序邏輯或句型框架。例如：主句為疑問句（¿Por qué + 動詞 + 主詞），後接 si 條件從句形成對比語氣。",
    "【片語拆解】insistir en + inf.：動詞 insistir 後固定接介詞 en，再加不定詞，表示堅持做某事。",
    "【片語拆解】confiar en：動詞 confiar 後接介詞 en，表示信任某人或某事。",
    "【語法細節】任何虛擬式、條件句、特殊語序、時態等值得特別標注的細節。"
  ],
  "vocab_list": [
    {"word": "單字（原形）", "pos": "詞性（v./m./f./adj./exp.）", "meaning": "中文意思"}
  ],
  "grammar_list": [
    {"point": "片語名稱（如 Insistir en）", "desc": "一句話說明用法"}
  ]
}

規則：
- analysis 第一點必須是整句結構說明，之後才是片語與語法細節
- analysis 每點前加【句型結構】【片語拆解】【語法細節】等標籤
- 文字極簡，絕對不可包含粗體（**）、斜體（*）或圖示
- vocab_list 的 word 填動詞原形或名詞單數形"""


def analyze_sentence(es_sentence, zh_meaning, grammar_tag):
    import time
    prompt = (
        f"原句：{es_sentence}\n"
        f"中文：{zh_meaning}\n"
        f"預期語法：{grammar_tag}\n\n"
        f"請依照指定JSON格式解析。"
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
                print(f"速率限制，等待 {wait} 秒後重試...")
                time.sleep(wait)
            else:
                print(f"API 解析失敗: {e}")
                return None


def make_card_id(raw_no, month, week):
    """
    將 Excel 原始編號（如 M24-001）轉成卡片 ID（如 M1-W24-001）
    month: 月份數字（如 1）
    week: 週次數字（如 24）
    """
    seq = raw_no.split('-')[-1]  # 取最後的序號部分 001
    return f"M{month}-W{week}-{seq}"


# ==================== 3. 主程式 ====================
def process_weekly_excel(file_path, month, week, title_name):
    """
    month: int，第幾個月，例如 1
    week:  int，第幾週，例如 24
    title_name: str，主題名稱，例如 "社交媒體與隱私"
    """
    week_label = f"M{month}-W{week}"  # 例如 M1-W24

    # 輸出目錄
    vault = OBSIDIAN_VAULT_PATH
    cards_dir = os.path.join(vault, week_label)
    os.makedirs(cards_dir, exist_ok=True)

    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    index_rows = []   # 收集 index 表格每一行

    # 欄位：類型(A), 編號(B), 西文(C), 中文(D), 語法(E)
    # 數據從第 12 行開始（第 11 行是欄位標題）
    for row in range(12, sheet.max_row + 1):
        tipo      = sheet[f'A{row}'].value
        raw_no    = sheet[f'B{row}'].value
        es_phrase = sheet[f'C{row}'].value
        zh_meaning = sheet[f'D{row}'].value
        grammar_tag = sheet[f'E{row}'].value

        if not raw_no or not es_phrase:
            continue

        card_id = make_card_id(raw_no, month, week)
        print(f"正在處理: {card_id}...")

        api_result = analyze_sentence(es_phrase, zh_meaning, grammar_tag)

        if not api_result:
            continue

        chunked_es   = api_result.get("chunked_es", es_phrase)
        analysis     = api_result.get("analysis", [])
        vocab_list   = api_result.get("vocab_list", [])
        grammar_list = api_result.get("grammar_list", [])

        # 核心單字：幽靈連結，只列實詞
        ghost_links = " ".join([f"[[{v['word']}]]" for v in vocab_list])

        # ---- 句子卡片 ----
        card_path = os.path.join(cards_dir, f"{card_id}.md")
        with open(card_path, "w", encoding="utf-8") as f:
            f.write(f"{tipo} | {card_id}\n\n")
            f.write(f"ES：{chunked_es}\n")
            f.write(f"ZH：{zh_meaning}\n")
            f.write(f"核心語法：{grammar_tag}\n")
            f.write("拆解：\n")
            for line in analysis:
                f.write(f"{line}\n")
            f.write(f"核心單字：{ghost_links}\n")

        # ---- 收集 index 資料 ----
        index_rows.append(
            f"| [[{week_label}/{card_id}\\|{card_id}]] | {tipo} | {grammar_tag} |"
        )

    # ---- INDEX 檔 ----
    index_path = os.path.join(vault, f"{week_label}_index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"# {week_label} 索引：{title_name}\n\n")
        f.write("| 編號 | 類型 | 語法重點 |\n")
        f.write("|---|---|---|\n")
        for r in index_rows:
            f.write(r + "\n")

    print(f"\n完成！共 {len(index_rows)} 張卡片，INDEX 已建立。")
    print(f"位置：{vault}")


# ==================== 4. 執行入口 ====================
if __name__ == "__main__":
    # month=第幾個月, week=第幾週
    process_weekly_excel("WK24.xlsx", month=1, week=24, title_name="社交媒體與隱私")
