---
slug: deepseek-harness
name: DeepSeek Harness
repo: deepseek-ai/deepseek-harness
slot: harness
summary: DeepSeek 開源的 agent 程式，整套功能都由外掛組成。
motto: "Everything is a Plugin."
difficulty: 2
tags: [外掛架構, Web UI, 開發者預覽]
homepage: https://deepseek.com/harness
docs: https://deepseek-harness.github.io/deepseek-harness/
added: 2026-11-06
updated: 2026-11-06
status: published
---

## 它是什麼

DeepSeek Harness（指令名稱 `dsh`）是 DeepSeek 開源的 agent 程式。它的設計原則是「一切皆外掛」：底層用 Cordis 這套框架，把每一項功能都做成可以替換、組合的外掛。啟動後會開一個網頁介面，選好工作資料夾就能交辦任務，agent 會自己讀寫檔案、執行指令、擬定計畫。

## 為什麼放在這一格

講義的公式是 AI Agent ＝ AI Model ＋ Harness。DSH 就是公式右邊的那一整套：接下任務、呼叫工具、遇到需要核准的動作先停下來問你，再把結果交回模型判斷下一步。模型則是另外接上的，例如在設定裡填 DeepSeek 的 API key。它不是單一工具、也不是單一技能，而是一個拿來就能上工的完整 agent，所以放在「整套 Harness」。

## 解決什麼問題

上個單元用 AISuite 自己寫 agent 時，迴圈、工具、錯誤處理都要自己來。DSH 把這些包好了；又因為功能都是外掛，想加新能力時裝一個外掛就好，不用改核心程式。社群已經做出桌面版、外掛清單等周邊專案。舉例：拿到一個陌生的程式專案，選好資料夾後請它「摘要這個 repo，找出主要的套件」，它會自己去翻檔案再回報。

## 怎麼試

需求：Node.js，以及一組模型的 API key（官方文件以 DeepSeek 為例，也支援其他 OpenAI 相容服務）。

1. 在想讓它工作的資料夾開終端機，執行：

```sh
npx @deepseek-ai/dsh web
```

2. 瀏覽器會自動打開網頁介面，預設網址是 `http://127.0.0.1:3080`。
3. 到 **Settings → Models** 填入 API key 並儲存。
4. 按 **Choose workspace** 選擇工作資料夾，開一個 session，先試一句「幫我摘要這個資料夾的內容」。

> 先開一個空的練習資料夾來試，不要一開始就讓它碰重要的檔案。

## 適合誰

- 想看「整套 harness」實際長什麼樣、拆開來研究的人。
- 手上有 DeepSeek 或其他 OpenAI 相容服務的 API key，想要一個會自己動手的 agent。
- 會寫 TypeScript、想做外掛的人：官方有獨立的外掛開發文件。
- 不適合：需要穩定、不想遇到改版就壞掉的正式工作環境。

## 注意事項

- 官方標明這是開發者預覽版，之後的更新可能出現不相容的變動。
- 官方的安全說明寫得很直白：它會執行模型產生的程式碼和指令、載入第三方外掛，可能改到或刪掉檔案、外流資料；沙盒和確認提示只能降低風險，不能保證隔離。建議用虛擬機或容器、只給最小權限、先備份。
- 第三方外掛等於把程式碼交給別人執行，安裝前先看過來源。
- 模型的 API 用量會計費，跑長任務前先確認額度。

## 搭配裝備

- [[magpie]]：想替 agent 換不同的大腦時參考。magpie 示範了「同一套 harness、換不同模型」的做法，它支援哪些 agent 以官方清單為準。
- [[agents-md]]：DSH 自己的 repo 根目錄就放了 AGENTS.md，可以從這裡看 agent 進到專案時會先讀什麼。
- [[openbot]]：同樣是讓 agent 動手，OpenBot 的重點是替每個 agent 準備獨立的工作空間和行為紀錄，可以對照兩者分工。

## 資料來源

- [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
- [官方文件](https://deepseek-harness.github.io/deepseek-harness/)
- [安全說明 SAFETY.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/SAFETY.md)
- [Web UI 使用說明](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/index.md)
- [GitHub 主題：dsh-plugin](https://github.com/topics/dsh-plugin)
- 查閱日期：2026-11-06
