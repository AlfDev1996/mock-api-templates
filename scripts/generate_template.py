#!/usr/bin/env python3
"""
MockHub — Mock API Template Generator
Generates a new JSON template using Claude and updates the README.

Usage:
    python generate_template.py               # auto-picks next unpublished
    python generate_template.py --slug <slug> # specific template
    python generate_template.py --dry-run     # generate only, do not commit

Required env:
    ANTHROPIC_API_KEY
"""

import os
import re
import json
import argparse
import logging
from datetime import datetime
from pathlib import Path

import anthropic
from json_repair import repair_json

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).parent.parent
TOPICS_FILE = Path(__file__).parent / "template_topics.json"

SYSTEM_PROMPT = """You are a senior API designer creating mock API templates for developers.

You generate realistic, production-quality JSON mock API templates.
Each template is used by developers to quickly spin up fake REST endpoints for testing,
frontend development, CI/CD pipelines, and demos — using MockHub (https://mockhub.ovh).

RULES:
- Every endpoint must have: name, method, path, status_code, headers, delay_ms, response
- Use ONLY these dynamic variables (MockHub-supported):
  {{uuid}}, {{name}}, {{firstname}}, {{lastname}}, {{email}}, {{phone}},
  {{isodate}}, {{timestamp}}, {{integer}}, {{float}}, {{boolean}},
  {{word}}, {{sentence}}, {{url}}, {{ipv4}}, {{color}},
  {{city}}, {{country}}, {{zipcode}}, {{company}}, {{jobtitle}},
  {{creditcard}}, {{iban}}
- Include at least 1 error scenario (4xx or 5xx) per logical operation
- Response bodies must be realistic and complete (not minimal stubs)
- Use standard HTTP conventions (201 for create, 204 for delete, etc.)
- delay_ms should be 0 for GET reads, 80-350 for writes/mutations
- path parameters use :param_name syntax (e.g., /users/:id)
- Always include "import_to_mockhub": "https://mockhub.ovh/api-generator/generate_api.html"
"""

TEMPLATE_PROMPT = """Generate a complete mock API template JSON for: {name}

Description: {description}
Category folder: {category}
Slug: {slug}

Output ONLY valid JSON matching this exact structure:
{{
  "name": "...",
  "description": "...",
  "import_to_mockhub": "https://mockhub.ovh/api-generator/generate_api.html",
  "endpoints": [
    {{
      "name": "...",
      "method": "GET|POST|PUT|PATCH|DELETE",
      "path": "/...",
      "status_code": 200,
      "headers": {{ "Content-Type": "application/json" }},
      "delay_ms": 0,
      "response": {{ ... }}
    }}
  ]
}}

Requirements:
- At least 5 endpoints covering the main CRUD operations
- At least 2 error scenarios (different status codes)
- Realistic nested response bodies using dynamic variables
- No trailing commas, valid JSON only
"""


def load_topics():
    with open(TOPICS_FILE) as f:
        return json.load(f)


def save_topics(topics):
    with open(TOPICS_FILE, "w") as f:
        json.dump(topics, f, indent=2)


def pick_next(topics, slug=None):
    if slug:
        for t in topics:
            if t["slug"] == slug:
                return t
        raise ValueError(f"Slug '{slug}' not found")
    for t in topics:
        if not t.get("published"):
            return t
    raise ValueError("All templates published. Add more to template_topics.json")


def generate_template(topic):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY not set")

    log.info(f"Generating template: {topic['name']}")

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=6000,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": TEMPLATE_PROMPT.format(
                name=topic["name"],
                description=topic["description"],
                category=topic["category"],
                slug=topic["slug"],
            )
        }],
    )

    raw = message.content[0].text.strip()

    # Try extracting from fenced code block first
    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", raw)
    if match:
        raw = match.group(1).strip()

    # Fallback: extract outermost JSON object
    if not raw.startswith("{"):
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            raw = raw[start:end]

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        log.warning("JSON has errors, attempting auto-repair...")
        try:
            data = json.loads(repair_json(raw))
            log.info("JSON repaired successfully")
        except Exception as e:
            log.error(f"Could not repair JSON: {e}")
            log.error(f"Raw output: {raw[:500]}")
            raise

    log.info(f"Generated {len(data.get('endpoints', []))} endpoints")
    return data


def save_template(topic, data):
    category_dir = ROOT / topic["category"]
    category_dir.mkdir(exist_ok=True)
    out_path = category_dir / f"{topic['slug']}.json"
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info(f"Saved to {out_path}")
    return out_path


def count_endpoints(data):
    return len(data.get("endpoints", data.get("operations", [])))


def update_readme(topic, data):
    readme_path = ROOT / "README.md"
    content = readme_path.read_text(encoding="utf-8")

    # Build the new table row
    ep_count = count_endpoints(data)
    row = f"| [{topic['category']}/{topic['slug']}.json]({topic['category']}/{topic['slug']}.json) | {ep_count} | {data.get('description', topic['description'])[:80]} |"

    # Find the right section table or add to a "More Templates" section
    # Look for the last table in the file and append, or add a new section
    new_section_marker = "<!-- AUTO-GENERATED TEMPLATES -->"

    if new_section_marker in content:
        # Append row after the marker's table header
        content = content.replace(
            new_section_marker,
            new_section_marker + "\n" + row
        )
    else:
        # Add new section before the Contributing header
        new_section = f"""
## 🔄 More Templates

{new_section_marker}
| Template | Endpoints | Description |
|----------|-----------|-------------|
{row}

"""
        content = content.replace("## Contributing", new_section + "## Contributing")

    # Update last-updated date
    today = datetime.utcnow().strftime("%Y-%m-%d")
    content = re.sub(
        r"\*\*Last updated:.*?\*\*",
        f"**Last updated: {today}**",
        content
    )

    # Add last-updated line if not present
    if "Last updated:" not in content:
        content = content.replace(
            "[![Last updated]",
            f"**Last updated: {today}** · [![Last updated]"
        )

    readme_path.write_text(content, encoding="utf-8")
    log.info("README.md updated")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    topics = load_topics()
    topic = pick_next(topics, slug=args.slug)
    log.info(f"Selected: {topic['slug']}")

    data = generate_template(topic)

    if args.dry_run:
        print(json.dumps(data, indent=2))
        log.info("[DRY RUN] Not saving files")
        return

    save_template(topic, data)
    update_readme(topic, data)

    # Mark as published
    for t in topics:
        if t["slug"] == topic["slug"]:
            t["published"] = True
            t["published_at"] = datetime.utcnow().strftime("%Y-%m-%d")
            break
    save_topics(topics)
    log.info(f"Template '{topic['slug']}' marked as published")


if __name__ == "__main__":
    main()
