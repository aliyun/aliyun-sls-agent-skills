#!/usr/bin/env python3
"""Main entry point for Aliyun SLS Agent Skills."""

import argparse
from dataclasses import dataclass
import os
import sys
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import questionary
    from questionary import Style
except ImportError:
    print(
        "Error: questionary is not installed. Please install it with: pip install questionary"
    )
    sys.exit(1)


# Custom style: no background for selected/highlighted items in checkbox/select.
# prompt_toolkit's default_ui_style uses ("selected", "reverse"); we override with noreverse.
_NO_BG_STYLE = Style(
    [
        ("selected", "noreverse"),
        ("highlighted", "noreverse"),
    ]
)


@dataclass
class InstallLocation:
    tool_name: str
    project_skills_dir: Optional[str]
    global_skills_dir: Optional[str]


@dataclass
class InstallContext:
    """Unified install parameters from headless args or interactive prompts."""

    tool_display_name: str
    install_path: str
    skills: List[str]


TOOL_CONFIGS: Dict[str, InstallLocation] = {
    "ClaudeCode": InstallLocation(
        tool_name="Claude Code",
        project_skills_dir=".claude/skills",
        global_skills_dir=".claude/skills",
    ),
    "OpenClaw": InstallLocation(
        tool_name="OpenClaw",
        project_skills_dir="skills",
        global_skills_dir=".openclaw/skills",
    ),
    "Cursor": InstallLocation(
        tool_name="Cursor",
        project_skills_dir=".cursor/skills",
        global_skills_dir=".cursor/skills",
    ),
    "Codex": InstallLocation(
        tool_name="Codex",
        project_skills_dir=".agents/skills",
        global_skills_dir=".agents/skills",
    ),
    "OpenCode": InstallLocation(
        tool_name="OpenCode",
        project_skills_dir=".opencode/skills",
        global_skills_dir=".config/opencode/skills",
    ),
    "GitHubCopilot": InstallLocation(
        tool_name="GitHub Copilot",
        project_skills_dir=".github/skills",
        global_skills_dir=".copilot/skills",
    ),
    "Qoder": InstallLocation(
        tool_name="Qoder",
        project_skills_dir=".qoder/skills",
        global_skills_dir=".qoder/skills",
    ),
    "Trae": InstallLocation(
        tool_name="Trae",
        project_skills_dir=".trae/skills",
        global_skills_dir=".trae/skills",
    ),
    "Iflow": InstallLocation(
        tool_name="Iflow",
        project_skills_dir=".iflow/skills",
        global_skills_dir=".iflow/skills",
    ),
    "Kiro": InstallLocation(
        tool_name="Kiro",
        project_skills_dir=".kiro/skills",
        global_skills_dir=".kiro/skills",
    ),
}

INSTALLABLE_SKILLS = [
    "aliyun-sls-cli-guidance",
]


def get_source_skills_dir() -> Path:
    package_dir = Path(__file__).parent
    # After installation: skills/ in package
    if (package_dir / "skills").exists():
        return package_dir / "skills"

    # During development: project root .agents/skills/ (package is in src/aliyun_sls_agent_skills/)
    root_skills = package_dir.parent.parent / ".agents" / "skills"
    if root_skills.exists():
        return root_skills
    raise FileNotFoundError("Skills directory not found")


def resolve_tool_key(name: str) -> Optional[str]:
    """Resolve tool name to TOOL_CONFIGS key (case-insensitive). Return None if not found."""
    if not name:
        return None
    key = name.strip()
    for k in TOOL_CONFIGS:
        if k.lower() == key.lower():
            return k
    return None


def get_tool_skills_path(tool_name: str) -> Tuple[str, str]:
    """Return (project_skills_dir, global_skills_dir) for the tool."""
    tool_config = TOOL_CONFIGS.get(tool_name)
    if not tool_config:
        raise ValueError(f"Unknown tool: {tool_name}")
    return (
        tool_config.project_skills_dir or "",
        tool_config.global_skills_dir or "",
    )


def copy_skill(
    source_skill_dir: Path, target_skills_dir: Path, skill_name: str
) -> bool:
    """Copy a skill directory to the target location."""
    target_skill_dir = target_skills_dir / skill_name

    try:
        # Remove existing skill if it exists
        if target_skill_dir.exists():
            shutil.rmtree(target_skill_dir)

        # Create parent directory if it doesn't exist
        target_skills_dir.mkdir(parents=True, exist_ok=True)

        # Copy the skill directory
        shutil.copytree(source_skill_dir, target_skill_dir)

        return True
    except Exception as e:
        print(f"Error copying skill {skill_name}: {e}")
        return False


def install_skills(
    tool: str,
    skills: List[str],
    project_root: Path,
    install_path: str,
) -> None:
    """Install selected skills to the given path. Always overwrites if already installed."""
    source_skills_dir = get_source_skills_dir()

    if not source_skills_dir.exists():
        print(f"Error: Skills directory not found at {source_skills_dir}")
        print("Please ensure the package is properly installed.")
        sys.exit(1)

    print(f"\n🔧 {tool} → {install_path}")
    for skill in skills:
        source_skill_dir = source_skills_dir / skill
        if not source_skill_dir.exists():
            print(f"   ⚠️  {skill} (not found, skip)")
            continue
        if copy_skill(source_skill_dir, Path(install_path), skill):
            print(f"   ✅ {skill}")
        else:
            print(f"   ❌ {skill} (failed)")
    print()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Aliyun SLS Agent Skills to AI coding tools.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Headless mode (-b, no prompts; -y = skip confirmation):
  %(prog)s -b --scope project --tool Cursor -y
  %(prog)s -b --scope global --tool codex --skills aliyun-sls-cli-guidance
