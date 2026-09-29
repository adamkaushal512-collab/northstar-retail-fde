import re
from pathlib import Path

from .investigation import PolicySection


def _tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 2}


def load_policy(path: str | Path) -> tuple[PolicySection, ...]:
    content = Path(path).read_text(encoding="utf-8")
    metadata: dict[str, str] = {}
    sections: list[PolicySection] = []
    current_title = "Policy"
    current_lines: list[str] = []

    for line in content.splitlines():
        if line.startswith(("policy_id:", "version:")):
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
        elif line.startswith("## "):
            if current_lines:
                sections.append(_section(metadata, current_title, current_lines))
            current_title = line[3:].strip()
            current_lines = []
        elif current_title != "Policy" and line.strip():
            current_lines.append(line.strip())

    if current_lines:
        sections.append(_section(metadata, current_title, current_lines))
    return tuple(sections)


def _section(metadata: dict[str, str], title: str, lines: list[str]) -> PolicySection:
    return PolicySection(
        policy_id=metadata.get("policy_id", "UNKNOWN"),
        version=metadata.get("version", "UNKNOWN"),
        title=title,
        text=" ".join(lines),
    )


def retrieve_policy(
    query: str,
    sections: tuple[PolicySection, ...],
    *,
    limit: int = 2,
) -> tuple[PolicySection, ...]:
    query_tokens = _tokens(query)
    ranked = sorted(
        sections,
        key=lambda section: len(query_tokens & _tokens(section.title + " " + section.text)),
        reverse=True,
    )
    return tuple(section for section in ranked if _tokens(section.title + " " + section.text) & query_tokens)[:limit]
