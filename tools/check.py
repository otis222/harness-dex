"""健檢：把 AGENTS.md 的規則變成可以驗收的項目。

用法：python tools/check.py

✗ 錯誤：一定要修到 0 個才算完成。
! 警告：要看過，能修就修；修不了就寫進 NOTES.md 的「健檢紀錄」。
全部沒有錯誤時，結束碼是 0。
"""
from __future__ import annotations

import os
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as builder  # noqa: E402
import hdx  # noqa: E402

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
STAR_RE = re.compile(r"\d[\d,.]*\s*(萬|千|[kK])?\s*(顆星|stars?|⭐|星)")
PUNCT_RE = re.compile(r"[一-鿿][,;:?!]|[,;:?!][一-鿿]")
KNOWN_FIELDS = set(hdx.REQUIRED_FIELDS) | set(hdx.OPTIONAL_FIELDS)
SECTION_NAMES = [name for name, _ in hdx.SECTIONS]

errors: list[tuple[str, str]] = []
warnings: list[tuple[str, str]] = []


def err(where: str, msg: str) -> None:
    errors.append((where, msg))


def warn(where: str, msg: str) -> None:
    warnings.append((where, msg))


def as_date(s) -> date | None:
    if not isinstance(s, str) or not DATE_RE.match(s):
        return None
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def prose(md: str) -> str:
    """去掉程式碼、網址與連結目標，只留下要給人讀的文字。"""
    md = hdx.strip_code(md)
    md = re.sub(r"\]\([^)]*\)", "]", md)
    return re.sub(r"https?://\S+", "", md)


def length_units(s: str) -> int:
    """中文一字算一字、英文一個單字算一字。"""
    return hdx.cjk_count(s) + hdx.word_count(s)


# ---------------------------------------------------------------- 設定檔

def check_config(slots: list[dict]) -> None:
    ids = [s.get("id") for s in slots]
    if len(ids) != len(set(ids)):
        err("data/slots.json", "欄位 id 重複")
    for s in slots:
        for key in ("id", "name", "zone", "blurb"):
            if not s.get(key):
                err("data/slots.json", f"欄位 {s.get('id', '?')} 缺少 {key}")
        if s.get("zone") not in ("model", "harness"):
            err("data/slots.json", f"欄位 {s.get('id')} 的 zone 只能是 model 或 harness")
        if not (hdx.ICONS_DIR / f"{s.get('id')}.svg").exists():
            err("assets/icons/slots/", f"缺少 {s.get('id')}.svg")
    site = hdx.load_site()
    for key in ("title", "description"):
        if not site.get(key):
            err("data/site.json", f"缺少 {key}")
    if not site.get("repo_url") or not site.get("site_url"):
        warn("data/site.json", "repo_url 或 site_url 還是空的：上傳 GitHub 之後記得填上，再重新 build")
    claude = hdx.ROOT / "CLAUDE.md"
    if not claude.exists() or "@AGENTS.md" not in claude.read_text(encoding="utf-8"):
        warn("CLAUDE.md", "應該用一行 @AGENTS.md 匯入規則，讓 Claude Code 和其他工具讀同一份")
    for name in ("AGENTS.md", "NOTES.md", "log.md"):
        if not (hdx.ROOT / name).exists():
            err(name, "檔案不見了")


# ---------------------------------------------------------------- 收錄稿

