"""抓 GitHub 數據快照，存成 raw/<slug>/<今天>.json。

用法
  python tools/snapshot.py owner/repo              收錄新專案：先抓快照，slug 由 repo 名稱決定
  python tools/snapshot.py owner/repo --slug xxx   指定 slug（撞名時用）
  python tools/snapshot.py --slug deepseek-harness 更新一個已收錄的專案
  python tools/snapshot.py --all                   更新所有收錄稿的快照

快照是「事實的來源」：網頁上的星數、日期、授權都從這裡讀。
一天一份；同一天重抓會覆蓋當天那份，舊日期的快照不會被動到。
有 GITHUB_TOKEN 環境變數時會帶上（API 次數上限從每小時 60 次變 5,000 次）。
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hdx  # noqa: E402

API = "https://api.github.com"


def get_json(url: str):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "harness-dex-snapshot",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def repo_info(repo: str) -> tuple[dict, str]:
    """先用 repos API；讀不到再改用搜尋 API（回傳的欄位相同）。"""
    try:
        return get_json(f"{API}/repos/{repo}"), "GitHub repos API"
    except urllib.error.HTTPError as err:
        if err.code == 404:
            sys.exit(f"✗ 找不到 {repo}：確認 owner/repo 有沒有拼錯，或它是不是私人 repo。")
        first = err
    except urllib.error.URLError as err:
        sys.exit(f"✗ 連不上 GitHub：{err.reason}")
    try:
        data = get_json(f"{API}/search/repositories?q=repo:{repo}")
        for item in data.get("items", []):
            if item.get("full_name", "").lower() == repo.lower():
                return item, "GitHub search API"
    except urllib.error.HTTPError:
        pass
    sys.exit(f"✗ 讀不到 {repo} 的資料（HTTP {first.code}）。如果是次數上限，設定 GITHUB_TOKEN 後再試。")


def root_file_names(repo: str) -> tuple[list[str] | None, str | None]:
    """repo 根目錄的檔名。先用 contents API；不行就用 git 只抓目錄結構。"""
    try:
        listing = get_json(f"{API}/repos/{repo}/contents/")
        return [x["name"] for x in listing], "GitHub contents API"
    except (urllib.error.HTTPError, urllib.error.URLError):
        pass
    if shutil.which("git"):
        tmp = tempfile.mkdtemp(prefix="hdx-")
        try:
            subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--no-checkout",
                            f"https://github.com/{repo}.git", tmp],
                           check=True, capture_output=True, timeout=180)
            out = subprocess.run(["git", "-C", tmp, "ls-tree", "--name-only", "HEAD"],
                                 check=True, capture_output=True, text=True)
            return out.stdout.split(), "git ls-tree"
        except (subprocess.SubprocessError, OSError):
            pass
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return None, None


def taipei_date(stamp: str | None) -> str | None:
    if not stamp:
        return None
    dt = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    return dt.astimezone(hdx.TAIPEI).strftime("%Y-%m-%d")


def make_snapshot(info: dict, names: list[str] | None, sources: dict) -> dict:
    lowered = {n.lower() for n in names} if names is not None else None
    root_files = None if lowered is None else {f: f.lower() in lowered for f in hdx.RULE_FILES}
    license_ = info.get("license") or {}
    return {
        "repo": info["full_name"],
        "url": info["html_url"],
        "checked_at": hdx.today(),
        "stars": info["stargazers_count"],
        "forks": info["forks_count"],
        "language": info.get("language"),
        "license": license_.get("spdx_id"),
        "created_at": taipei_date(info.get("created_at")),
        "pushed_at": taipei_date(info.get("pushed_at")),
        "archived": bool(info.get("archived", False)),
        "homepage": info.get("homepage") or None,
        "topics": info.get("topics", []),
        "root_files": root_files,
        "sources": sources,
    }


def take(repo: str, slug: str) -> Path:
    info, how = repo_info(repo)
    names, how_files = root_file_names(info["full_name"])
    snap = make_snapshot(info, names, {"repo": how, "root_files": how_files})
    path = hdx.RAW_DIR / slug / f"{snap['checked_at']}.json"
    hdx.write_text(path, json.dumps(snap, ensure_ascii=False, indent=2) + "\n")
    marks = "未知" if snap["root_files"] is None else (
        "、".join(k for k, v in snap["root_files"].items() if v) or "無")
    print(f"✓ {slug:<20} ⭐ {hdx.fmt_count(snap['stars']):>8}  規則檔：{marks}  → {path.relative_to(hdx.ROOT).as_posix()}")
    if snap["archived"]:
        print("  ! 這個 repo 已封存（archived），依 AGENTS.md 第 6 節不收錄。")
    return path


def main() -> None:
    hdx.setup_console()
    ap = argparse.ArgumentParser(description="抓 GitHub 數據快照到 raw/")
    ap.add_argument("repo", nargs="?", help="owner/repo")
    ap.add_argument("--slug", help="指定 slug；不給 repo 時代表更新這個已收錄的專案")
    ap.add_argument("--all", action="store_true", help="更新所有收錄稿的快照")
    args = ap.parse_args()

    if args.all:
        notes = [n for n in hdx.load_notes() if n["meta"].get("repo")]
        for n in notes:
            take(n["meta"]["repo"], n["meta"].get("slug") or n["file_slug"])
        print(f"完成：{len(notes)} 個專案。接著執行 python tools/build.py")
        return
    if args.repo:
        repo = args.repo.strip().removeprefix("https://github.com/").strip("/")
        if repo.count("/") != 1:
            sys.exit("✗ 請用 owner/repo 的格式，例如 deepseek-ai/deepseek-harness")
        take(repo, args.slug or hdx.slug_from_repo(repo))
        return
    if args.slug:
        for n in hdx.load_notes():
            if (n["meta"].get("slug") or n["file_slug"]) == args.slug:
                take(n["meta"]["repo"], args.slug)
                return
        sys.exit(f"✗ notes/ 裡沒有 slug 為 {args.slug} 的收錄稿。新專案請改用：python tools/snapshot.py owner/repo")
    ap.print_help()


if __name__ == "__main__":
    main()
