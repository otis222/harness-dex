---
slug: moli
name: Moli
repo: lexmount/moli
slot: tool
summary: 專為 AI agent 做的無頭瀏覽器，平常只處理網頁結構，需要時才排版、繪製畫面。
motto: "Structure first. Pixels on demand."
difficulty: 2
tags: [無頭瀏覽器, 網頁擷取, Rust, Agent Skill]
homepage: https://browser.lexmount.com/moli
added: 2026-11-06
updated: 2026-11-06
status: published
---

## 它是什麼

Moli 是 Lexmount 開源的無頭瀏覽器，也就是沒有視窗、專門讓程式操作的瀏覽器，主打給 AI agent 使用。它不是把 Chromium 包一層，而是用 Rust 自己組起來的瀏覽器核心：JavaScript 交給 V8 執行，CSS 用 Servo 專案的元件處理。最核心的特色就寫在標語裡：平常只維護網頁的結構（DOM），不排版也不畫圖；要截圖或取得元素的實際位置時，加上 `--layout` 選項，它才會臨時排版、繪製畫面。用法有兩種：用指令列一次抓一個網頁，輸出成 Markdown、截圖或 PDF；或開一個伺服器，讓 Playwright 這類自動化工具連進來操作。

## 為什麼放在這一格

講義列的工具是「讀寫檔案、終端機、瀏覽器、搜尋」，Moli 補上的正是瀏覽器這一項：讓 agent 能打開網頁、讀內容、點按鈕、截圖，搭配官方技能也能搜尋網頁。repo 裡附了三個技能（抓網頁、搜尋、開自動化伺服器），但技能只是教 agent 怎麼呼叫 `moli` 這支程式，真正做事的是瀏覽器本身，這點和 anydoc 一樣。它也不是「工作環境」：它不替 agent 準備能存檔、跑程式的獨立空間，只提供上網這一種能力，所以放在「工具」。

## 解決什麼問題

很多網頁的內容要等 JavaScript 跑完才出現，只下載 HTML 會拿到一個空殼；改用 Chrome 的無頭模式雖然讀得到，但每開一個都要佔用不少記憶體，同時開很多個時負擔很重。Moli 保留完整的 JavaScript 和 DOM，但預設不排版、不畫圖。官方 README 的測試裡，抓同一批公開網頁時，它成功抓到的頁數和 Chrome 無頭模式差不多，記憶體用量卻只有十分之一左右。舉例：請 agent 整理系上網站的最新公告，它可以用一個 `moli fetch` 指令把頁面轉成 Markdown 來讀，不必先開一整個 Chrome。

## 怎麼試

需求：Linux、macOS 或 Windows 電腦，不用另外安裝 Chrome；README 說開源版不需要 Lexmount 的雲端服務就能完整使用。第 3 步要用 Playwright 連線的話，還要先裝好 Playwright（README 的範例是 Node.js 版）；想走第 4 步「交給 agent 安裝」，則要有一個支援技能的 coding agent。

1. 安裝。Linux 或 macOS 在終端機執行：

```sh
curl --proto '=https' --tlsv1.2 -fsSL \
  https://github.com/lexmount/moli/releases/latest/download/moli-installer.sh | sh
```

Windows 則在 PowerShell 執行：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://github.com/lexmount/moli/releases/latest/download/moli-installer.ps1 | iex"
```

2. 把一個網頁轉成 Markdown 印出來：

```bash
moli fetch \
  --dump markdown \
  --wait-until done \
  https://example.com
```

3. 想用 Playwright 這類工具操作，先啟動自動化伺服器：

```bash
moli serve
```

伺服器的網址是 `http://127.0.0.1:9222`，Playwright 可以用 `connectOverCDP` 直接連上去，完整範例在 README 的「Start the automation server」。

4. 也可以照 README 的「Quick start」，把下面這段話交給你的 agent，讓它自己裝好技能和 Moli，再抓一個網頁給你看：

