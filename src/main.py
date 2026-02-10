#!/usr/bin/env python3
"""
CLI entry-point for the Multi-Agent Campaign Creator.

Usage:
    python -m src.main --demo        # Run with sample product
    python -m src.main               # Interactive mode
"""

from __future__ import annotations

import argparse
import sys
import traceback

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.models.campaign_models import (
    CampaignChannel,
    CampaignRequest,
    CopyTone,
)
from src.workflow.crew_workflow import CampaignCrew

console = Console()


# ── Demo preset ──────────────────────────────────────────────────────

DEMO_REQUEST = CampaignRequest(
    product_name="AeroFlow Pro",
    product_description=(
        "A smart, AI-powered air purifier that learns your air-quality "
        "preferences, adapts to pollen and pollution levels in real time, "
        "and integrates with smart-home ecosystems like Alexa and Google Home."
    ),
    target_audience=(
        "Health-conscious millennials and Gen-Z professionals aged 25-38 "
        "living in urban apartments who value clean air, modern design "
        "aesthetics, and smart-home technology."
    ),
    campaign_goals=(
        "Drive 10,000 pre-orders in 60 days via Kickstarter, build brand "
        "awareness among target demographic, achieve 5% social-media "
        "engagement rate."
    ),
    budget_range="$50,000 - $100,000",
    channels=[
        CampaignChannel.SOCIAL_MEDIA,
        CampaignChannel.EMAIL,
        CampaignChannel.DISPLAY_ADS,
        CampaignChannel.INFLUENCER,
    ],
    brand_voice=CopyTone.PROFESSIONAL,
    additional_context=(
        "Launching on Kickstarter first, then moving to D2C website. "
        "Key competitors include Dyson Pure Cool, Molekule Air, and "
        "Coway Airmega. Our differentiator is the AI-learning feature "
        "that adapts to individual preferences over time."
    ),
)


# ── Channel and tone lookups ─────────────────────────────────────────

CHANNEL_MAP = {c.value: c for c in CampaignChannel}
TONE_MAP = {t.value: t for t in CopyTone}


def gather_request_interactive() -> CampaignRequest:
    """Gather campaign parameters from user input."""
    console.print(
        Panel(
            "[bold]Let's set up your marketing campaign.[/bold]\n"
            "Answer the following questions to brief the AI team.",
            title="📝 Campaign Setup",
            border_style="cyan",
        )
    )

    product_name = Prompt.ask("\n[bold]Product / brand name[/bold]")

    product_desc = Prompt.ask(
        "[bold]Describe the product[/bold] (1-2 sentences)"
    )

    audience = Prompt.ask("[bold]Target audience[/bold]")

    goals = Prompt.ask("[bold]Campaign goals / KPIs[/bold]")

    budget = Prompt.ask(
        "[bold]Budget range[/bold] (optional)",
        default="Not specified",
    )

    console.print(
        f"\n[dim]Available channels:[/dim] {', '.join(CHANNEL_MAP.keys())}"
    )
    raw_channels = Prompt.ask(
        "[bold]Channels[/bold] (comma-separated)",
        default="social_media",
    )
    channels = []
    for ch in raw_channels.split(","):
        ch = ch.strip().lower()
        if ch in CHANNEL_MAP:
            channels.append(CHANNEL_MAP[ch])
    if not channels:
        channels = [CampaignChannel.SOCIAL_MEDIA]

    console.print(
        f"\n[dim]Available tones:[/dim] {', '.join(TONE_MAP.keys())}"
    )
    tone_str = Prompt.ask(
        "[bold]Brand voice / tone[/bold]",
        default="professional",
    )
    tone = TONE_MAP.get(tone_str.strip().lower(), CopyTone.PROFESSIONAL)

    extra = Prompt.ask(
        "[bold]Additional context[/bold] (optional, press Enter to skip)",
        default="",
    )

    return CampaignRequest(
        product_name=product_name,
        product_description=product_desc,
        target_audience=audience,
        campaign_goals=goals,
        budget_range=budget if budget != "Not specified" else None,
        channels=channels,
        brand_voice=tone,
        additional_context=extra if extra else None,
    )


