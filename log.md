# log.md — 決策紀錄

> 只記會改變之後做法的決定。最新的放最上面，只增不刪。格式見 AGENTS.md 第 12 節。

---

## 2026-11-06｜新 AI 試跑後，補清楚 10 處規則
- 改了什麼：另開一個沒參與過的 AI，只交辦「收錄 https://github.com/lexmount/moli」。它照手冊做完（check 0 個錯誤），並回報 10 處得自己判斷的地方，全部補進 AGENTS.md：4.1 第 2、4 步的順序（先初判，門檻以快照確認）、第 5 步不算雲端服務的文件、第 9 步要改 NOTES.md 的哪兩段；第 2 節的欄位邊界（工作環境／工具／技能／連接器）；5.1 標語找法、`homepage` 填專案自己的頁面、上手難度 1 和 2 的界線；5.2 授權寫法、「搭配裝備」可以寫一起用或對照；第 6 節「不收」只看 repo 本身；第 9 節官方測試數字的寫法；第 12 節 NOTES.md 的段落清單。順手把第 2 節表格的連接器範例改成 github-mcp-server，並在 AGENTS.md、CLAUDE.md、README.md 補上 `python3` 的說明。
- 為什麼：規則要讓沒看過這個專案的 AI 也能照做；試跑時卡住的地方，就是手冊沒寫清楚的地方。
- 影響哪些檔案：`AGENTS.md`、`CLAUDE.md`、`README.md`、`NOTES.md`、`pages/about.md`；新增 `notes/moli.md`、`raw/moli/`（試跑的成品，對照 README 審過）。

## 2026-11-06｜連接器改收 GitHub MCP Server
- 改了什麼：連接器原本的候選 `oomol-lab/open-connector`，換成 `github/github-mcp-server`。
- 為什麼：open-connector 建立超過 90 天、星數未到 2 萬，不符合第 6 節的收錄門檻。照規則換成符合門檻的官方範例，而不是為了它放寬規則。
- 影響哪些檔案：`notes/github-mcp-server.md`、`raw/github-mcp-server/`；open-connector 移到 NOTES.md 的「待決定」。

## 2026-11-06｜摘要長度的算法寫清楚
- 改了什麼：AGENTS.md 5.1 的 `summary` 上限改成「中文一字算一字、英文一個單字算一字」。
- 為什麼：中英混寫時「40 字」有兩種算法，check.py 需要一個明確的標準。
- 影響哪些檔案：`AGENTS.md`、`tools/check.py`。

## 2026-11-06｜建立專案
- 改了什麼：建立規則（AGENTS.md）、收錄稿（notes/）、數據快照（raw/）三層，加上 snapshot、build、check 三支工具；首批收錄 8 個專案，每個欄位 1 件。
- 為什麼：第九週作業要的是一套能重複使用的規則。分層借用課堂上的 LLM Wiki：規則、原始資料、AI 寫的頁面。
- 影響哪些檔案：全部。