""",
    )
    parser.add_argument(
        "-b",
        "--batch",
        action="store_true",
        dest="batch",
        help="Headless mode: use --scope, --tool (--skills optional, empty = all).",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        dest="yes",
        help="Skip the final 'Proceed with installation?' confirmation.",
    )
    parser.add_argument(
        "--scope",
        choices=["global", "project"],
        help="Install scope: project = current working dir, global = user home.",
    )
    parser.add_argument(
        "--tool",
        metavar="TOOL",
        help="Target tool, case-insensitive. Supported: %s."
        % ", ".join(TOOL_CONFIGS.keys()),
    )
    parser.add_argument(
        "--skills",
        metavar="SKILLS",
        default="",
        help="Skills to install: empty = all, or comma-separated (e.g. aliyun-sls-cli-guidance).",
    )
    return parser.parse_args()


def collect_context_from_args(args: argparse.Namespace) -> Optional[InstallContext]:
    """Build InstallContext from CLI args. Returns None if headless args are incomplete or invalid."""
    if not all([args.scope, args.tool]):
        return None
    tool_key = resolve_tool_key(args.tool)
    if tool_key is None:
        return None
    project_install_path, global_install_path = get_tool_skills_path(tool_key)
    if args.scope == "global":
        install_path = os.path.join(os.path.expanduser("~"), global_install_path)
    else:
        install_path = os.path.join(os.getcwd(), project_install_path)

    skills_arg = (args.skills or "").strip()
    if not skills_arg or skills_arg == "*":
        skills_list = list(INSTALLABLE_SKILLS)
    else:
        skills_list = [s.strip() for s in skills_arg.split(",") if s.strip()]
    if not skills_list:
        return None
    config = TOOL_CONFIGS[tool_key]
    return InstallContext(
        tool_display_name=config.tool_name,
        install_path=install_path,
        skills=skills_list,
    )


def collect_context_interactive() -> Optional[InstallContext]:
    """Build InstallContext via interactive prompts. Returns None if user cancels."""
    try:
        print("🚀 Aliyun SLS Agent Skills Installer")
        print("=" * 50)

        print("\n📋 Select tool to install to:")
        selected_tool = questionary.select(
            "Select one tool (use ↑↓ to navigate, Enter to confirm, Ctrl+C to cancel):",
            choices=list(TOOL_CONFIGS.keys()),
            style=_NO_BG_STYLE,
        ).ask()

        if not selected_tool:
            return None

        project_install_path, global_install_path = get_tool_skills_path(selected_tool)
        project_choice_display = f"Project ({project_install_path})"
        global_choice_display = f"Global (~/{global_install_path})"
        chosen = questionary.select(
            "Select install path:",
            choices=[project_choice_display, global_choice_display],
            default=project_choice_display,
            style=_NO_BG_STYLE,
        ).ask()

        if chosen == global_choice_display:
            install_path = os.path.join(os.path.expanduser("~"), global_install_path)
        else:
            install_path = os.path.join(os.getcwd(), project_install_path)

        print(f"\n📁 Skills will be installed to: {install_path}")

        print("\n📦 Select skills to install:")
        selected_skills = questionary.checkbox(
            "Select skills (use ↑↓ to navigate, Space to select, Enter to confirm, Ctrl+C to cancel):",
            choices=INSTALLABLE_SKILLS,
            default="aliyun-sls-cli-guidance",
            instruction="(Select multiple with Space)",
            style=_NO_BG_STYLE,
        ).ask()

        if not selected_skills:
            return None

        config = TOOL_CONFIGS[selected_tool]
        return InstallContext(
            tool_display_name=config.tool_name,
            install_path=install_path,
            skills=selected_skills,
        )
    except KeyboardInterrupt:
        return None


def run(context: InstallContext, skip_confirm: bool) -> None:
    """Execute install: if not skip_confirm, show summary and confirm; then install."""
    print("\n📝 Installation Summary:")
    print(f"  Tool: {context.tool_display_name}")
    print(f"  Skills: {', '.join(context.skills)}")
    print(f"  Install path: {context.install_path}")

    if not skip_confirm:
        try:
            proceed = questionary.confirm(
                "Proceed with installation?",
                default=True,
                style=_NO_BG_STYLE,
            ).ask()
        except KeyboardInterrupt:
            print("\n\nInstallation cancelled by user.")
            sys.exit(0)
        if not proceed:
            print("Installation cancelled.")
            return

    install_skills(
        context.tool_display_name,
        context.skills,
        Path.cwd(),
        context.install_path,
    )
    print("✨ Installation complete")
    print("\n💡 Please verify the skills are available in your tool's skill directory")


def main():
    """Main entry point: collect context (headless or interactive), then run with optional confirm."""
    args = _parse_args()

    if args.batch and all([args.scope, args.tool]):
        context = collect_context_from_args(args)
        if context is None:
            if args.tool and resolve_tool_key(args.tool) is None:
                print(f"Error: unknown tool '{args.tool}'.")
            else:
                print(
                    "Error: no valid skills from --skills (empty = all, or comma-separated names)."
                )
            sys.exit(1)
    else:
        if args.batch:
            print(
                "Error: headless mode (-b) requires --scope and --tool (--skills empty = all)."
            )
            sys.exit(1)
        context = collect_context_interactive()
        if context is None:
            print("\nInstallation cancelled by user.")
            sys.exit(0)

    run(context, skip_confirm=args.batch or args.yes)


if __name__ == "__main__":
    main()
