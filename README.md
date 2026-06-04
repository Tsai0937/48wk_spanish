# 48週西班牙文句型解析自動化系統

將每週西班牙文學習 Excel 檔案，自動分析並產生 Obsidian 筆記卡片。

---

## 資料夾結構

```
48wk_spanish/
├── process_weekly.py       ← 主腳本
├── requirements.txt        ← Python 套件需求
├── input/                  ← 每週上傳的 Excel 原始檔
│   ├── WK24.xlsx           ← 每週句型資料（50句）
│   └── WK25.xlsx           ← 48週課程規劃總表（用於產生主INDEX）
└── vault/                  ← 產出的 Obsidian 筆記
    └── Spanish/
        ├── ES_00_總覽.md   ← 48週主INDEX（從WK25.xlsx產生，只需一次）
        └── M06/            ← 每月一個資料夾（M01~M12）
            ├── ES_W24_index.md   ← 週INDEX（清單格式）
            ├── ES_W24-001.md     ← 句型卡片
            └── ES_W24-002.md ...
```

---

## 每張句型卡片的格式

```
Q | ES_W24-001

ES：原句（依語意用 / 斷句）
ZH：中文翻譯

句型解析：
1. 【主要子句】...
2. 【介系詞片語】...

文法：
1. Insistir en（Régimen preposicional）— 說明...

例句：
1. 西文例句（中文翻譯）
2. 西文例句（中文翻譯）

核心單字：[[insistir]] [[revisar]] ...
```

---

## 週INDEX格式（清單）

```markdown
# ES_W24：社交媒體與隱私

[[ES_00_總覽]]

---

[[ES_W24-001]]  Q
ES：¿Por qué insiste el director / en revisar...
ZH：主管為什麼還「堅持要」修改隱私政策？

---
```

---

## 命名規則

| 檔案 | 格式 | 範例 |
|---|---|---|
| 主INDEX | `ES_00_總覽.md` | `ES_00_總覽.md` |
| 週INDEX | `ES_W{WW}_index.md` | `ES_W24_index.md` |
| 句型卡片 | `ES_W{WW}-{NNN}.md` | `ES_W24-001.md` |
| 月份資料夾 | `M{MM}` | `M06` |

`ES_` 前綴確保 Obsidian vault 擴大後不與其他學習系統的連結打架。

---

## Excel 欄位格式（每週句型檔）

數據從第 **12 行**開始（第 11 行為標題）：

| 欄 | 內容 |
|---|---|
| A | 類型（Q/A/R/D） |
| B | 編號（M24-001） |
| C | 西班牙文句子 |
| D | 中文意思 |
| E | 核心語法重點 |

---

## ES 斷句規則（依優先順序）

| 優先 | 規則 | 說明 |
|---|---|---|
| 1 | 主從句邊界 | porque / si / que / cuando / aunque 等連接詞前切割 |
| 2 | 逗號位置 | 已有逗號處直接切，逗號保留在前段 |
| 3 | 介系詞片語 | en/de/por/para/con + 名詞組 獨立成群 |
| 4 | 不定詞補語 | 動詞固定搭配的 en/a/de + inf. 單獨成群 |
| 5 | 關係子句 | que/quien/donde 引導的修飾從句前切割 |
| 6 | 長名詞片語 | 超過 4 個詞的名詞片語單獨成群 |

底線原則：不可切斷「動詞 + 直接受詞」的核心結構。

---

## 每次 Session 執行流程

### 1. 提供 Gemini API Key
每次新 session 都需要重新提供（環境不保留）：
- 從 [aistudio.google.com](https://aistudio.google.com) 取得
- 使用模型：`gemini-2.0-flash`（免費方案每日 1500 次，50句綽綽有餘）
- 直接貼給 Claude，格式：`我的 API key 是：AIza...`

### 2. 上傳 Excel
將當週句型 Excel 放入 `input/` 資料夾。

### 3. 執行

**產生主INDEX（只需第一次，或課程規劃有更新時）：**
```python
# 取消 process_weekly.py 最後的註解：
generate_master_index("input/WK25.xlsx")
```

**每週執行：**
```python
# 修改 process_weekly.py 最後幾行：
process_weekly_excel("input/WK25.xlsx", month=7, week=25, title_name="學術討論與大學生活")
```

```bash
GEMINI_API_KEY="你的金鑰" python3 process_weekly.py
```

### 4. 同步到 Obsidian
將 `vault/Spanish/` 內容複製到：
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/西文48週X50句型解析/Spanish/
```
iCloud 自動同步到 iPad。

---

## Obsidian 連結說明

- `[[ES_00_總覽]]` — 從任何週INDEX返回主INDEX
- `[[ES_W24_index|W24：社交媒體與隱私]]` — 主INDEX連結到週INDEX（含顯示名稱）
- `[[ES_W24-001]]` — 週INDEX連結到句型卡片
- `[[insistir]]` — 核心單字 ghost link（未來可建立單字卡）
