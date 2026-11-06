# NOTES.md — 現況白板

> 做到哪、下一步、待收錄。每次收工都更新；會變成長期規則的事，改寫進 AGENTS.md 並記 log.md。

最後更新：2026-11-06

## 下一步

- [ ] 確認 GitHub Pages 上線：https://otis222.github.io/harness-dex/ 每一頁都打得開（repo：https://github.com/otis222/harness-dex）。
- [ ] 第一次「更新數據」：一週後（2026-11-13 前後）。

## 目前收錄（9 件）

| 欄位 | 專案 |
|---|---|
| 大腦 | magpie |
| 整套 Harness | deepseek-harness |
| 工作環境 | openbot |
| 工具 | anydoc、moli |
| 連接器 | github-mcp-server |
| 技能 | anatomy |
| 規則檔 | agents-md |
| 排程 | aihot |

## 待收錄清單

已經大致看過、符合第 6 節門檻的候選，下次直接「收錄」：

- `Niko1221/Strata`：在一般電腦上跑本地模型 → 大腦
- `google-labs-code/design.md`：把視覺識別寫給 agent 看的 DESIGN.md 格式 → 規則檔
- `heydamir/unslop`：把 AI 味介面改成有設計感的技能 → 技能
- `google-research/harness2`：README 還沒讀 → 欄位待決定

## 待決定

- `oomol-lab/open-connector`（連接器）：內容扎實，但建立超過 90 天、星數未到 2 萬，不符合門檻。要收錄需要使用者同意。
- `gamedev-skills/awesome-gamedev-agent-skills`（技能）：遊戲開發技能合集，星數未到門檻。要收錄需要使用者同意。
- `nashsu/llm_wiki`：LLM Wiki 桌面 App，放「工具」還是「工作環境」？

## 不收紀錄

- 2026-11-06：篩選熱門榜時排除了越獄提示詞外掛 1 個、免登入使用付費模型的外掛 1 個、去除 AI 浮水印的工具 1 個（AGENTS.md 第 6 節）。

## 健檢紀錄

- 2026-11-06：`check.py` 0 個錯誤；警告：`data/site.json` 的網址還沒填（等上傳 GitHub）。
- 2026-11-06：實測——另開一個全新的 AI，只給「收錄 https://github.com/lexmount/moli」，照手冊做完、check 0 個錯誤。內容對照 README 審過後收進網站；它回報的 10 處不清楚已補進 AGENTS.md（見 log.md）。