def check_note(note: dict, slot_ids: set[str], notes_by_slug: dict) -> None:
    where = f"notes/{note['path'].name}"
    meta, body = note["meta"], note["body"]
    for msg in note["errors"]:
        err(where, msg)
    if not meta:
        return

    for key in hdx.REQUIRED_FIELDS:
        if key not in meta or (meta[key] in ("", None, []) and key != "motto"):
            err(where, f"缺少必填欄位 {key}")
    for key in meta:
        if key not in KNOWN_FIELDS:
            warn(where, f"不認得的欄位 {key}（AGENTS.md 5.1 沒有這個欄位）")

    slug = meta.get("slug", "")
    if slug and slug != note["file_slug"]:
        err(where, f"slug「{slug}」要和檔名相同")
    if slug and not SLUG_RE.match(str(slug)):
        err(where, "slug 只能用英文小寫、數字和連字號")
    repo = str(meta.get("repo", ""))
    if repo and not REPO_RE.match(repo):
        err(where, "repo 要寫成 owner/repo")
    if meta.get("slot") and meta["slot"] not in slot_ids:
        err(where, f"slot「{meta['slot']}」不是 8 個欄位之一：{'、'.join(sorted(slot_ids))}")
    if meta.get("difficulty") not in (1, 2, 3):
        err(where, "difficulty 只能是 1、2 或 3")
    if meta.get("status") and meta["status"] not in hdx.STATUSES:
        err(where, "status 只能是 published 或 draft")
    tags = meta.get("tags")
    if isinstance(tags, list) and not 2 <= len(tags) <= 4:
        err(where, f"tags 要 2～4 個，現在有 {len(tags)} 個")

    added, updated = as_date(meta.get("added")), as_date(meta.get("updated"))
    if "added" in meta and not added:
        err(where, "added 要寫成 YYYY-MM-DD")
    if "updated" in meta and not updated:
        err(where, "updated 要寫成 YYYY-MM-DD")
    if added and updated and updated < added:
        err(where, "updated 不能早於 added")

    summary = str(meta.get("summary", ""))
    if length_units(summary) > 40:
        err(where, f"summary 太長（{length_units(summary)} 字，上限 40）")
    if STAR_RE.search(summary):
        err(where, "summary 不寫星數")
    motto = str(meta.get("motto", ""))
    if motto:
        if hdx.cjk_count(motto) and hdx.cjk_count(motto) > 20:
            err(where, f"motto 超過 20 個中文字（{hdx.cjk_count(motto)} 字）")
        if not hdx.cjk_count(motto) and hdx.word_count(motto) > 15:
            err(where, f"motto 超過 15 個英文字（{hdx.word_count(motto)} 字）")
    for key in ("homepage", "docs"):
        if meta.get(key) and not str(meta[key]).startswith("https://"):
            err(where, f"{key} 要是 https:// 開頭的網址")

    # ---- 正文段落
    parts = hdx.split_sections(body)
    headings = [h for h, _ in parts if h]
    if any(not h and c.strip() for h, c in parts):
        err(where, "第一個 ## 標題之前不能有文字")
    if headings != SECTION_NAMES:
        missing = [h for h in SECTION_NAMES if h not in headings]
        extra = [h for h in headings if h not in SECTION_NAMES]
        detail = []
        if missing:
            detail.append("缺少：" + "、".join(missing))
        if extra:
            detail.append("多了：" + "、".join(extra))
        if not missing and not extra:
            detail.append("順序不對")
        err(where, "正文的 8 個段落不符合 AGENTS.md 5.2（" + "；".join(detail) + "）")
    sec = {h: c for h, c in parts if h}

    plain = hdx.strip_code(body)
    for n, line in enumerate(plain.split("\n"), start=1):
        s = line.strip()
        if s.startswith("|"):
            err(where, "正文不能用表格")
            break
    if re.search(r"!\[", plain):
        err(where, "正文不能放圖片")
    if re.search(r"<[A-Za-z/][^>]*>", plain):
        err(where, "正文不能寫 HTML 標籤")
    if re.search(r"^#{4,}\s", plain, re.M):
        err(where, "正文最多只能用到 ### 三級標題")
    if STAR_RE.search(prose(body)):
        err(where, "正文裡有星數；數字要讓 build 從 raw/ 快照讀出來")

    if "怎麼試" in sec and not sec["怎麼試"].lstrip().startswith("需求"):
        err(where, "「怎麼試」第一行要先寫「需求：……」")
    if "適合誰" in sec and "不適合" not in sec["適合誰"]:
        err(where, "「適合誰」至少要有一點「不適合：……」")
    if "注意事項" in sec:
        items = re.findall(r"^\s*(?:[-*]|\d+\.)\s+", sec["注意事項"], re.M)
        if len(items) < 2:
            err(where, "「注意事項」至少要列 2 點")
    if "搭配裝備" in sec and not hdx.WIKI_RE.search(sec["搭配裝備"]):
        err(where, "「搭配裝備」至少要用 [[slug]] 連到一個已收錄的條目")
    for target in hdx.WIKI_RE.findall(hdx.strip_code(body)):
        if target == slug:
            warn(where, "搭配裝備連到了自己")
        elif target not in notes_by_slug:
            err(where, f"[[{target}]] 連到不存在的條目")
        elif notes_by_slug[target]["meta"].get("status") != "published":
            warn(where, f"[[{target}]] 還是草稿，網頁上會顯示成紅字")
    if "資料來源" in sec:
        links = hdx.LINK_RE.findall(sec["資料來源"])
        if not links:
            err(where, "「資料來源」沒有任何連結")
        elif repo and links[0][1].rstrip("/").lower() != f"https://github.com/{repo}".lower():
            err(where, f"「資料來源」第一個連結要是 https://github.com/{repo}")
        if not re.search(r"查閱日期：\d{4}-\d{2}-\d{2}", sec["資料來源"]):
            err(where, "「資料來源」最後要寫「查閱日期：YYYY-MM-DD」")

    # ---- 文字
    text = " ".join(str(v) for k, v in meta.items() if k != "motto") + " " + prose(body)
    found = sorted({ch for ch in text if ch in hdx.SIMPLIFIED})
    if found:
        err(where, "有簡體字：" + "".join(found))
    punct = PUNCT_RE.findall(text)
    if punct:
        warn(where, "中文旁邊用了半形標點：" + "、".join(sorted(set(punct))[:5]))

    # ---- 快照與收錄門檻
    if meta.get("status") == "published":
        check_snapshot(where, slug or note["file_slug"], repo, added)


