---
slug: anatomy
name: Anatomy
repo: wheresryan22/anatomy
slot: skill
summary: 一個 agent 技能：把抽象概念畫成會動的等角機械圖解。
motto: "explains an idea by building it as a real, working object"
difficulty: 2
tags: [Agent Skill, SVG, 互動圖解]
homepage: https://skills.wheresryan.sh/anatomy
added: 2026-11-06
updated: 2026-11-06
status: published
---

## 它是什麼

Anatomy 是一個 Agent Skill，以 Claude 為主，也能在 Codex、OpenCode、Antigravity、MiniMax Code 使用。你請 agent 解釋一個技術概念，它會先「發明」一台運作原理剛好就是這個概念的機器，例如把「內容沒變就跳過重算」的快取，比喻成所有彈子都對齊才轉得動的鎖；再用幾十個零件把它畫成可以互動的等角圖解，輸出成 SVG、WebGL 或 3D（測試版）。

## 為什麼放在這一格

講義說技能是「一個資料夾加一份 SKILL.md，教 agent 某件事的標準做法」。Anatomy 的 repo 根目錄就是一份 `SKILL.md`，再加上繪圖腳本、參考資料和自我檢查流程。裝進 agent 之後，agent 就學會這一套固定的作圖做法。它不提供模型，也不接外部服務，所以放在「技能」。

## 解決什麼問題

請 AI 解釋技術概念，最常拿到的是一大段文字，或一張普通的流程圖。Anatomy 改成讓人「看見機制」：游標移上去，零件會動、數字跟著變。它畫完還會自己放大檢查每個接點有沒有畫錯。適合教學、簡報，或作品集裡的技術說明。

## 怎麼試

需求：Node.js，以及一個支援技能的 agent，例如 Claude Code。官方說不需要 API key，也不用另外安裝套件。

1. 安裝技能，過程中會問你要裝到哪些 agent：

```sh
npx skills add wheresryan22/anatomy -g
```

2. 在 Claude Code 裡輸入下面這行（Codex 改用 `$anatomy`）：

```text
/anatomy explain how a token bucket rate limiter works, interactive
```

3. 等它跑完，打開產生的 HTML 檔就能互動。

## 適合誰

- 要做技術簡報、教學圖解、作品集說明，又想要有設計感的人。
- 想看一份成熟的技能長什麼樣子的人：它的資料夾結構很適合當成自己寫技能的範本。
- 不適合：要畫統計圖表、人物或精確地圖的人。官方明講它不是圖表工具，也不畫人和地圖。

## 注意事項

- 官方說它「刻意很慢」：一張圖要跑好幾分鐘，3D 圖的完整檢查可能要 15 到 20 分鐘，會用掉不少 agent 的額度。
- 3D 模式還是測試版；光影效果需要瀏覽器支援 WebGL，不支援時仍會顯示 SVG 的部分。
- 想把作品分享到社群圖庫時，它會先問你、讓你看過要送出的內容，確認後才開 PR。

## 搭配裝備

- [[agents-md]]：技能教「怎麼做一件事」，規則檔講「這個專案的規矩」。在規則檔寫上「解釋機制時用 anatomy 畫圖」，兩者就串起來了。
- [[anydoc]]：anydoc 也發佈成技能，可以對照看「技能教 agent 怎麼用工具」和「技能本身就是一套做法」的差別。

## 資料來源

- [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy)
- [Anatomy 官方介紹頁](https://skills.wheresryan.sh/anatomy)
- 查閱日期：2026-11-06
