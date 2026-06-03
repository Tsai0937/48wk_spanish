import os
import openpyxl
import re
import json
from datetime import datetime
import google.generativeai as genai

# ==================== 1. 基本設定（請依據本機環境修改） ====================
# Mac 用戶：iCloud 路徑如下
# Windows 用戶：改成 os.path.expanduser("~/iCloudDrive/Obsidian/西文48週X50句型解析")
OBSIDIAN_VAULT_PATH = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/西文48週X50句型解析"
)
WEEKLY_DIR = os.path.join(OBSIDIAN_VAULT_PATH, "Obsidian-Weekly")
DICT_DIR = os.path.join(OBSIDIAN_VAULT_PATH, "Dictionary")
GRAMMAR_DIR = os.path.join(OBSIDIAN_VAULT_PATH, "Grammar")

os.makedirs(WEEKLY_DIR, exist_ok=True)
os.makedirs(DICT_DIR, exist_ok=True)
os.makedirs(GRAMMAR_DIR, exist_ok=True)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# ==================== 2. API 核心提示詞設計 ====================
SYSTEM_PROMPT = """
你是一位精通中西雙語的進階西班牙文（B1-B2）教學專家。
請針對使用者提供的西班牙文長難句進行深度解析。

你必須嚴格輸出 JSON 格式（不要包含任何 markdown 標記如 ```json），結構如下：
{
  "chunked_es": "將原句依據語意群組，使用 / 分隔開來的句子。例如：Dudo que / el vuelo / salga / a tiempo",
  "analysis": [
    "解析點 1（例如：dudar que -> 表達懷疑 -> 觸發虛擬式）",
    "解析點 2"
  ],
  "vocab_list": [
    {"word": "單字1", "pos": "詞性（如 m., f., v., exp.）", "meaning": "中文意思"},
    {"word": "單字2", "pos": "詞性", "meaning": "中文意思"}
  ],
  "grammar_list": [
    {"point": "文法點名稱（如 Presente de Subjuntivo）", "desc": "簡短的一句文法說明"}
  ]
}

注意：請保持文字極簡，絕對不可包含任何粗體（**）、斜體（*）或圖示。
"""


def analyze_sentence(es_sentence, zh_meaning, grammar_tag):
    prompt = f"原句：{es_sentence}\n中文：{zh_meaning}\n預期語法：{grammar_tag}\n\n請依照指定JSON格式解析。"
    try:
        response = model.generate_content(
            contents=prompt,
            generation_config={"response_mime_type": "application/json", "temperature": 0.2},
            system_instruction=SYSTEM_PROMPT
        )
        return json.loads(response.text.strip())
    except Exception as e:
        print(f"API 解析失敗: {e}")
        return None


# ==================== 3. 處理 Excel 主程式 ====================
def process_weekly_excel(file_path, week_id, title_name):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    weekly_filename = f"{week_id}.md"
    weekly_file_path = os.path.join(WEEKLY_DIR, weekly_filename)

    weekly_content = []
    weekly_content.append(f"# {week_id} 西文檢視：{title_name}\n")
    weekly_content.append("## 學習概覽")
    weekly_content.append(f"主題：{title_name}")
    weekly_content.append("樣式規範：極簡文字，無粗斜體，無圖示\n")
    weekly_content.append("## 核心句型與拆解\n")

    # 欄位順序：類型(A), 編號(B), 西文句型(C), 中文意思(D), 核心語法標註(E)
    # 從第 11 行開始讀取數據，請根據實際 Excel 調整
    for row in range(11, sheet.max_row + 1):
        tipo = sheet[f'A{row}'].value
        no = sheet[f'B{row}'].value
        es_phrase = sheet[f'C{row}'].value
        zh_meaning = sheet[f'D{row}'].value
        grammar_tag = sheet[f'E{row}'].value

        if not no or not es_phrase:
            continue

        print(f"正在處理: {no}...")

        api_result = analyze_sentence(es_phrase, zh_meaning, grammar_tag)

        if api_result:
            chunked_es = api_result.get("chunked_es", es_phrase)
            analysis_lines = api_result.get("analysis", [])
            vocab_list = api_result.get("vocab_list", [])
            grammar_list = api_result.get("grammar_list", [])

            ghost_links = [f"[[{v['word']}]]" for v in vocab_list]
            ghost_links_str = ", ".join(ghost_links)

            weekly_content.append(f"類型：{tipo}")
            weekly_content.append(f"編號：{no}")
            weekly_content.append(f"西文斷句：{chunked_es}")
            weekly_content.append(f"中文意思：{zh_meaning}")
            weekly_content.append(f"核心語法標註：{grammar_tag}")
            weekly_content.append("句型拆解：")
            for line in analysis_lines:
                weekly_content.append(f"{line}")
            weekly_content.append(f"核心單字連結：{ghost_links_str}")
            weekly_content.append("\n---\n")

            # ---- Dictionary 原子卡片 ----
            for v in vocab_list:
                word_file = os.path.join(DICT_DIR, f"{v['word']}.md")
                if not os.path.exists(word_file):
                    with open(word_file, "w", encoding="utf-8") as f:
                        f.write(f"單字：{v['word']}\n")
                        f.write(f"詞性：{v['pos']}\n")
                        f.write(f"中文：{v['meaning']}\n")
                        f.write(f"來源週次：[[{week_id}]]\n")

            # ---- Grammar 原子卡片 ----
            for g in grammar_list:
                clean_point = re.sub(r'[\/*?:"<>|]', "", g['point'])
                grammar_file = os.path.join(GRAMMAR_DIR, f"{clean_point}.md")
                if not os.path.exists(grammar_file):
                    with open(grammar_file, "w", encoding="utf-8") as f:
                        f.write(f"語法點：{g['point']}\n")
                        f.write(f"說明：{g['desc']}\n")
                        f.write(f"出現週次：[[{week_id}]]\n")
                else:
                    with open(grammar_file, "a", encoding="utf-8") as f:
                        f.write(f", [[{week_id}]]")

    with open(weekly_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(weekly_content))
    print(f"{week_id} 自動化流程執行完畢！檔案已成功導入 Obsidian。")


# ==================== 4. 執行入口 ====================
if __name__ == "__main__":
    # 請確保運行目錄下有對應的 .xlsx 檔案
    process_weekly_excel("WK24範例.xlsx", "M6-WK24", "機場報到")