def check_snapshot(where: str, slug: str, repo: str, added: date | None) -> None:
    files = hdx.snapshot_files(slug)
    if not files:
        err(where, f"沒有快照：請執行 python tools/snapshot.py {repo or 'owner/repo'}")
        return
    snap = hdx.read_json(files[-1])
    for key in ("repo", "url", "checked_at", "stars", "forks", "created_at", "root_files"):
        if key not in snap:
            err(f"raw/{slug}/{files[-1].name}", f"快照缺少 {key}；請用 snapshot.py 重新抓")
    if repo and str(snap.get("repo", "")).lower() != repo.lower():
        err(where, f"快照的 repo（{snap.get('repo')}）和收錄稿不同")
    if snap.get("archived"):
        err(where, "這個 repo 已經封存，依 AGENTS.md 第 6 節要下架（status 改成 draft）")
    if snap.get("root_files") is None:
        warn(where, "快照沒有根目錄檔案的資料，規則檔記號會顯示成未知")
    checked = as_date(snap.get("checked_at"))
    if checked and (date.today() - checked).days > 30:
        warn(where, f"快照是 {snap['checked_at']} 的，超過 30 天了：執行 python tools/snapshot.py --slug {slug}")
    created = as_date(snap.get("created_at"))
    stars = snap.get("stars", 0)
    fresh = bool(created and added and (added - created).days <= 90)
    if not ((fresh and stars >= 5000) or stars >= 20000):
        warn(where, "沒有達到 AGENTS.md 第 6 節的收錄門檻；確認使用者同意收錄，並寫進 NOTES.md")


# ---------------------------------------------------------------- 產生的網頁

def resolve_target(page_rel: str, url_path: str) -> str:
    joined = os.path.normpath(os.path.join(os.path.dirname(page_rel), url_path)).replace("\\", "/")
    if url_path.endswith("/") or url_path in ("", ".", "./", ".."):
        joined = (joined.rstrip("/") + "/index.html") if joined not in (".", "") else "index.html"
    return joined


def check_output(slot_ids: set[str]) -> int:
    try:
        out = builder.build()
    except builder.BuildError as e:
        err("tools/build.py", f"build 失敗：{e}")
        return 0
    for rel, text in out.items():
        path = hdx.ROOT / rel
        if not path.exists():
            err(rel, "還沒產生：請執行 python tools/build.py")
        elif path.read_text(encoding="utf-8") != text:
            err(rel, "不是最新的（收錄稿、快照或版型改過了）：請執行 python tools/build.py")
    for d in builder.stale_entry_dirs(out):
        err(f"entries/{d.name}/", "已經沒有對應的收錄稿：請執行 python tools/build.py")

    ids = {rel: set(re.findall(r'\sid="([^"]+)"', text)) for rel, text in out.items() if rel.endswith(".html")}
    checked = 0
    for rel, text in out.items():
        if not rel.endswith(".html"):
            continue
        for m in re.finditer(r'\b(?:href|src)="([^"]*)"', text):
            url = m.group(1)
            if re.match(r"^(https?:|mailto:|data:|//)", url):
                continue
            checked += 1
            path_part, _, frag = url.partition("#")
            target = rel if path_part == "" else resolve_target(rel, path_part.split("?")[0])
            if path_part and target not in out and not (hdx.ROOT / target).exists():
                err(rel, f"連結 {url} 指向不存在的檔案（{target}）")
                continue
            if not frag:
                continue
            if frag.startswith("slot-"):
                if frag[5:] not in slot_ids:
                    err(rel, f"連結 {url} 的欄位不存在")
            elif target in ids and frag not in ids[target]:
                err(rel, f"連結 {url} 的錨點 #{frag} 在 {target} 裡找不到")
        for m in re.finditer(r'wikilink-missing">\[\[([a-z0-9-]+)\]\]', text):
            err(rel, f"網頁裡有連不到的條目 [[{m.group(1)}]]")
    return checked


# ---------------------------------------------------------------- 主程式

def main() -> None:
    hdx.setup_console()
    slots = hdx.load_slots()
    slot_ids = {s["id"] for s in slots}
    check_config(slots)

    notes = hdx.load_notes()
    by_slug: dict = {}
    repos: dict = {}
    for n in notes:
        slug = n["meta"].get("slug") or n["file_slug"]
        if slug in by_slug:
            err(f"notes/{n['path'].name}", f"slug {slug} 重複")
        by_slug[slug] = n
        repo = str(n["meta"].get("repo", "")).lower()
        if repo and repo in repos:
            err(f"notes/{n['path'].name}", f"和 {repos[repo]} 收錄的是同一個 repo")
        repos[repo] = n["path"].name
    for n in notes:
        check_note(n, slot_ids, by_slug)
    links = check_output(slot_ids)

    published = sum(1 for n in notes if n["meta"].get("status") == "published")
    print("Harness 圖鑑健檢")
    print("─" * 40)
    for where, msg in errors:
        print(f"✗ {where}：{msg}")
    for where, msg in warnings:
        print(f"! {where}：{msg}")
    if errors or warnings:
        print("─" * 40)
    print(f"收錄稿 {len(notes)} 份（已發布 {published} 份），檢查了 {links} 個站內連結。")
    print(f"結果：{len(errors)} 個錯誤、{len(warnings)} 個警告。")
    if not errors:
        print("✓ 錯誤 0 個，可以交差。")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
