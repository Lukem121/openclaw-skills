# Crawl4AI Project

Python project using [Crawl4AI](https://docs.crawl4ai.com/) for LLM-friendly web crawling and scraping.

## Setup

### 1. Create the Conda environment

```bash
conda env create -f environment.yml
```

### 2. Activate the environment

```bash
conda activate crawl4ai
```

### 3. Run the post-install setup

Crawl4AI needs browser dependencies (Playwright). After activating:

```bash
crawl4ai-setup
```

### 4. (Optional) Run diagnostics

If you hit any issues:

```bash
crawl4ai-doctor
```

## Quick test

Run the example script to verify everything works:

```bash
python example_crawl.py
```

## Advanced features

To add optional Crawl4AI extras (Torch, Transformers, etc.):

- Torch: `pip install crawl4ai[torch]`
- Transformers: `pip install crawl4ai[transformer]`
- All: `pip install crawl4ai[all]` then `crawl4ai-download-models`
