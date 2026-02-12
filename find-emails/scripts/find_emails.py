#!/usr/bin/env python3
"""Crawl websites via crawl4ai hosted API and extract contact emails from relevant pages."""
import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

DEFAULT_URL_PATTERNS = [
    "*contact*", "*support*", "*about*", "*team*",
    "*email*", "*reach*", "*staff*", "*inquiry*", "*enquir*",
    "*get-in-touch*", "*contact-us*", "*about-us*",
]


def load_url_patterns(script_dir: Path) -> list[str]:
    """Load URL filter patterns from url_patterns.json, or return defaults."""
    config_path = script_dir / "url_patterns.json"
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text())
            return data.get("url_patterns", DEFAULT_URL_PATTERNS)
        except (json.JSONDecodeError, OSError):
            pass
    return DEFAULT_URL_PATTERNS


def extract_emails_from_text(text: str, path: str) -> dict[str, list[str]]:
    """Extract emails from text and return {email_lower: [paths]}."""
    email_sources: dict[str, set[str]] = {}
    for email in EMAIL_REGEX.findall(text):
        key = email.lower()
        email_sources.setdefault(key, set()).add(path)
    return {e: sorted(paths) for e, paths in email_sources.items()}


def extract_from_file(file_path: Path) -> dict[str, list[str]]:
    """Extract emails from a local markdown/text file."""
    text = file_path.read_text()
    path = str(file_path.name)
    return extract_emails_from_text(text, path)


async def crawl_and_extract(
    urls: list[str],
    api_base: str,
    url_patterns: list[str],
    max_depth: int,
    max_pages: int,
    verbose: bool,
) -> dict[str, list[str]]:
    """Crawl URLs via crawl4ai hosted API and extract emails."""
    from crawl4ai.docker_client import Crawl4aiDockerClient
    from crawl4ai import BrowserConfig, CrawlerRunConfig, CacheMode
    from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
    from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter

    async with Crawl4aiDockerClient(
        base_url=api_base,
        timeout=300.0,
        verbose=verbose,
    ) as client:
        results = await client.crawl(
            urls,
            browser_config=BrowserConfig(headless=True),
            crawler_config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                page_timeout=15_000,
                deep_crawl_strategy=BFSDeepCrawlStrategy(
                    max_depth=max_depth,
                    include_external=False,
                    max_pages=max_pages,
                    filter_chain=FilterChain([
                        URLPatternFilter(patterns=url_patterns),
                    ]),
                ),
            ),
            hooks_timeout=300,
        )

    if not results:
        return {}

    pages = results if isinstance(results, list) else [results]
    combined: dict[str, set[str]] = {}

    for result in pages:
        if result.success and result.markdown:
            text = (
                result.markdown.raw_markdown
                if hasattr(result.markdown, "raw_markdown")
                else str(result.markdown)
            )
            path = urlparse(result.url).path or "/"
            for email in EMAIL_REGEX.findall(text):
                key = email.lower()
                combined.setdefault(key, set()).add(path)

    return {e: sorted(paths) for e, paths in combined.items()}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Crawl websites and extract contact emails via crawl4ai hosted API."
    )
    parser.add_argument(
        "urls",
        nargs="*",
        help="URL(s) to crawl",
    )
    parser.add_argument(
        "-o", "--output",
        help="Write results to file",
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="JSON output",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Minimal output",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=2,
        help="Max crawl depth (default: 2)",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=25,
        help="Max pages to crawl (default: 25)",
    )
    parser.add_argument(
        "--api-base",
        default=os.environ.get("CRAWL4AI_API_BASE"),
        metavar="URL",
        help="crawl4ai API base URL (pass as flag or set CRAWL4AI_API_BASE env var)",
    )
    parser.add_argument(
        "--from-file",
        metavar="FILE",
        help="Extract emails from local markdown file (skip crawl)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose crawl output",
    )
    args = parser.parse_args()

    script_dir = Path(__file__).parent

    if args.from_file:
        file_path = Path(args.from_file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        email_sources = extract_from_file(file_path)
    elif args.urls:
        if not args.api_base:
            print(
                "Error: Set CRAWL4AI_API_BASE or pass --api-base <url>. "
                "Get your crawl4ai hosted instance URL from your deployment.",
                file=sys.stderr,
            )
            sys.exit(1)
        url_patterns = load_url_patterns(script_dir)
        try:
            email_sources = asyncio.run(crawl_and_extract(
                urls=args.urls,
                api_base=args.api_base,
                url_patterns=url_patterns,
                max_depth=args.max_depth,
                max_pages=args.max_pages,
                verbose=args.verbose,
            ))
        except Exception as e:
            print(f"Crawl failed: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.error("Either provide URLs or use --from-file")

    output_lines: list[str] = []
    if args.json:
        output_lines.append(json.dumps({"emails": email_sources}, indent=2))
    else:
        if not args.quiet:
            output_lines.append(f"{len(email_sources)} emails found:")
            output_lines.append("Format: email — path where the email was found")
        for email in sorted(email_sources):
            paths = ", ".join(sorted(email_sources[email]))
            output_lines.append(f"{email} - {paths}")

    out_text = "\n".join(output_lines)
    if args.output:
        Path(args.output).write_text(out_text)
        if not args.quiet:
            print(f"→ {args.output}", file=sys.stderr)
    else:
        print(out_text)


if __name__ == "__main__":
    main()
