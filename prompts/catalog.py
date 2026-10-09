"""Load reviewed agent prompts from packaged resources, not the working directory."""

from importlib.resources import files

from schemas.config import AGENT_NAMES, AgentName


def load_prompt(
    agent: AgentName, *, authoring_version: int = 2, document_path: str | None = None
) -> str:
    if agent not in AGENT_NAMES:
        raise ValueError(f"Unknown agent: {agent}")
    if authoring_version not in {1, 2}:
        raise ValueError("Unknown authoring contract version")
    name = (
        f"{agent}.v1.md"
        if authoring_version == 1 and agent in {"analyst_agent", "writer_agent", "orchestrator"}
        else f"{agent}.md"
    )
    content = files("prompts").joinpath(name).read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"Prompt is empty: {agent}")
    return content.replace(
        "{content_path}", document_path or "output/{yyyy-mm-dd-hh-mm-ss}-content.md"
    )
