# 48週西班牙文句型解析自動化系統

將每週西班牙文學習 Excel 檔案，自動分析並產生 Obsidian 筆記卡片。

---

## 資料夾結構

```
48wk_spanish/
├── process_weekly.py    ← 主腳本（唯一需要維護的程式）
├── requirements.txt     ← Python 套件需求
├── input/               ← 每週上傳的 Excel 原始檔
│   ├── WK24.xlsx
│   └── WK25.xlsx ...
└── output/              ← 產出的 Obsidian 筆記，每週一個子資料夾
    ├── M6-W24/
    │   ├── M6-W24_index.md    ← 本週索引（50句總覽表格）
    │   ├── M6-W24-001.md      ← 句子卡片
    │   └── M6-W24-002.md ...
    └── M6-W25/ ...
```

---

## 每張句子卡片的格式

```
Q | M6-W24-001

ES：原句（依語意用 / 斷句）
ZH：中文翻譯

句型解析：
1. 【主要子句】...
2. 【介系詞片語】...

文法：
1. Insistir en（Régimen preposicional）— 說明...
2. ...

例句：
1. 西文例句（中文翻譯）
2. 西文例句（中文翻譯）

核心單字：[[insistir]] [[revisar]] ...
```

---

## ES 斷句規則（系統化，依優先順序）

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

## Excel 欄位格式

數據從第 **12 行**開始（第 11 行為標題）：

| 欄 | 內容 |
|---|---|
| A | 類型（Q/A/R/D） |
| B | 編號（M24-001） |
| C | 西班牙文句子 |
| D | 中文意思 |
| E | 核心語法重點 |

---

## 使用方式

### 環境設定（首次）
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="你的金鑰"
```

### 每週執行
```python
# 修改 process_weekly.py 最後幾行：
process_weekly_excel("input/WK25.xlsx", month=6, week=25, title_name="本週主題")
```

```bash
python process_weekly.py
```

產出檔案位於 `output/M6-W25/`，複製到 Obsidian iCloud 資料夾即可同步到 iPad。

---

## Obsidian 資料夾位置（Mac + iCloud）

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/西文48週X50句型解析/
```

---

## 週次編號邏輯

`M6-W24-001` = 第 **6** 個月 / 第 **24** 週 / 第 **001** 句
