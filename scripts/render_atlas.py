#!/usr/bin/env python3
"""Render Agentic AI Atlas markdown from the phase modules."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from phases import PHASES  # noqa: E402

REQUIRED = (
    "day",
    "slug",
    "title",
    "level",
    "summary",
    "concept",
    "approach",
    "components",
    "flow",
    "stack",
    "setup",
    "done",
)
LEVELS = {"Beginner", "Intermediate", "Advanced"}
BANNED = (
    "100 days of",
    "100 Days of",
    "delve",
    "leverage",
    "it's worth noting",
    "cutting-edge",
    "tapestry",
)


def fail(msg: str) -> None:
    raise SystemExit(msg)


def validate(phases: list[dict]) -> list[dict]:
    projects = []
    seen_days = set()
    seen_slugs = set()
    for phase in phases:
        for key in ("id", "dir", "name", "blurb", "outcome", "goal", "skills", "projects"):
            if key not in phase:
                fail(f"phase {phase.get('id')} missing {key}")
        if len(phase["goal"].split()) < 30:
            fail(f"phase {phase['id']} goal is thin")
        if len(phase["skills"]) < 4:
            fail(f"phase {phase['id']} needs skills")
        for project in phase["projects"]:
            for key in REQUIRED:
                if key not in project:
                    fail(f"day {project.get('day')} missing {key}")
            day = project["day"]
            if day in seen_days:
                fail(f"duplicate day {day}")
            seen_days.add(day)
            slug = project["slug"]
            if slug in seen_slugs:
                fail(f"duplicate slug {slug}")
            seen_slugs.add(slug)
            if project["level"] not in LEVELS:
                fail(f"day {day} bad level {project['level']}")
            if len(project["summary"]) > 140:
                fail(f"day {day} summary is {len(project['summary'])} chars")
            if len(project["concept"].split()) < 80:
                fail(f"day {day} concept is thin ({len(project['concept'].split())} words)")
            if len(project["approach"].split()) < 60:
                fail(f"day {day} approach is thin ({len(project['approach'].split())} words)")
            if len(project["components"]) < 4:
                fail(f"day {day} needs at least 4 components")
            if len(project["flow"]) < 5:
                fail(f"day {day} flow is short")
            if len(project["stack"]) < 3:
                fail(f"day {day} stack is short")
            if len(project["setup"]) < 4:
                fail(f"day {day} setup is short")
            if len(project["done"]) < 4:
                fail(f"day {day} done is short")
            if project["level"] == "Advanced":
                ahead = project.get("ahead") or ""
                if len(ahead.split()) < 50:
                    fail(f"day {day} advanced project needs a Step ahead ({len(ahead.split())} words)")
            blob = " ".join(
                [
                    project["title"],
                    project["summary"],
                    project["concept"],
                    project["approach"],
                    project.get("ahead") or "",
                ]
            )
            for phrase in BANNED:
                if phrase.lower() in blob.lower() and phrase.lower().startswith("100 days"):
                    fail(f"day {day} contains banned phrasing {phrase}")
                if phrase in ("delve", "leverage", "it's worth noting", "cutting-edge", "tapestry"):
                    if phrase in blob.lower():
                        fail(f"day {day} contains '{phrase}'")
            project["_phase"] = phase
            projects.append(project)
    if seen_days != set(range(1, 101)):
        missing = sorted(set(range(1, 101)) - seen_days)
        extra = sorted(seen_days - set(range(1, 101)))
        fail(f"days must be 1..100 missing={missing} extra={extra}")
    return projects


def render_project(project: dict) -> str:
    phase = project["_phase"]
    lines = [
        f"# {project['title']}",
        "",
        f"**Day {project['day']:02d}** · **{project['level']}** · Phase {phase['id']}: {phase['name']}",
        "",
        project["summary"],
        "",
        "## Concept",
        "",
        project["concept"].strip(),
        "",
        "## Approach",
        "",
        project["approach"].strip(),
        "",
        "## Components",
        "",
        "| Piece | Role |",
        "| --- | --- |",
    ]
    for name, role in project["components"]:
        lines.append(f"| {name} | {role} |")
    lines += ["", "## How it works", ""]
    for i, step in enumerate(project["flow"], start=1):
        lines.append(f"{i}. {step}")
    lines += ["", "## Tech stack", ""]
    for item in project["stack"]:
        lines.append(f"- {item}")
    lines += ["", "## Setup", ""]
    for i, step in enumerate(project["setup"], start=1):
        lines.append(f"{i}. {step}")
    lines += ["", "## What done looks like", ""]
    for item in project["done"]:
        lines.append(f"- {item}")
    if project["level"] == "Advanced":
        lines += ["", "## Step ahead", "", project["ahead"].strip(), ""]
    else:
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_phase_readme(phase: dict) -> str:
    days = [p["day"] for p in phase["projects"]]
    lines = [
        f"# Phase {phase['id']}: {phase['name']}",
        "",
        f"Days {min(days):02d}–{max(days):02d}. {phase['blurb']}",
        "",
        "| Day | Level | Project | Summary |",
        "| --- | --- | --- | --- |",
    ]
    for project in phase["projects"]:
        href = f"day-{project['day']:02d}-{project['slug']}/README.md"
        lines.append(
            f"| {project['day']:02d} | {project['level']} | [{project['title']}]({href}) | {project['summary']} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_root(phases: list[dict]) -> str:
    lines = [
        "# Agentic AI Atlas",
        "",
        "A build curriculum for people who need to construct agent systems and explain them: measurement, classical learning, transformers, retrieval, tool-using agents, evaluation harnesses, analytics pipelines, and the system patterns that showed up once a chat window was no longer the product.",
        "",
        "Madan Mohan maintains this atlas as portfolio work for technical product management. Each folder is a project you can build, run, and talk through. The write-up is the spec: concept, approach, components, flow, stack, setup, and a definition of done. Advanced projects end with **Step ahead**, the next failure the first design will meet.",
        "",
        "**Read the full plan:** [PLAN.md](PLAN.md) is the consolidated document. It spells out every phase — goal, day range, and skills — and every project: concept, approach, components, flow, stack, setup, deliverable, and, for advanced projects, the step-ahead extension. The tables on this page are the catalog. The plan is the page you read straight through.",
        "",
        "Work in order if the material is new. Drop into a phase if you already know the earlier ground. Every project has an offline path. Hosted models are optional and named where they help.",
        "",
        "## Phase map",
        "",
        "| Phase | Days | Projects | What you leave able to do |",
        "| --- | --- | --- | --- |",
    ]
    for phase in phases:
        days = [p["day"] for p in phase["projects"]]
        lines.append(
            f"| [{phase['id']}. {phase['name']}](atlas/{phase['dir']}/README.md) | {min(days):02d}–{max(days):02d} | {len(phase['projects'])} | {phase['outcome']} |"
        )
    lines += [
        "",
        "## How a project folder works",
        "",
        "- Build only what that folder asks for. A finished project is a small program or notebook plus the checks in **What done looks like**.",
        "- Prefer the standard library early. Add a dependency when the folder names it, and pin it in that folder's notes.",
        "- When a model is involved, ship a scripted or fixture response first so the control flow is testable without a key.",
        "- Treat **Step ahead** as the design you would propose in a review, after the core path already works. Do not start there.",
        "",
        "## What this collection is for",
        "",
        "The atlas covers AI agents, retrieval-augmented generation, evals, eval harnesses, classical machine learning, data analytics, analytics workflows, data pipelines, transformers, and recent system patterns. It is a curriculum, not a framework. Projects stay separate so you can show one of them without dragging the other ninety-nine along.",
        "",
    ]
    for phase in phases:
        days = [p["day"] for p in phase["projects"]]
        lines += [
            f"## Phase {phase['id']}: {phase['name']}",
            "",
            f"Days {min(days):02d}–{max(days):02d}. {phase['blurb']}",
            "",
            "| Day | Level | Project | Summary |",
            "| --- | --- | --- | --- |",
        ]
        for project in phase["projects"]:
            href = f"atlas/{phase['dir']}/day-{project['day']:02d}-{project['slug']}/README.md"
            lines.append(
                f"| {project['day']:02d} | {project['level']} | [{project['title']}]({href}) | {project['summary']} |"
            )
        lines.append("")
    lines += [
        "## A note on scope",
        "",
        "These projects are original build briefs. They are not wrappers around a single vendor SDK, and they are not renames of other repositories. If a later day needs a score, a policy, or a trace, it specifies the narrow check for that day rather than a general platform.",
        "",
    ]
    return "\n".join(lines)


def render_plan(phases: list[dict]) -> str:
    lines = [
        "# Agentic AI Atlas — Full Plan",
        "",
        "This is the consolidated build plan for all eight phases and all 100 projects. Each project also has a folder of its own, linked below, with the same spec. Advanced projects include a step-ahead extension: the next failure the core design does not yet handle.",
        "",
        "The catalog of links lives in [README.md](README.md). This file is the plan written out in full.",
        "",
        "## Contents",
        "",
    ]
    for phase in phases:
        days = [p["day"] for p in phase["projects"]]
        lines.append(
            f"- [Phase {phase['id']}: {phase['name']}](#phase-{phase['id']}) — days {min(days):02d}–{max(days):02d}"
        )
    lines.append("")
    for phase in phases:
        days = [p["day"] for p in phase["projects"]]
        lines += [
            f"<a id=\"phase-{phase['id']}\"></a>",
            "",
            f"## Phase {phase['id']}: {phase['name']}",
            "",
            f"**Days {min(days):02d}–{max(days):02d}.** {len(phase['projects'])} projects.",
            "",
            "### Goal",
            "",
            phase["goal"].strip(),
            "",
            "### Skills covered",
            "",
        ]
        for skill in phase["skills"]:
            lines.append(f"- {skill}")
        lines += [
            "",
            phase["blurb"].strip(),
            "",
            f"By the end of the phase you should be able to: {phase['outcome']}",
            "",
        ]
        for project in phase["projects"]:
            href = f"atlas/{phase['dir']}/day-{project['day']:02d}-{project['slug']}/README.md"
            lines += [
                f"### Day {project['day']:02d} — {project['title']}",
                "",
                f"**Level:** {project['level']}",
                "",
                f"**Folder:** [{href}]({href})",
                "",
                project["summary"],
                "",
                "#### Concept",
                "",
                project["concept"].strip(),
                "",
                "#### Approach",
                "",
                project["approach"].strip(),
                "",
                "#### Components",
                "",
                "| Piece | Role |",
                "| --- | --- |",
            ]
            for name, role in project["components"]:
                lines.append(f"| {name} | {role} |")
            lines += ["", "#### How it works", ""]
            for i, step in enumerate(project["flow"], start=1):
                lines.append(f"{i}. {step}")
            lines += ["", "#### Tech stack", ""]
            for item in project["stack"]:
                lines.append(f"- {item}")
            lines += ["", "#### Setup", ""]
            for i, step in enumerate(project["setup"], start=1):
                lines.append(f"{i}. {step}")
            lines += ["", "#### Deliverable", ""]
            for item in project["done"]:
                lines.append(f"- {item}")
            if project["level"] == "Advanced":
                lines += ["", "#### Step ahead", "", project["ahead"].strip(), ""]
            else:
                lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    projects = validate(PHASES)
    atlas = ROOT / "atlas"
    # Remove previously rendered project trees so renamed slugs do not linger.
    if atlas.exists():
        for child in atlas.iterdir():
            if child.is_dir():
                for sub in child.rglob("*"):
                    if sub.is_file():
                        sub.unlink()
                for sub in sorted(child.rglob("*"), reverse=True):
                    if sub.is_dir():
                        sub.rmdir()
                child.rmdir()
    for phase in PHASES:
        phase_dir = atlas / phase["dir"]
        phase_dir.mkdir(parents=True, exist_ok=True)
        (phase_dir / "README.md").write_text(render_phase_readme(phase), encoding="utf-8")
        for project in phase["projects"]:
            folder = phase_dir / f"day-{project['day']:02d}-{project['slug']}"
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "README.md").write_text(render_project(project), encoding="utf-8")
    (ROOT / "README.md").write_text(render_root(PHASES), encoding="utf-8")
    plan = render_plan(PHASES)
    (ROOT / "PLAN.md").write_text(plan, encoding="utf-8")
    if plan.count("### Day ") != 100:
        fail(f"PLAN.md day headings = {plan.count('### Day ')}")
    print(f"rendered {len(projects)} projects and PLAN.md ({len(plan.splitlines())} lines)")


if __name__ == "__main__":
    main()
