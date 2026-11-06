---
slug: agents-md
name: AGENTS.md
repo: agentsmd/agents.md
slot: rules
summary: 一個開放格式：在專案裡放一份給 coding agent 讀的說明書。
motto: "a README for agents"
difficulty: 1
tags: [開放格式, 規則檔, 跨工具]
homepage: https://agents.md
added: 2026-11-06
updated: 2026-11-06
status: published
---

## 它是什麼

AGENTS.md 是一個開放格式，這個 repo 則是推廣它的官方網站原始碼。概念很簡單：在專案根目錄放一個叫 `AGENTS.md` 的 Markdown 檔，寫給 AI coding agent 看，內容是怎麼裝環境、怎麼跑測試、提交前要注意什麼。官方把它比喻成「給 agent 看的 README」：README 寫給人，AGENTS.md 寫給 agent。

## 為什麼放在這一格

這一格就是講義裡的「員工手冊」。AGENTS.md 不是程式，而是大家約定好的檔名和寫法，讓不同的 agent 都知道「進到這個專案，先讀哪一份」。它跟用哪顆大腦、哪套 harness 無關，所以放在「規則檔」。

## 解決什麼問題

以前每個 agent 都有自己的規則檔名稱，同一個專案要為不同工具各寫一份，內容還很容易不同步。AGENTS.md 讓大家共用同一份。GitHub 在 2026 年的 Octoverse 報告提到：今年新建的 repo 裡，有 agent 設定檔的平均 commit 數，是沒有的 8 倍。這不代表有手冊就一定做得好，但看得出越來越多專案把規則寫成檔案。

## 怎麼試

需求：一個專案資料夾，和任何一個支援 AGENTS.md 的 coding agent。

1. 在專案根目錄新增 `AGENTS.md`，先寫三段就好：

```markdown
# AGENTS.md
## 開發環境
- 用什麼工具、怎麼安裝
## 測試方式
- 改完要跑哪些檢查
## 提交前
- 標題格式、哪些事不能做
```

2. 打開你的 agent，交辦一件小事，觀察它有沒有照手冊做。
3. 用 Claude Code 的話：新版在專案裡沒有 CLAUDE.md 時會直接讀 AGENTS.md；如果同時有 CLAUDE.md，在裡面寫一行 `@AGENTS.md` 匯入，兩邊就只要維護一份。

## 適合誰

- 每一個想讓 AI 幫忙做專案的人，不論用哪個 agent。
- 正在寫這份作業的同學：本站就是用一份 AGENTS.md 長出來的，可以打開[這個網站怎麼長出來的](../../about/)對照。
- 不適合：期待「寫了規則，agent 就一定照做」的人。規則檔是提醒，不是強制；要強制，還是得靠測試或檢查腳本。

## 注意事項

- 檔案放在 repo 根目錄，檔名是大寫的 `AGENTS.md`；子資料夾也可以有自己的一份。
- 寫太長反而會稀釋重點，只寫 agent 猜不到、又真的會影響結果的規則。
- 不要在規則檔裡放密碼或金鑰：它會被提交進 repo，也會被送進模型。
- 各家工具讀取的細節不一樣，例如 Claude Code 同時遇到 CLAUDE.md 時的行為，以各工具的官方文件為準。

## 搭配裝備

- [[magpie]]：大腦可以換，規則檔還是同一份。
- [[aihot]]：AIHOT 的 README 建議把整個 repo 交給 agent，請它先讀 AGENTS.md 再改成你自己領域的版本，是規則檔實際派上用場的例子。
- [[anatomy]]：技能教「怎麼做一件事」，規則檔講「這個專案的規矩」，兩者常一起出現。

## 資料來源

- [agentsmd/agents.md](https://github.com/agentsmd/agents.md)
- [AGENTS.md 官方網站](https://agents.md)
- [Claude Code 文件：How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [GitHub Octoverse 2026](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/)
- 查閱日期：2026-11-06
