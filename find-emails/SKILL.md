---
name: find-emails
description: Crawl websites locally with crawl4ai to extract contact emails. Uses deep crawling with URL filters (contact, about, support) to find emails on relevant pages. Use when extracting emails from websites, finding contact information, or crawling for email addresses.
allowed-tools:
  - Read
  - Write
  - StrReplace
  - Shell
  - Glob
---

# Find Emails

CLI for crawling websites locally via crawl4ai and extracting contact emails from pages likely to contain them (contact, about, support, team, etc.).

## Setup

1. Install dependencies: `pip install crawl4ai`
2. Run the script:

```bash
python scripts/find_emails.py https://example.com
```

## Quick Start

```bash
# Crawl a site
python scripts/find_emails.py https://example.com

# Multiple URLs
python scripts/find_emails.py https://example.com https://other.com

# JSON output
python scripts/find_emails.py https://example.com -j

# Save to file
python scripts/find_emails.py https://example.com -o emails.txt
```

---

## Script

### find_emails.py — Crawl and Extract Emails

```bash
python scripts/find_emails.py <url> [url ...]
python scripts/find_emails.py https://example.com
python scripts/find_emails.py https://example.com -j -o results.json
python scripts/find_emails.py --from-file page.md
```

**Arguments:**

| Argument          | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `urls`            | One or more URLs to crawl (positional)               |
| `-o`, `--output`  | Write results to file                                |
| `-j`, `--json`    | JSON output (`{"emails": {"email": ["path", ...]}}`) |
| `-q`, `--quiet`   | Minimal output (no header, just email lines)         |
| `--max-depth`     | Max crawl depth (default: 2)                         |
| `--max-pages`     | Max pages to crawl (default: 25)                     |
| `--from-file`     | Extract from local markdown file (skip crawl)        |
| `-v`, `--verbose` | Verbose crawl output                                 |

**Output format (human-readable):**

```
N emails found:
Format: email — path where the email was found
contact@example.com - /contact, /about
support@example.com - /support
```

**Output format (JSON):**

```json
{
  "emails": {
    "contact@example.com": ["/contact", "/about"],
    "support@example.com": ["/support"]
  }
}
```

---

## Configuration

Edit `scripts/url_patterns.json` to customize which URLs the crawler follows. Only links matching these glob-style patterns are included:

```json
{
  "url_patterns": [
    "*contact*",
    "*support*",
    "*about*",
    "*team*",
    "*email*",
    "*reach*",
    "*staff*",
    "*inquiry*",
    "*enquir*",
    "*get-in-touch*",
    "*contact-us*",
    "*about-us*"
  ]
}
```

If the file is missing or invalid, default patterns are used.

---

## Workflow

1. **Crawl** a site:

   ```bash
   python scripts/find_emails.py https://example.com -o emails.json
   ```

2. **Extract from local file** (e.g., cached markdown):

   ```bash
   python scripts/find_emails.py --from-file crawled.md -j
   ```

3. **Customize** URL filters by editing `scripts/url_patterns.json`.

---

## Dependencies

```bash
pip install crawl4ai
playwright install
```

Requires a browser (Playwright) for local crawling.

---

## Batch Processing

```bash
# Crawl multiple sites
python scripts/find_emails.py https://site1.com https://site2.com -j -o combined.json

# Extract from multiple local files
for f in crawled/*.md; do
  echo "=== $f ==="
  python scripts/find_emails.py --from-file "$f" -q
done
```