```text
Install the skills under https://github.com/lexmount/moli/tree/main/skills,
follow their instructions to download and install the latest prebuilt Moli
binary, then use moli-webfetch to fetch https://example.com and show me the
result.
```

> 裝好後如果終端機找不到 `moli` 指令，官方技能說明提到 Linux 和 macOS 預設裝在 `~/.local/bin/moli`，Windows 則是 `%LOCALAPPDATA%\Moli\bin\moli.exe`。

## 適合誰

- 想讓 agent 上網查資料、讀動態網頁的人。
- 要大量抓網頁，或想在同一台電腦上同時開很多個瀏覽器的人：省資源正是它的主打。
- 已經在用 Playwright 或 Puppeteer 的人：它支援 CDP，可以拿來替換原本的 Chromium 試試看。
- 不適合：需要畫面和 Chrome 逐像素一致，或要精準呈現 Canvas、WebGL、影音的情境，官方明講不追求這些；也不適合想要一個有視窗、能自己點來點去的瀏覽器的人。

## 注意事項

- 網頁內容是別人寫的，裡面可能藏著想指揮 agent 的文字（提示注入）。官方技能要求把抓回來的內容當成資料，不照網頁上的指示做；在安全要求高的環境抓來路不明的網址時，官方建議加上 `--block-private-networks`，擋掉連往內部網路的請求。
- 安裝方式是直接執行網路上的腳本；走「交給 agent」那條路時，則是 agent 自己下載並執行程式。先看過腳本內容，或在虛擬機、容器裡試。
- 成熟度：官方 README 說它在自己定義的 agent 瀏覽器情境裡已經可以正式使用，但仍在積極開發。官方技能說明提醒它只支援一部分 CDP 功能，不是和 Chrome 完全相容；README 則說遇到不支援的操作會直接回報錯誤，不會假裝做到了。README 引用的 Lexbench 測試（Lexmount 自己做的）裡，Moli 0.1.1 版的任務成功率約八成，Chrome 接近百分之百。
- repo 上標示的網址是 Lexmount Browser 的首頁，那是 Lexmount 以 Moli 為核心另外經營的雲端服務，要註冊帳號，有免費方案也有付費方案；只用開源版不需要它。Lexmount 網站上專門介紹開源 Moli 的是另一頁，連結見資料來源。
- 授權：README 寫明可以從兩種開源授權中擇一使用，第三方元件另有各自的授權，細節見 [README 的 License 段落](https://github.com/lexmount/moli#license)。另外，抓別人的網站要遵守對方的使用規範，官方技能也明講不可繞過登入、付費牆和驗證碼。

## 搭配裝備

- [[anydoc]]：同一格的兩個工具剛好互補，anydoc 負責你電腦裡的 Word、PDF，Moli 負責網路上的網頁；兩個一起裝，agent 讀檔案和讀網頁都能拿到 Markdown。
- [[agents-md]]：在規則檔寫上「要讀網頁時，先用 Moli 轉成 Markdown」，agent 就知道該用它；Moli 自己的 AGENTS.md 整份只有一條規矩（改了 Rust 程式或建置設定，提交前先跑完格式、靜態檢查和測試），可以當成精簡規則檔的範例。

## 資料來源

- [lexmount/moli](https://github.com/lexmount/moli)
- [Moli README：Benchmark 段落](https://github.com/lexmount/moli#benchmark)
- [moli-webfetch 技能說明](https://github.com/lexmount/moli/blob/main/skills/moli-webfetch/SKILL.md)
- [moli-cdp-server 技能說明](https://github.com/lexmount/moli/blob/main/skills/moli-cdp-server/SKILL.md)
- [Moli 的 AGENTS.md](https://github.com/lexmount/moli/blob/main/AGENTS.md)
- [Moli 官方介紹頁](https://browser.lexmount.com/moli)
- [Lexmount Browser 官方網站](https://browser.lexmount.com)
- [Lexmount Browser 價格方案](https://browser.lexmount.com/pricing)
- 查閱日期：2026-11-06
