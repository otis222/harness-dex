# Harness 圖鑑

收錄 GitHub 上正熱門的 AI Agent 開源專案，照課堂公式「AI Agent ＝ Model ＋ Harness」分成 8 個裝備欄位，一個專案一頁說明書。

- 網站：見 `data/site.json` 的 `site_url`（GitHub Pages）
- 規則手冊：[AGENTS.md](AGENTS.md)。Claude Code 透過 [CLAUDE.md](CLAUDE.md) 匯入同一份。

這是 TAICA「生成式 AI：文字與圖像生成的原理與實務」第九週的作業：寫一份規則手冊，讓 AI 照同一套方式持續新增頁面。

## 交給 AI 新增一個專案

打開 Codex、Claude Code 或其他會讀 AGENTS.md 的 agent，在這個資料夾裡對它說：

```text
收錄 https://github.com/owner/repo
```

它會照 AGENTS.md 4.1 的步驟：檢查收錄標準、抓數據快照、讀 README、寫收錄稿、產生網頁、跑健檢，最後更新 NOTES.md 並回報。另外兩個指令是「更新數據」和「健檢」。

## 自己動手

需要 Python 3.9 以上，不用安裝任何套件。沒有 `python` 指令時，macOS／Linux 改打 `python3`，Windows 改打 `py`。

```sh
python tools/snapshot.py owner/repo   # 抓 GitHub 數據快照到 raw/
python tools/build.py                 # 用 notes/ 和 raw/ 產生網頁
python tools/check.py                 # 健檢，錯誤要修到 0 個
python -m http.server 8000            # 本機預覽：http://localhost:8000/
```

## 資料夾

| 位置 | 內容 | 誰來改 |
|---|---|---|
| `AGENTS.md` | 規則手冊 | 人和 AI 一起 |
| `notes/` | 每個專案的收錄稿（Markdown） | AI 寫、人審 |
| `raw/` | GitHub 數據快照（JSON），只增不改 | `tools/snapshot.py` |
| `pages/` | 「這個網站怎麼長出來的」原稿 | 人和 AI |
| `templates/`、`assets/` | 版型、樣式、圖示 | 改版型時才動 |
| `index.html`、`entries/`、`about/`、`data/entries.json`、`llms.txt` | 網頁成品 | `tools/build.py` 產生，不手改 |
| `NOTES.md`、`log.md` | 現況白板、決策紀錄 | 每次收工更新 |

## 說明

各專案的名稱、商標與內容屬於原作者；本站只做介紹，數據來自 GitHub API，星數每天都在變，以 GitHub 上的為準。
