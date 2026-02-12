---
name: find-emails
description: Crawl websites with crawl4ai hosted API to extract contact emails. Uses deep crawling with URL filters (contact, about, support) to find emails on relevant pages. Use when extracting emails from websites, finding contact information, or crawling for email addresses.
allowed-tools:
  - Read
  - Write
  - StrReplace
  - Shell
  - Glob
---

# Find Emails

CLI for crawling websites via the crawl4ai hosted API and extracting contact emails from pages likely to contain them (contact, about, support, team, etc.).

## Setup

1. Obtain a crawl4ai hosted API instance (deploy your own or get a URL from your provider)
2. Store the base URL:

```bash
mkdir -p ~/.config/crawl4ai
echo "https://your-instance.example.com" > ~/.config/crawl4ai/api_base
```

3. Use when running — either export the env var:

```bash
export CRAWL4AI_API_BASE=$(cat ~/.config/crawl4ai/api_base)
python scripts/find_emails.py https://example.com
```

Or pass the API base as a flag:

```bash
python scripts/find_emails.py --api-base https://your-instance.example.com https://example.com
```

## Quick Start

```bash
# Crawl a site (set CRAWL4AI_API_BASE or use --api-base)
python scripts/find_emails.py https://example.com

# Or pass API base as flag
python scripts/find_emails.py --api-base $CRAWL4AI_API_BASE https://example.com

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

| Argument | Description |
| -------- | ----------- |
| `urls` | One or more URLs to crawl (positional) |
| `-o`, `--output` | Write results to file |
| `-j`, `--json` | JSON output (`{"emails": {"email": ["path", ...]}}`) |
| `-q`, `--quiet` | Minimal output (no header, just email lines) |
| `--max-depth` | Max crawl depth (default: 2) |
| `--max-pages` | Max pages to crawl (default: 25) |
| `--api-base` | crawl4ai API base URL (pass as flag or use CRAWL4AI_API_BASE) |
| `--from-file` | Extract from local markdown file (skip crawl) |
| `-v`, `--verbose` | Verbose crawl output |

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
    "*contact*", "*support*", "*about*", "*team*",
    "*email*", "*reach*", "*staff*", "*inquiry*", "*enquir*",
    "*get-in-touch*", "*contact-us*", "*about-us*"
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
pip install crawl4ai httpx
```

**API configuration:**

- Required for crawl: Set `CRAWL4AI_API_BASE` or pass `--api-base <url>`. See Setup above.

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
