"""Harness 圖鑑：build.py、check.py、snapshot.py 共用的函式。

只用 Python 標準函式庫。規則說明見 AGENTS.md。
"""
from __future__ import annotations

import html
import json
import math
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "notes"
RAW_DIR = ROOT / "raw"
PAGES_DIR = ROOT / "pages"
TEMPLATES_DIR = ROOT / "templates"
ICONS_DIR = ROOT / "assets" / "icons" / "slots"

TAIPEI = timezone(timedelta(hours=8))

# 收錄稿正文的 8 個二級標題（順序固定）與它們在網頁上的錨點
SECTIONS = [
    ("它是什麼", "what"),
    ("為什麼放在這一格", "why-slot"),
    ("解決什麼問題", "problem"),
    ("怎麼試", "try"),
    ("適合誰", "who"),
    ("注意事項", "caveats"),
    ("搭配裝備", "combos"),
    ("資料來源", "sources"),
]

REQUIRED_FIELDS = ["slug", "name", "repo", "slot", "summary", "motto",
                   "difficulty", "tags", "added", "updated", "status"]
OPTIONAL_FIELDS = ["homepage", "docs"]
STATUSES = ["published", "draft"]
RULE_FILES = ["AGENTS.md", "CLAUDE.md", "SKILL.md"]

# 常見的簡體專用字。繁體中文頁面不該出現（motto 與程式碼區塊除外）。
SIMPLIFIED = set(
    "这们说为时会对发进还过动个么务实现应开关将让设计览层听吗网页题码图书写门问间风读获载"
    "环节简历运给经热点调试样产块编辑决错误权选择钟专业语营销装备级线帮库数类项无杂难领导"
    "闭观视频缓储键账认识记录档资讯体两车东马头买卖纪约终组细结统续维绍罗职联声处学宝宽寻"
    "尔尝岁广张弹归当彻径忆态怀总惊惯战扩扫扬护报担拥换损摄敌断旧显术机杀条来构标栏树检汇汉没"
)


def today() -> str:
    """台灣時間的今天，YYYY-MM-DD。"""
    return datetime.now(TAIPEI).strftime("%Y-%m-%d")


