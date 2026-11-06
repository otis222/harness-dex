---
slug: openbot
name: OpenBot
repo: CopilotKit/OpenBot
slot: workspace
summary: 可以架在自己機器上的 AI 同事範本，每個 agent 都有自己的瀏覽器和檔案。
motto: "The AI assistant your company can actually own."
difficulty: 3
tags: [自架, 行為紀錄, AG-UI]
homepage: https://www.copilotkit.ai/openbot
added: 2026-11-06
updated: 2026-11-06
status: published
---

## 它是什麼

OpenBot 是 CopilotKit 開源的「AI 同事」平台範本。介面和 ChatGPT 很像，但整套系統跑在你自己的機器或伺服器上。每位 AI 同事有自己的瀏覽器（連登入狀態都是它自己的）、自己的檔案，以及你允許它用的工具；它在自己的畫面上工作，你可以在旁邊看，遇到它不該自己決定的事，可以接手操作再交還給它。

## 為什麼放在這一格

講義說工作環境是 agent「自己的電腦」。OpenBot 做的就是這件事：替每個 agent 準備獨立的瀏覽器、檔案和工具權限，每個動作在執行前先經過決定、執行後留下紀錄。它透過 AG-UI 協定接上各種 agent，不綁定特定的大腦或 harness，所以放在「工作環境」。

## 解決什麼問題

讓 agent 直接用你的電腦和帳號做事，風險很高：你所有的檔案和登入狀態它都碰得到。團隊想導入 AI 同事時，還需要知道「它到底做了什麼」。OpenBot 把每個 agent 關在各自的工作空間，只給需要的工具，並把動作記錄下來。例如讓「知識庫」同事只回答公司文件相關的問題，不碰其他系統。

## 怎麼試

需求：Docker、[Bun](https://bun.sh)、CopilotKit 帳號（官方說免費的 Developer 方案可以在 Mac 上本機執行），以及一組模型 API key。步驟比較多；官方建議如果請 AI 助理幫忙安裝，先把 repo 裡的 `prompt.txt` 貼給它。

1. 把 repo 下載到電腦後，在資料夾裡建立設定檔並安裝套件：

```sh
cp .env.example .env
bun install
```

2. 登入 CopilotKit 並選擇專案：

```sh
npx --yes copilotkit@latest login
npx --yes copilotkit@latest project select
bun scripts/setup-learning.ts
```

3. 接下來照 README「Quick start」的後續步驟啟動服務。

## 適合誰

- 想研究「怎麼安全地給 agent 一台自己的電腦」的人。
- 想在團隊裡導入 AI 同事，需要權限控管和行為紀錄的人。
- 想看生成式介面實作的人：它的 agent 會用介面元件回答，不只是文字。
- 不適合：只想在自己電腦上快速試試 agent 的人，需要的帳號和設定步驟比較多。

## 注意事項

- 官方定位是「範本，不是產品」：沒有線上版可以註冊，要 clone 下來改成自己的版本。
- 目前是 beta，官方提醒會有問題，功能也還會變動。
- 預設是單人模式（`OPENBOT_SINGLE_USER=true`），所有請求都當成管理員處理；讓別人連進來之前，一定要先設定登入。
- 需要 CopilotKit 帳號；模型要自己提供，用量會計費。

## 搭配裝備

- [[deepseek-harness]]：DSH 是一整套 harness；OpenBot 專心處理「agent 在哪裡工作、能碰什麼」，兩者關注的層次不同。
- [[github-mcp-server]]：連接器決定 agent 能接上哪些服務，工作環境決定它在哪裡動手。兩邊的權限要一起設計，才不會漏洞百出。

## 資料來源

- [CopilotKit/OpenBot](https://github.com/CopilotKit/OpenBot)
- [OpenBot 官方介紹頁](https://www.copilotkit.ai/openbot)
- 查閱日期：2026-11-06
