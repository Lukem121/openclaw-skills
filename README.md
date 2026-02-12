# OpenClaw Skills

A collection of AI agent skills for Cursor and compatible agents. Each skill includes a `SKILL.md` that teaches the agent how to use it, plus scripts and config as needed.

## Skills

| Skill                       | Description                                                                                                 |
| --------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [find-emails](find-emails/) | Crawl websites via crawl4ai hosted API to extract contact emails from pages (contact, about, support, etc.) |

## Usage

Add the skill folder to your Cursor skills path (e.g. `~/.cursor/skills/` or `.cursor/skills/` in your project). Each skill is self-contained: read its `SKILL.md` for setup and usage.

## Requirements

Each skill documents its own dependencies. For example, find-emails requires `crawl4ai` and `httpx`; see [find-emails/SKILL.md](find-emails/SKILL.md) for details.

---

## Sponsors

This project is sponsored by [Social Crow](https://www.socialcrow.co/).

[![Social Crow](https://github.com/user-attachments/assets/5737a0b9-6fd1-481b-a29d-4727b1afb9b1)](https://www.socialcrow.co/)
