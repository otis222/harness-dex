---
slug: magpie
name: magpie
repo: yetone/magpie
slot: brain
summary: 一個本機閘道，替 Claude Code、Codex 等 agent 統一切換模型。
motto: "Every agent's model. One place."
difficulty: 2
tags: [模型切換, 本機閘道, 多帳號]
homepage: https://usemagpie.ai
docs: https://usemagpie.ai/docs/start
added: 2026-11-06
updated: 2026-11-06
status: published
---

## 它是什麼

magpie 是 yetone 開源的模型切換工具，用 Go 寫成。它在你的電腦上跑一個本機閘道，Claude Code、Codex、Gemini CLI、OpenCode 這些 agent 的模型請求都會經過它。你可以從選單列直接替每個 agent 換模型，例如讓 Claude Code 改用 Kimi、讓 Codex 改用 DeepSeek。

## 為什麼放在這一格

magpie 自己不是 agent，也不提供工具，它只處理公式左邊的 Model：harness 不動，把背後的大腦換掉。官方 README 舉的「Codex on DeepSeek」正好就是公式的示範：Codex 是 harness，DeepSeek 是大腦。所以它放在「大腦」，而不是「整套 Harness」。

## 解決什麼問題

每個 agent 都把模型設定藏在自己的設定檔裡，格式、金鑰、網址各不相同，付費方案也常常只能在自家的 agent 用。同時用兩三個 agent、好幾家模型時，光是切換設定就很麻煩。magpie 把這些集中到一個 App：選好模型，它會去改那個 agent 的設定；某個帳號的額度用完，它可以自動換下一個帳號或下一個模型，agent 那邊不會看到錯誤。

## 怎麼試

需求：macOS、Windows 或 Linux；至少一組模型供應商的 API key 或訂閱帳號；一個你已經在用的 agent，例如 Claude Code 或 Codex。

1. 到官方網站 [usemagpie.ai](https://usemagpie.ai) 下載 App；macOS 和 Linux 也可以在終端機執行：

```sh
curl -fsSL https://usemagpie.ai/install.sh | sh
```

2. 打開 magpie，到 **Providers → Add provider** 選一個預設的供應商，貼上 API key。
3. 到 **Agents** 頁面替某個 agent 選模型，開一個新的 session 就會用新的模型。

也可以全部用指令完成，例如讓 Claude Code 改用 DeepSeek：

```sh
magpie provider add deepseek sk-…
magpie claude deepseek/deepseek-v4-pro
```

## 適合誰

- 同時用好幾個 agent、好幾家模型的人。
- 想比較「同一個 agent 換不同大腦」表現差多少的人，很適合拿來做課堂實驗。
- 不適合：只用一個 agent、直接用該家方案就夠的人，官方 README 也這麼說。

## 注意事項

- 所有請求都會經過 magpie 的本機閘道。官方提供遮蔽功能（**Settings → Privacy**），能在送出前先在本機遮掉金鑰、密碼和 Email，但預設是關的。
- 把訂閱方案接到別家 agent 使用之前，先讀過該服務的使用條款。
- 它會改動 agent 的設定檔。官方說解除安裝時會把 agent 改回原樣，安裝前仍建議先備份設定。
- 模型用量一樣會計費；開了自動換帳號，記得留意每個帳號各自的用量。

## 搭配裝備

- [[deepseek-harness]]：一套完整的 harness，可以拿來對照「harness」和「大腦」各自負責什麼。
- [[agents-md]]：大腦換了，規則檔還是同一份。這正是把規則寫成檔案的好處。

## 資料來源

- [yetone/magpie](https://github.com/yetone/magpie)
- [magpie 官方網站](https://usemagpie.ai)
- [快速開始](https://usemagpie.ai/docs/start)
- 查閱日期：2026-11-06
