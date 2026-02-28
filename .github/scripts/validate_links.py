#!/usr/bin/env python3

from html.parser import HTMLParser
from pathlib import Path
from typing import override
from urllib.parse import urlparse, unquote


REPO_ROOT = Path(__file__).resolve().parents[2]
HTML_FILES = [
    REPO_ROOT / "index.html",
    REPO_ROOT / "home" / "index.html",
]


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, int]] = []

    @override
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        href = attrs_map.get("href")
        src = attrs_map.get("src")
        if tag == "a" and href:
            self.links.append((href, self.getpos()[0]))
        if tag in {"img", "script", "source"} and src:
            self.links.append((src, self.getpos()[0]))
        if tag == "link" and href:
            self.links.append((href, self.getpos()[0]))


def is_external(target: str) -> bool:
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https", "mailto", "tel", "javascript"}:
        return True
    if target.startswith("#"):
        return True
    return False


def resolve_path(source_file: Path, target: str) -> Path:
    parsed = urlparse(target)
    clean = unquote(parsed.path)

    if clean.startswith("/"):
        candidate = REPO_ROOT / clean.lstrip("/")
    else:
        candidate = (source_file.parent / clean).resolve()

    return candidate


def exists_on_disk(path: Path) -> bool:
    if path.exists():
        return True
    if path.suffix == "":
        return (path / "index.html").exists()
    return False


def validate_file(html_file: Path) -> list[str]:
    parser = LinkCollector()
    parser.feed(html_file.read_text(encoding="utf-8"))
    errors: list[str] = []

    for raw_target, line in parser.links:
        target = raw_target.strip()
        if not target or is_external(target):
            continue

        resolved = resolve_path(html_file, target)
        if not exists_on_disk(resolved):
            rel_source = html_file.relative_to(REPO_ROOT)
            rel_target = (
                resolved.relative_to(REPO_ROOT)
                if str(resolved).startswith(str(REPO_ROOT))
                else resolved
            )
            errors.append(
                f"{rel_source}:{line} broken link '{target}' -> '{rel_target}'"
            )

    return errors


def main() -> int:
    missing_inputs = [
        str(path.relative_to(REPO_ROOT)) for path in HTML_FILES if not path.exists()
    ]
    if missing_inputs:
        print("Missing required HTML files:")
        for missing in missing_inputs:
            print(f"- {missing}")
        return 1

    all_errors: list[str] = []
    for html_file in HTML_FILES:
        all_errors.extend(validate_file(html_file))

    if all_errors:
        print("Link validation failed:")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print("Link validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
