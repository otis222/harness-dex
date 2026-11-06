---
slug: anydoc
name: anydoc
repo: firecrawl/anydoc
slot: tool
summary: 把 Word、PowerPoint、Excel、PDF 等文件轉成乾淨 Markdown 的工具。
motto: "turn any office document into LLM-ready Markdown"
difficulty: 1
tags: [文件轉檔, Rust, Agent Skill]
homepage: https://firecrawl.github.io/anydoc/
added: 2026-11-06
updated: 2026-11-06
status: published
---

## 它是什麼

anydoc 是 Firecrawl 開源的文件轉換函式庫，用 Rust 寫成。它把 Word、PowerPoint、Excel、OpenDocument、RTF、EPUB、CSV、PDF 轉成格式一致的 Markdown，速度很快，並提供指令列工具、Node.js、Python 和瀏覽器（WebAssembly）幾種版本。它也包裝成一個 Agent Skill，裝了之後，agent 遇到文件就知道怎麼讀。

## 為什麼放在這一格

講義列的工具是「讀寫檔案、終端機、瀏覽器、搜尋」。模型本身讀不了 .pptx 或 .docx，anydoc 補上的正是「讀懂文件」這一項動手能力。它雖然也以技能的形式發佈，但技能只是教 agent 去呼叫這個轉換程式，真正做事的是程式本身，所以放在「工具」。

## 解決什麼問題

講義是 PPT、作業說明是 Word、資料是 Excel，要丟給 AI 之前，常常得手動複製貼上，表格和標題還會亂掉。anydoc 一個指令就把它們轉成 Markdown。例如課堂上 LLM Wiki 的 `raw/` 資料夾，就可以先用它把講義轉好再收錄。

## 怎麼試

需求：最快的方式只要瀏覽器；用指令列需要 Node.js。

1. 打開[線上示範頁](https://firecrawl.github.io/anydoc/)，拖一個檔案進去。官方說這個頁面用 WebAssembly 在瀏覽器裡轉換，檔案不會離開你的電腦。
2. 想在終端機用：

```sh
npx @firecrawl/anydoc report.docx
npx @firecrawl/anydoc slides.pptx -o slides.md
```

3. 想讓 agent 自己會用，安裝它的技能：

```sh
npx skills add firecrawl/anydoc
```

## 適合誰

- 常常要把講義、報告交給 AI 讀的學生。
- 在做 LLM Wiki 或 RAG，需要把一堆文件整理成文字的人。
- 寫程式的人：Node.js 和 Python 都能直接呼叫。
- 不適合：掃描版 PDF。那種檔案裡沒有文字，要另外做 OCR。

## 注意事項

- 掃描版 PDF 要開 OCR，而 anydoc 的 OCR 選項走的是 Firecrawl 的雲端服務（Firecrawl Parse），檔案會被上傳，機密文件要想清楚。
- 不開 OCR 時，指令列和線上示範頁都在本機轉換。
- 轉成 Markdown 會失去原本的版面和動畫，適合給 AI 讀，不適合拿來重新排版。

## 搭配裝備

- [[agents-md]]：在規則檔寫上「收到 .docx、.pptx 先用 anydoc 轉成 Markdown」，agent 每次都會照做。
- [[github-mcp-server]]：同樣是替 agent 多一種能力；anydoc 處理你電腦裡的檔案，GitHub MCP Server 則是接上遠端的服務。

## 資料來源

- [firecrawl/anydoc](https://github.com/firecrawl/anydoc)
- [anydoc 線上示範頁](https://firecrawl.github.io/anydoc/)
- 查閱日期：2026-11-06
