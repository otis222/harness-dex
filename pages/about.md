---
title: 這個網站怎麼長出來的
summary: Harness 圖鑑的每一頁，都是 AI 照著同一份 AGENTS.md 做出來的。人負責挑專案、審稿和驗收。
---

## 一份手冊，管整個網站

這個網站的規矩全部寫在 repo 根目錄的 `AGENTS.md`：收錄哪些專案、放進哪個裝備欄位、每頁固定寫哪 8 段、什麼不能做、做完要檢查什麼。接手的 AI 不論是 Codex、Claude Code 還是 DeepSeek Harness，開工前都先讀這一份，所以做出來的頁面長得一樣、寫法一致。

## 收錄一個新專案

[[diagram:pipeline]]

這個分工借用了課堂上的 LLM Wiki：

- **規則**：`AGENTS.md`。人和 AI 一起寫，規則有變就在 `log.md` 記一筆。
- **原始資料**：`raw/` 裡的 GitHub 數據快照，由 `tools/snapshot.py` 產生，只增不改。網頁上的星數、日期、授權全部從這裡讀，AI 不會自己打數字。
- **收錄稿**：`notes/` 裡每個專案一份 Markdown，是 AI 讀完 README 和官方文件後寫的說明書原稿。
- **網頁**：`tools/build.py` 把收錄稿和快照組合成網頁。網頁不手改；要改內容就改收錄稿，再重新產生。

## 只要三句話

收錄一個新專案：

```text
收錄 https://github.com/owner/repo
```

更新所有專案的數據，順便修正過時的說法：

```text
更新數據
```

全站健檢，找出過期的快照、失效的連結和不再成立的說法：

```text
健檢
```

每一句背後的完整步驟，都寫在 `AGENTS.md` 第 4 節。

## 規則檔只是提醒，所以要有健檢

寫在手冊裡的規則，AI 不一定每次都照做。這個網站用 `tools/check.py` 把規則變成可以驗收的項目：

- 每份收錄稿的欄位是否齊全，8 個段落的順序對不對。
- 「搭配裝備」連到的條目是否真的存在。
- 正文裡有沒有手打的星數。
- 有沒有混進簡體字。
- 網頁是不是最新的：檢查腳本會自己重新產生一次網頁，和 repo 裡的版本逐一比對。

錯誤要修到 0 個，才算完成。

## 實測：換一個 AI 照手冊做

規則寫得清不清楚，要換一個沒參與過的 AI 來做才知道。網站建好後，另外開了一個全新的 AI 工作階段，只給它這個資料夾和一句話：

```text
收錄 https://github.com/lexmount/moli
```

另外只補充了執行環境的事（例如這台電腦的 Python 指令叫 `python3`），並請它回報手冊哪裡寫得不清楚。

- **結果**：它照 `AGENTS.md` 4.1 的十個步驟做完：抓快照、讀 README 和官方技能說明、判斷放「工具」、寫收錄稿、產生網頁、更新 `NOTES.md`，健檢 0 個錯誤。成品就是 [[moli]] 這一頁，對照原始 README 審過後收進網站。
- **它卡住的地方**：它列出 10 處得自己判斷的地方，例如收錄門檻寫「以快照為準」，這一步卻排在抓快照之前；上手難度 1 和 2 的界線不清楚；標語該從哪裡找沒有說。這些都補進了 `AGENTS.md`，並在 `log.md` 記了一筆。下一個接手的 AI 遇到同樣的情況，就不用再猜。

## 為什麼要把規矩寫下來

GitHub 在 2026 年 10 月發表的 Octoverse 報告提到：到 2026 年 9 月，超過四成的 pull request 是 agent 先寫出第一版；今年新建的 repo 裡，有 agent 設定檔的平均 commit 數是沒有的 8 倍。agent 越常動手，「把規矩寫成檔案」就越像專案的基本功。

資料來源：[GitHub Octoverse 2026](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/)
