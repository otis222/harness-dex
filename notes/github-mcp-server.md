---
slug: github-mcp-server
name: GitHub MCP Server
repo: github/github-mcp-server
slot: connector
summary: GitHub 官方的 MCP 伺服器，讓 agent 讀 repo、管理 issue 和 PR。
motto: "GitHub's official MCP Server"
difficulty: 2
tags: [MCP, 官方, 權限控管]
added: 2026-11-06
updated: 2026-11-06
status: published
---

## 它是什麼

GitHub MCP Server 是 GitHub 官方做的 MCP 伺服器，用 Go 寫成。接上之後，agent 可以用自然語言讀 repo 和程式碼、建立和管理 issue 與 pull request、查看 GitHub Actions 的執行結果和安全性警示。它有兩種用法：GitHub 代管的遠端伺服器（最簡單），或用 Docker 在自己的電腦上跑。

## 為什麼放在這一格

講義說連接器負責「把你的 App 接給 agent」，最常見的接法就是 MCP。這個專案是 GitHub 這個 App 的官方插頭：它不負責思考，也不是 agent，只把 GitHub 的功能包成 agent 能呼叫的工具，並處理登入與權限。它接的是一個外部服務和你的帳號，所以放在「連接器」，而不是「工具」。

## 解決什麼問題

想請 agent 幫忙整理 issue、看 CI 為什麼失敗，以前要把網頁內容複製給它，或讓它用指令列工具東拼西湊。接上 GitHub MCP Server 之後，可以直接說「列出這週新開、還沒有人回覆的 issue」，agent 會自己去查。

## 怎麼試

需求：一個支援 MCP 的 agent（官方列出 VS Code、Claude Code、Codex、Cursor 等），以及一組 GitHub Personal Access Token（PAT）。以下以 Claude Code 為例：

1. 到 GitHub 的設定頁建立 PAT，只勾你需要的權限。
2. 在終端機（不是在 Claude Code 裡面）執行下面這行，把 `YOUR_GITHUB_PAT` 換成你的 token：

```sh
claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer YOUR_GITHUB_PAT"}}'
```

3. 重新啟動 Claude Code，執行 `claude mcp list` 確認清單裡有 github。
4. 其他 agent 的設定方式，官方 repo 的 `docs/installation-guides/` 資料夾裡各有一份說明。

## 適合誰

- 常用 GitHub，想讓 agent 幫忙整理 issue、看 PR、追 CI 的人。
- 想實際體驗「連接器」的人：這是文件最齊全、最好接的官方範例之一。
- 不適合：還沒準備好管理 token 權限的人。權限給太大，agent 就能動到你所有的 repo。

## 注意事項

- PAT 只給最小權限。只想讓 agent 讀資料時，官方提供唯讀模式（`--read-only`），也能用 `--toolsets` 只開需要的功能組。
- 不要把 token 直接寫在指令或檔案裡提交出去；官方建議存在 `.env`，並把 `.env` 加進 `.gitignore`。
- issue 和 PR 的內容是別人寫的，裡面可能藏著想指揮 agent 的文字（提示注入）。讓 agent 讀公開 repo 時，特別注意它有沒有寫入權限。
- 各家 agent 的支援程度和需要的版本不同，以官方的安裝說明為準。

## 搭配裝備

- [[openbot]]：連接器決定 agent 能接上什麼，工作環境決定它在哪裡動手，兩邊的權限要一起設計。
- [[anydoc]]：同樣是替 agent 多一種能力；anydoc 處理你電腦裡的檔案，這裡則是接上遠端的服務。
- [[agents-md]]：讓 agent 透過 GitHub 開 PR 之前，在 repo 放一份 AGENTS.md，寫清楚標題格式和要跑的檢查。

## 資料來源

- [github/github-mcp-server](https://github.com/github/github-mcp-server)
- [Claude Code 安裝說明](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md)
- 查閱日期：2026-11-06
