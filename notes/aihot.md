---
slug: aihot
name: AIHOT
repo: KKKKhazix/AIHOT
slot: schedule
summary: 每天定時找熱點、自己寫日報的網站框架，可以改成任何領域的版本。
motto: "一个自己找热点、自己写日报的网站框架。"
difficulty: 3
tags: [定時任務, 日報, 自架]
homepage: https://aihot.news
added: 2026-11-06
updated: 2026-11-06
status: published
---

## 它是什麼

AIHOT 是一個中文的 AI 熱點網站，這個 repo 是它背後的引擎和網站框架。它每天從一批資訊來源收集資料，先用大型語言模型篩選、再獨立評分兩次，替入選的消息寫標題和摘要，把不同來源講的同一件事合併成一個「事件」，再依熱度排序。每天早上出日報，每週、每月再彙整成週報和月報。作者是設計師出身，在 README 裡說這套程式是和 AI 一起重寫的。

## 為什麼放在這一格

講義說排程是「時間到了，自己開工」。AIHOT 的核心就是一串定時發生的工作：抓資料、評分、出刊。日報預設每天早上八點，週報和月報也有固定時間，都不需要有人下指令。模型可以換、資料來源也可以換，不變的是這套定時流程，所以放在「排程」。

## 解決什麼問題

想追一個領域的新消息，每天要自己逛好幾個網站、看一堆重複的報導。AIHOT 把「找、篩、寫、排」全部自動化，而且篩選標準和提示詞都公開在 repo 裡，可以照自己的需要改。例如想做一個遊戲開發新聞站，換成遊戲業的資訊來源和評分標準就好。

## 怎麼試

需求：Docker、Node.js 24、一組 OpenAI 相容的模型 API key（官方預設用 DeepSeek，也支援千問、智譜等）。

1. 下載程式並產生設定檔：

```sh
git clone https://github.com/KKKKhazix/AIHOT.git myhot
cd myhot
node scripts/init-env.ts --llm-key <你的模型 API Key>
```

2. 啟動：

```sh
docker compose up -d --build
```

3. 打開 `http://localhost:3000`；後台在 `/admin`，管理員密碼在 `.env` 的 `ADMIN_PASSWORD`。第一次匯入的資料大約要半小時處理完。
4. 想改成自己的領域：官方建議把 repo 交給你的 agent，請它先讀 `AGENTS.md` 和 `docs/customize.md`，再告訴它你想追的來源和判斷標準。

## 適合誰

- 想替社團、系學會或某個領域做資訊整理站的人。
- 想研究定時任務、內容篩選、事件合併怎麼做的人：提示詞和入選門檻全部公開。
- 不適合：沒有伺服器、或不想長期付模型費用的人。它要一直開著，才會定時運作。

## 注意事項

- 每天都會呼叫模型，費用會持續累積；後台有付費服務的預算上限保護，記得先設定好。
- 資料來源要換成你自己的，並遵守各來源網站的使用規範。
- 作者要求不要使用 AIHOT 的名稱和 Logo，請換上自己的站名。
- 介面和文件是簡體中文。開源版是線上網站引擎的匯出版本，作者也說明無法保證每次更新都同步過來。

## 搭配裝備

- [[agents-md]]：AIHOT 的客製化方式就是「讓 agent 先讀 AGENTS.md 再動手」，是規則檔最實際的用法。

## 資料來源

- [KKKKhazix/AIHOT](https://github.com/KKKKhazix/AIHOT)
- [AIHOT 網站](https://aihot.news)
- 查閱日期：2026-11-06