def display_request_summary(request: CampaignRequest) -> None:
    """Show what we're about to run."""
    channels_str = ", ".join(c.value for c in request.channels)
    summary = (
        f"[bold cyan]Product:[/bold cyan] {request.product_name}\n"
        f"[bold]Description:[/bold] {request.product_description[:100]}...\n"
        f"[bold]Audience:[/bold] {request.target_audience[:80]}...\n"
        f"[bold]Goals:[/bold] {request.campaign_goals[:80]}...\n"
        f"[bold]Channels:[/bold] {channels_str}\n"
        f"[bold]Tone:[/bold] {request.brand_voice.value}\n"
        f"[bold]Budget:[/bold] {request.budget_range or 'Not specified'}"
    )
    console.print(
        Panel(
            summary,
            title="🚀 Campaign Configuration",
            border_style="bright_blue",
        )
    )


def run_campaign(request: CampaignRequest) -> None:
    """Execute the full multi-agent campaign workflow."""

    display_request_summary(request)

    console.print("\n[bold yellow]Initializing AI agent team...[/bold yellow]\n")

    # Build the crew
    try:
        crew = CampaignCrew(request)
    except Exception as exc:
        console.print(f"[bold red]Failed to initialize crew:[/bold red] {exc}")
        console.print(
            "\n[yellow]Hint: Check your .env file has a valid API key.[/yellow]"
        )
        traceback.print_exc()
        sys.exit(1)

    console.print("[green]✓[/green] Agent team assembled:")
    console.print("  🔍 Research Agent — Market trends & competitor analysis")
    console.print("  ✍️  Copywriter Agent — Ad copy & messaging")
    console.print("  🎨 Art Director Agent — Visual direction & image prompts")
    console.print("  📋 Manager Agent — Final brief assembly")
    console.print()

    # Execute
    console.print(
        Panel(
            "[bold]Running campaign workflow...[/bold]\n"
            "Each agent will work sequentially, building on previous results.\n"
            "This typically takes 2-5 minutes depending on your LLM provider.",
            title="⏳ Execution Started",
            border_style="yellow",
        )
    )
    console.print()

    try:
        brief = crew.run()
        console.print(
            Panel(
                f"[bold green]Campaign '{brief.campaign_name}' "
                f"completed successfully![/bold green]\n\n"
                f"[bold]Executive Summary:[/bold]\n"
                f"{brief.executive_summary[:800]}...\n\n"
                f"[dim]Full brief saved to src/output/[/dim]",
                title="✅ Campaign Complete",
                border_style="green",
            )
        )
    except Exception as exc:
        console.print(
            Panel(
                f"[bold red]Campaign execution failed:[/bold red]\n\n{exc}\n\n"
                "[yellow]Common fixes:[/yellow]\n"
                "1. Check your API key is valid and has credits\n"
                "2. Check your internet connection\n"
                "3. Try a different model in .env\n"
                "4. Check the full traceback below",
                title="❌ Error",
                border_style="red",
            )
        )
        traceback.print_exc()
        sys.exit(1)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Multi-Agent Marketing Campaign Creator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python -m src.main --demo    Run with sample product\n"
            "  python -m src.main           Interactive mode\n"
        ),
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run with the built-in demo product (AeroFlow Pro)",
    )
    args = parser.parse_args()

    console.print(
        Panel(
            "[bold bright_blue]Multi-Agent Marketing Campaign Creator[/bold bright_blue]\n"
            "[dim]Powered by CrewAI — 4 specialized AI agents collaborating[/dim]",
            border_style="bright_blue",
        )
    )

    try:
        if args.demo:
            console.print("\n[cyan]Running demo campaign for AeroFlow Pro...[/cyan]\n")
            request = DEMO_REQUEST
        else:
            request = gather_request_interactive()

        run_campaign(request)

    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled by user.[/yellow]")
        sys.exit(0)


if __name__ == "__main__":
    main()