def setup_console() -> None:
    """讓 Windows 終端機也能印出中文與 ✓ ✗ 符號。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def load_site() -> dict:
    return read_json(ROOT / "data" / "site.json")


def load_slots() -> list[dict]:
    return read_json(ROOT / "data" / "slots.json")


def slug_from_repo(repo: str) -> str:
    """owner/repo → slug（英文小寫、句點與底線改成連字號）。"""
    name = repo.split("/")[-1].lower()
    name = re.sub(r"[._]+", "-", name)
    name = re.sub(r"[^a-z0-9-]", "", name)
    return re.sub(r"-{2,}", "-", name).strip("-")


# ---------------------------------------------------------------- front matter

def parse_front_matter(text: str) -> tuple[dict, str, list[str]]:
    """回傳 (欄位, 正文, 錯誤訊息)。格式見 AGENTS.md 5.1。"""
    errors: list[str] = []
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return {}, text, ["檔案開頭沒有 front matter（第一行要是 ---）"]
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text, ["front matter 沒有結尾的 ---"]
    head, body = text[4:end], text[end + 5:]
    meta: dict = {}
    for n, line in enumerate(head.split("\n"), start=2):
        if not line.strip():
            continue
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if not m:
            errors.append(f"front matter 第 {n} 行看不懂：{line!r}")
            continue
        key, raw = m.group(1), m.group(2).strip()
        if key in meta:
            errors.append(f"front matter 欄位重複：{key}")
        meta[key] = _parse_value(raw, key, errors)
    return meta, body, errors


def _parse_value(raw: str, key: str, errors: list[str]):
    if raw.startswith('"'):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            errors.append(f"{key} 的引號沒有配對好：{raw}")
            return raw.strip('"')
    if raw.startswith("["):
        if not raw.endswith("]"):
            errors.append(f"{key} 的清單要寫在同一行，並用 ] 結尾")
            return []
        inner = raw[1:-1].strip()
        return [x.strip().strip('"') for x in inner.split(",") if x.strip()] if inner else []
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    return raw


# ---------------------------------------------------------------- notes & snapshots

def load_notes(include_drafts: bool = True) -> list[dict]:
    notes = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        meta, body, errors = parse_front_matter(path.read_text(encoding="utf-8"))
        note = {"path": path, "file_slug": path.stem, "meta": meta, "body": body, "errors": errors}
        if include_drafts or meta.get("status") == "published":
            notes.append(note)
    return notes


def snapshot_files(slug: str) -> list[Path]:
    folder = RAW_DIR / slug
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.glob("*.json") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.stem))


def latest_snapshot(slug: str) -> dict | None:
    files = snapshot_files(slug)
    return read_json(files[-1]) if files else None


# ---------------------------------------------------------------- numbers

def fmt_count(n: int) -> str:
    """273872 → 27.4 萬；10257 → 1.0 萬；9634 → 9,634。"""
    if n >= 10000:
        return f"{n / 10000:.1f} 萬"
    return f"{n:,}"


GAUGE_MIN, GAUGE_MAX = 1_000, 300_000


def gauge_percent(stars: int) -> float:
    """星數在對數刻度（1 千～30 萬）上的位置，0～100。"""
    s = min(max(stars, GAUGE_MIN), GAUGE_MAX)
    return round(100 * math.log(s / GAUGE_MIN) / math.log(GAUGE_MAX / GAUGE_MIN), 1)


def cjk_count(s: str) -> int:
    return len(re.findall(r"[㐀-鿿豈-﫿]", s))


def word_count(s: str) -> int:
    return len(re.findall(r"[A-Za-z0-9'’\-]+", s))


# ---------------------------------------------------------------- markdown

def esc(s: str) -> str:
    return html.escape(s, quote=True)


WIKI_RE = re.compile(r"\[\[([a-z0-9-]+)\]\]")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
INCLUDE_RE = re.compile(r"^\[\[diagram:([a-z0-9-]+)\]\]$")


def inline(text: str, resolve_wiki) -> str:
    out = []
    for part in re.split(r"(`[^`]+`)", text):
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append(f"<code>{esc(part[1:-1])}</code>")
            continue
        s = esc(part)
        s = WIKI_RE.sub(lambda m: resolve_wiki(m.group(1)), s)

        def link(m):
            label, url = m.group(1), m.group(2)
            ext = url.startswith("http://") or url.startswith("https://")
            attrs = ' class="ext" rel="noopener"' if ext else ""
            return f'<a href="{url}"{attrs}>{label}</a>'

        s = LINK_RE.sub(link, s)
        s = BOLD_RE.sub(r"<strong>\1</strong>", s)
        out.append(s)
    return "".join(out)


def md_to_html(md: str, resolve_wiki, resolve_include=None) -> str:
    """把收錄稿用的 Markdown 子集轉成 HTML（語法範圍見 AGENTS.md 5.2）。"""
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    para: list[str] = []
    items: list[str] = []
    list_tag = None
    list_start = 1
    quote: list[str] = []

    def flush_para():
        if para:
            out.append(f"<p>{inline(' '.join(para), resolve_wiki)}</p>")
            para.clear()

    def flush_list():
        nonlocal list_tag
        if list_tag:
            start = f' start="{list_start}"' if list_tag == "ol" and list_start != 1 else ""
            lis = "".join(f"<li>{inline(i, resolve_wiki)}</li>" for i in items)
            out.append(f"<{list_tag}{start}>{lis}</{list_tag}>")
            items.clear()
            list_tag = None

    def flush_quote():
        if quote:
            out.append(f"<blockquote><p>{inline(' '.join(quote), resolve_wiki)}</p></blockquote>")
            quote.clear()

    def flush_all():
        flush_para(); flush_list(); flush_quote()

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush_all()
            lang = line[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            label = f' data-lang="{esc(lang)}"' if lang else ""
            out.append(f'<pre class="code"{label}><code>{esc(chr(10).join(code))}</code></pre>')
            continue
        stripped = line.strip()
        if not stripped:
            flush_all(); i += 1; continue
        inc = INCLUDE_RE.match(stripped)
        if inc and resolve_include:
            flush_all(); out.append(resolve_include(inc.group(1))); i += 1; continue
        m = re.match(r"^(#{2,3})\s+(.*)$", line)
        if m:
            flush_all()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2).strip(), resolve_wiki)}</h{level}>")
            i += 1; continue
        m_ul = re.match(r"^[-*]\s+(.*)$", line)
        m_ol = re.match(r"^(\d+)\.\s+(.*)$", line)
        if m_ul or m_ol:
            flush_para(); flush_quote()
            tag = "ul" if m_ul else "ol"
            if list_tag != tag:
                flush_list()
                list_tag = tag
                list_start = int(m_ol.group(1)) if m_ol else 1
            items.append(m_ul.group(1) if m_ul else m_ol.group(2))
            i += 1; continue
        if line.startswith("  ") and list_tag and items:
            items[-1] += " " + stripped
            i += 1; continue
        if line.startswith(">"):
            flush_para(); flush_list()
            quote.append(line[1:].strip())
            i += 1; continue
        flush_list(); flush_quote()
        para.append(stripped)
        i += 1
    flush_all()
    return "\n".join(out)


def split_sections(body: str) -> list[tuple[str, str]]:
    """依 '## ' 切開正文，回傳 [(標題, 內容)]。第一個標題前的文字標為 ''。"""
    sections: list[tuple[str, str]] = []
    current, buf = "", []
    in_code = False
    for line in body.replace("\r\n", "\n").split("\n"):
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and line.startswith("## "):
            if current or "".join(buf).strip():
                sections.append((current, "\n".join(buf).strip("\n")))
            current, buf = line[3:].strip(), []
        else:
            buf.append(line)
    sections.append((current, "\n".join(buf).strip("\n")))
    return sections


def strip_code(md: str) -> str:
    """去掉程式碼區塊與行內程式碼（給文字檢查用）。"""
    md = re.sub(r"```.*?```", "", md, flags=re.S)
    return re.sub(r"`[^`]*`", "", md)
