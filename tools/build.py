"""產生網頁：notes/ ＋ raw/ ＋ pages/ ＋ templates/ → index.html、entries/、about/、data/entries.json、llms.txt

用法：python tools/build.py

規則見 AGENTS.md。這支程式產生的檔案不要手改：內容改 notes/ 或 pages/，版型改 templates/，再重新執行。
輸出只跟輸入有關（不寫入當下時間），所以 check.py 可以重新產生一次來比對網頁是不是最新的。
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hdx  # noqa: E402
from hdx import esc  # noqa: E402

DIFFICULTY_TEXT = {
    1: "打開網頁或一行指令就能試",
    2: "要先裝軟體，或準備金鑰、帳號",
    3: "要架服務、設定多組金鑰",
}


class BuildError(Exception):
    pass


# ---------------------------------------------------------------- 版型

def tpl(name: str) -> str:
    return (hdx.TEMPLATES_DIR / name).read_text(encoding="utf-8")


def fill(template: str, values: dict, name: str) -> str:
    def rep(m):
        key = m.group(1)
        if key not in values:
            raise BuildError(f"templates/{name} 用到 {{{{{key}}}}}，但 build.py 沒有提供這個值")
        return str(values[key])
    return re.sub(r"\{\{([a-z_]+)\}\}", rep, template)


def sprite(slots: list[dict]) -> str:
    """把 8 個剪影 SVG 合成一份 <symbol> 圖庫，頁面裡用 <use href="#icon-<id>"> 引用。"""
    defs, symbols = [], []
    for s in slots:
        path = hdx.ICONS_DIR / f"{s['id']}.svg"
        if not path.exists():
            raise BuildError(f"缺少欄位圖示 {path.relative_to(hdx.ROOT).as_posix()}")
        m = re.search(r"<svg[^>]*>(.*)</svg>", path.read_text(encoding="utf-8"), re.S)
        inner = m.group(1) if m else ""
        d = re.search(r"<defs>(.*?)</defs>", inner, re.S)
        if d:
            defs.append(d.group(1).strip())
            inner = inner.replace(d.group(0), "")
        symbols.append(f'<symbol id="icon-{s["id"]}" viewBox="0 0 64 64">{inner.strip()}</symbol>')
    body = "<defs>" + "".join(defs) + "</defs>" + "".join(symbols)
    body = re.sub(r">\s+<", "><", body)
    return f'<svg class="sprite" aria-hidden="true" focusable="false">{body}</svg>'


# ---------------------------------------------------------------- 資料

def collect() -> tuple[list[dict], list[dict]]:
    slots = hdx.load_slots()
    slot_map = {s["id"]: s for s in slots}
    entries = []
    for note in hdx.load_notes(include_drafts=True):
        meta = note["meta"]
        if note["errors"]:
            raise BuildError(f"notes/{note['path'].name}：" + "；".join(note["errors"]))
        if meta.get("status") != "published":
            continue
        slug = meta.get("slug") or note["file_slug"]
        snap = hdx.latest_snapshot(slug)
        if snap is None:
            raise BuildError(f"{slug} 還沒有快照：先執行 python tools/snapshot.py {meta.get('repo', 'owner/repo')}")
        slot = slot_map.get(meta.get("slot"))
        if slot is None:
            raise BuildError(f"notes/{note['path'].name} 的 slot「{meta.get('slot')}」不是 data/slots.json 裡的欄位")
        entries.append({
            "slug": slug,
            "name": str(meta.get("name", slug)),
            "repo": meta.get("repo", ""),
            "slot": slot["id"],
            "slot_name": slot["name"],
            "summary": str(meta.get("summary", "")),
            "motto": str(meta.get("motto", "")),
            "difficulty": meta.get("difficulty") if meta.get("difficulty") in DIFFICULTY_TEXT else 2,
            "tags": meta.get("tags") or [],
            "homepage": meta.get("homepage", ""),
            "docs": meta.get("docs", ""),
            "body": note["body"],
            "snap": snap,
        })
    entries.sort(key=lambda e: (-e["snap"]["stars"], e["name"].lower()))
    return slots, entries


# ---------------------------------------------------------------- 小元件

def pips(level: int) -> str:
    cells = "".join(f'<span class="pip{" on" if i < level else ""}"></span>' for i in range(3))
    return f'<span class="pips" role="img" aria-label="上手難度 {level}，滿分 3">{cells}</span>'


def marks(root_files: dict | None) -> str:
    if root_files is None:
        return '<span class="marks"><span class="mark">快照沒有這項資料</span></span>'
    items = []
    for f in hdx.RULE_FILES:
        on = bool(root_files.get(f))
        hidden = "：有" if on else "：沒有"
        items.append(f'<span class="mark{" on" if on else ""}">{f}<span class="visually-hidden">{hidden}</span></span>')
    return f'<span class="marks">{"".join(items)}</span>'


def wiki_resolver(by_slug: dict, prefix: str):
    def resolve(slug: str) -> str:
        e = by_slug.get(slug)
        if not e:
            return f'<span class="wikilink-missing">[[{slug}]]</span>'
        icon = f'<svg class="mini" viewBox="0 0 64 64" aria-hidden="true"><use href="#icon-{e["slot"]}"></use></svg>'
        return f'<a class="wikilink" href="{prefix}{slug}/">{icon}{esc(e["name"])}</a>'
    return resolve


def ext_link(url: str, label: str) -> str:
    return f'<a class="ext" rel="noopener" href="{esc(url)}">{esc(label)}</a>'


# ---------------------------------------------------------------- 頁面

def page(content: str, ctx: dict, *, title: str, description: str, root: str, body_class: str) -> str:
    values = dict(ctx)
    values.update(page_title=esc(title), description=esc(description), root=root,
                  body_class=body_class, content=content)
    return fill(tpl("base.html"), values, "base.html")


def render_entry(e: dict, prev: dict | None, nxt: dict | None, by_slug: dict, ctx: dict) -> str:
    resolve = wiki_resolver(by_slug, "../")
    ids = dict(hdx.SECTIONS)
    sections, toc = [], []
    for heading, content in hdx.split_sections(e["body"]):
        if not heading:
            continue
        sid = ids.get(heading, f"sec-{len(sections) + 1}")
        shown = f"為什麼放在「{e['slot_name']}」這一格" if sid == "why-slot" else heading
        body = hdx.md_to_html(content, resolve)
        sections.append(f'<section class="sec sec--{sid}" id="{sid}">\n<h2>{esc(shown)}</h2>\n{body}\n</section>')
        toc.append(f'<li><a href="#{sid}">{esc(shown)}</a></li>')

    snap = e["snap"]
    links = [ext_link(snap["url"], "GitHub repo")]
    if e["homepage"]:
        links.append(ext_link(e["homepage"], "官方網站"))
    if e["docs"]:
        links.append(ext_link(e["docs"], "官方文件"))

    motto = ""
    if e["motto"]:
        motto = f'<p class="motto"><span class="motto-label">官方標語</span>「{esc(e["motto"])}」</p>'

    pager = []
    if prev:
        pager.append(f'<a class="prev" href="../{prev["slug"]}/"><small>上一件</small><strong>{esc(prev["name"])}</strong></a>')
    if nxt:
        pager.append(f'<a class="next" href="../{nxt["slug"]}/"><small>下一件</small><strong>{esc(nxt["name"])}</strong></a>')

    content = fill(tpl("entry.html"), {
        "root": "../../",
        "slot": e["slot"],
        "slot_name": esc(e["slot_name"]),
        "name": esc(e["name"]),
        "motto_html": motto,
        "summary": esc(e["summary"]),
        "links": "".join(links),
        "stars": hdx.fmt_count(snap["stars"]),
        "gauge": hdx.gauge_percent(snap["stars"]),
        "forks": hdx.fmt_count(snap["forks"]),
        "language": esc(snap.get("language") or "—"),
        "license": esc(snap.get("license") or "未標示"),
        "created": snap.get("created_at") or "—",
        "pushed": snap.get("pushed_at") or "—",
        "difficulty_html": pips(e["difficulty"]) + esc(DIFFICULTY_TEXT[e["difficulty"]]),
        "rule_marks": marks(snap.get("root_files")),
        "checked_at": snap["checked_at"],
        "tags": esc("、".join(e["tags"])),
        "toc": "".join(toc),
        "sections": "\n".join(sections),
        "pager": "".join(pager),
    }, "entry.html")
    return page(content, ctx, title=f"{e['name']}｜{ctx['site_title']}",
                description=e["summary"], root="../../", body_class="page-entry")


def render_home(slots: list[dict], entries: list[dict], ctx: dict) -> str:
    by_slot = {s["id"]: [e for e in entries if e["slot"] == s["id"]] for s in slots}
    slot_tpl = tpl("partials/slot.html")

    def slot_html(s: dict) -> str:
        items = by_slot[s["id"]]
        hung = "".join(f'<li><a href="entries/{e["slug"]}/">{esc(e["name"])}</a></li>' for e in items)
        return fill(slot_tpl, {"id": s["id"], "name": esc(s["name"]), "count": len(items),
                               "hung": hung or '<li><span class="empty">尚未收錄</span></li>'},
                    "partials/slot.html")

    filters = [f'<button type="button" class="filter" data-slot="all" data-name="全部" aria-pressed="true">'
               f'全部<span class="n">{len(entries)}</span></button>']
    for s in slots:
        filters.append(f'<button type="button" class="filter" data-slot="{s["id"]}" data-name="{esc(s["name"])}" '
                       f'aria-pressed="false">{esc(s["name"])}<span class="n">{len(by_slot[s["id"]])}</span></button>')

    row_tpl = tpl("partials/row.html")
    rows = []
    for e in entries:
        rows.append(fill(row_tpl, {
            "slot": e["slot"], "slug": e["slug"], "name": esc(e["name"]),
            "summary": esc(e["summary"]), "slot_name": esc(e["slot_name"]),
            "stars": hdx.fmt_count(e["snap"]["stars"]), "gauge": hdx.gauge_percent(e["snap"]["stars"]),
            "difficulty_html": pips(e["difficulty"]), "rule_marks": marks(e["snap"].get("root_files")),
        }, "partials/row.html"))

    known = [e for e in entries if e["snap"].get("root_files") is not None]
    have = {f: [e for e in known if e["snap"]["root_files"].get(f)] for f in hdx.RULE_FILES}
    strips = []
    for f in hdx.RULE_FILES:
        pegs = "".join(f'<span class="peg{" on" if e["snap"]["root_files"].get(f) else ""}" title="{esc(e["name"])}"></span>'
                       for e in known)
        names = "、".join(e["name"] for e in have[f]) or "沒有"
        label = f"{f}：{len(known)} 個專案中有 {len(have[f])} 個（{names}）"
        strips.append(f'<div class="peg-strip"><span class="file">{f}</span>'
                      f'<span class="peg-row" role="img" aria-label="{esc(label)}">{pegs}</span>'
                      f'<span class="count">{len(have[f])}／{len(known)}</span></div>')
    sentence = (f"收錄的 {len(known)} 個專案裡，有 {len(have['AGENTS.md'])} 個在 repo 根目錄放了 AGENTS.md，"
                f"{len(have['CLAUDE.md'])} 個放了 CLAUDE.md")
    sentence += f"；另有 {len(have['SKILL.md'])} 個專案本身就是一份 SKILL.md 技能。" if have["SKILL.md"] else "。"
    sentence += "每個圓點代表一個專案，順序和裝備清單相同。"

    content = fill(tpl("home.html"), {
        "slot_model": "".join(slot_html(s) for s in slots if s["zone"] == "model"),
        "slots_harness": "".join(slot_html(s) for s in slots if s["zone"] == "harness"),
        "slot_count": len(slots),
        "snapshot_date": ctx["snapshot_date"],
        "filters": "".join(filters),
        "entry_count": len(entries),
        "rows": "".join(rows),
        "rule_sentence": esc(sentence),
        "peg_strips": "".join(strips),
    }, "home.html")
    return page(content, ctx, title=f"{ctx['site_title']}｜AI Agent 的裝備庫",
                description=ctx["site_description_raw"], root="./", body_class="page-home")


def render_page(path: Path, by_slug: dict, ctx: dict) -> str:
    meta, body, errors = hdx.parse_front_matter(path.read_text(encoding="utf-8"))
    if errors or "title" not in meta or "summary" not in meta:
        raise BuildError(f"pages/{path.name} 的 front matter 要有 title 和 summary" + (f"：{'；'.join(errors)}" if errors else ""))

    def include(name: str) -> str:
        part = hdx.TEMPLATES_DIR / "partials" / f"diagram-{name}.html"
        if not part.exists():
            raise BuildError(f"pages/{path.name} 用到 [[diagram:{name}]]，但沒有 templates/partials/diagram-{name}.html")
        return part.read_text(encoding="utf-8").strip()

    html_body = hdx.md_to_html(body, wiki_resolver(by_slug, "../entries/"), include)
    content = fill(tpl("page.html"), {"title": esc(meta["title"]), "summary": esc(meta["summary"]),
                                      "body": html_body}, "page.html")
    return page(content, ctx, title=f"{meta['title']}｜{ctx['site_title']}", description=meta["summary"],
                root="../", body_class=f"page-{path.stem}")


def entries_json(entries: list[dict]) -> str:
    data = [{
        "slug": e["slug"], "name": e["name"], "repo": e["repo"], "url": f"entries/{e['slug']}/",
        "slot": e["slot"], "slot_name": e["slot_name"], "summary": e["summary"],
        "difficulty": e["difficulty"], "tags": e["tags"], "stars": e["snap"]["stars"],
        "checked_at": e["snap"]["checked_at"], "root_files": e["snap"].get("root_files"),
    } for e in entries]
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def llms_txt(site: dict, slots: list[dict], entries: list[dict]) -> str:
    base = site["site_url"].rstrip("/") + "/" if site.get("site_url") else ""
    sections = "、".join(name for name, _ in hdx.SECTIONS)
    lines = [f"# {site['title']}", "", f"> {site['description']}", "",
             f"每個專案一頁，固定 8 段：{sections}。網站規則寫在 repo 的 AGENTS.md。", ""]
    for s in slots:
        items = [e for e in entries if e["slot"] == s["id"]]
        if not items:
            continue
        lines += [f"## {s['name']}", ""]
        lines += [f"- [{e['name']}]({base}entries/{e['slug']}/): {e['summary']}" for e in items]
        lines.append("")
    lines += ["## 關於本站", "", f"- [這個網站怎麼長出來的]({base}about/): 規則、資料流程與健檢方式"]
    if site.get("repo_url"):
        lines.append(f"- [原始碼與 AGENTS.md]({site['repo_url']})")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- 主程式

def build() -> dict[str, str]:
    """回傳 {相對路徑: 內容}。不寫檔，方便 check.py 比對。"""
    site = hdx.load_site()
    slots, entries = collect()
    by_slug = {e["slug"]: e for e in entries}
    snapshot_date = max((e["snap"]["checked_at"] for e in entries), default="—")
    repo_url = site.get("repo_url") or ""
    ctx = {
        "site_title": esc(site["title"]),
        "site_description": esc(site["description"]),
        "site_description_raw": site["description"],
        "credit": esc(site.get("credit", "")),
        "snapshot_date": snapshot_date,
        "sprite": sprite(slots),
        "github_link": ext_link(repo_url, "GitHub") if repo_url else "",
        "github_footer": f"<p>{ext_link(repo_url, '原始碼與 AGENTS.md')}</p>" if repo_url else "",
    }

    out: dict[str, str] = {"index.html": render_home(slots, entries, ctx)}
    for i, e in enumerate(entries):
        prev = entries[i - 1] if i > 0 else None
        nxt = entries[i + 1] if i + 1 < len(entries) else None
        out[f"entries/{e['slug']}/index.html"] = render_entry(e, prev, nxt, by_slug, ctx)
    for path in sorted(hdx.PAGES_DIR.glob("*.md")):
        out[f"{path.stem}/index.html"] = render_page(path, by_slug, ctx)
    out["data/entries.json"] = entries_json(entries)
    out["llms.txt"] = llms_txt(site, slots, entries)
    return out


def stale_entry_dirs(out: dict[str, str]) -> list[Path]:
    keep = {rel.split("/")[1] for rel in out if rel.startswith("entries/")}
    folder = hdx.ROOT / "entries"
    return [d for d in sorted(folder.iterdir()) if d.is_dir() and d.name not in keep] if folder.is_dir() else []


def main() -> None:
    hdx.setup_console()
    try:
        out = build()
    except BuildError as err:
        print(f"✗ {err}")
        sys.exit(1)
    changed = 0
    for rel, text in out.items():
        path = hdx.ROOT / rel
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            hdx.write_text(path, text)
            changed += 1
    for d in stale_entry_dirs(out):
        shutil.rmtree(d)
        print(f"- 移除已下架的頁面 entries/{d.name}/")
    print(f"✓ 產生 {len(out)} 個檔案，其中 {changed} 個有變動。接著執行 python tools/check.py")


if __name__ == "__main__":
    main()
