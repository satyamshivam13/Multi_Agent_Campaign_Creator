"""
CampaignCrew — orchestrates agents + tasks via CrewAI.

    crew = CampaignCrew(request)
    brief = crew.run()
"""

from __future__ import annotations

from datetime import datetime

from crewai import Crew, Process
from rich.console import Console
from rich.panel import Panel

from src.agents import (
    create_art_director_agent,
    create_copywriter_agent,
    create_manager_agent,
    create_research_agent,
)
from src.config import settings
from src.models.campaign_models import (
    CampaignBrief,
    CampaignRequest,
    CopyPackage,
    MarketResearch,
    VisualDirection,
)
from src.tasks.campaign_tasks import CampaignTaskFactory

console = Console()


class CampaignCrew:
    """High-level facade around a CrewAI crew."""

    def __init__(self, request: CampaignRequest) -> None:
        self.request = request
        self._factory = CampaignTaskFactory(request)

        # Build agents
        console.print("  [dim]Creating Research Agent...[/dim]")
        self.researcher = create_research_agent()

        console.print("  [dim]Creating Copywriter Agent...[/dim]")
        self.copywriter = create_copywriter_agent()

        console.print("  [dim]Creating Art Director Agent...[/dim]")
        self.art_director = create_art_director_agent()

        console.print("  [dim]Creating Manager Agent...[/dim]")
        self.manager = create_manager_agent()

        # Build tasks (order matters)
        self.research_task = self._factory.research_task(self.researcher)
        self.copy_task = self._factory.copywriting_task(
            self.copywriter, self.research_task
        )
        self.art_task = self._factory.art_direction_task(
            self.art_director, self.research_task, self.copy_task
        )
        self.manager_task = self._factory.manager_task(
            self.manager, self.research_task, self.copy_task, self.art_task
        )

        # Assemble the crew
        self.crew = Crew(
            agents=[
                self.researcher,
                self.copywriter,
                self.art_director,
                self.manager,
            ],
            tasks=[
                self.research_task,
                self.copy_task,
                self.art_task,
                self.manager_task,
            ],
            process=Process.sequential,
            verbose=True,
        )

    def run(self) -> CampaignBrief:
        """Execute the full workflow and return a structured brief."""
        console.print(
            "\n[bold cyan]═══ AGENT WORKFLOW STARTING ═══[/bold cyan]\n"
        )

        # Kick off CrewAI execution
        result = self.crew.kickoff()

        # Get the raw output string
        raw_output = str(result)

        console.print(
            "\n[bold cyan]═══ AGENT WORKFLOW COMPLETE ═══[/bold cyan]\n"
        )

        # Build structured brief
        brief = self._build_brief(raw_output)

        # Save to disk
        self._save_outputs(brief, raw_output)

        return brief

    def _build_brief(self, raw_output: str) -> CampaignBrief:
        """Wrap raw crew output into a typed CampaignBrief."""
        return CampaignBrief(
            client_name=self.request.product_name,
            campaign_name=f"{self.request.product_name} Campaign",
            objective=self.request.campaign_goals,
            target_audience=self.request.target_audience,
            request=self.request,
            research=MarketResearch(
                market_summary="See full Markdown brief for detailed research."
            ),
            copy_package=CopyPackage(
                campaign_tagline="See full Markdown brief for tagline.",
                elevator_pitch="See full Markdown brief for pitch.",
            ),
            visuals=VisualDirection(
                brand_visual_identity="See full Markdown brief for visuals."
            ),
            executive_summary=raw_output[:3000],
            final_recommendations=raw_output,
        )

    def _save_outputs(self, brief: CampaignBrief, raw_output: str) -> None:
        """Save the campaign brief as Markdown and JSON."""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = self.request.product_name.lower().replace(" ", "_")[:30]
        base = settings.output_dir / f"{slug}_{ts}"

        # Save Markdown
        md_path = base.with_suffix(".md")
        md_content = self._format_markdown(brief, raw_output)
        md_path.write_text(md_content, encoding="utf-8")
        console.print(f"\n[green]✓ Saved Markdown:[/green] {md_path}")

        # Save JSON
        json_path = base.with_suffix(".json")
        json_path.write_text(
            brief.model_dump_json(indent=2), encoding="utf-8"
        )
        console.print(f"[green]✓ Saved JSON:[/green]     {json_path}")

    def _format_markdown(
        self, brief: CampaignBrief, raw_output: str
    ) -> str:
        """Create a well-formatted Markdown document."""
        channels = ", ".join(c.value for c in self.request.channels)
        return f"""# {brief.campaign_name}

**Generated:** {brief.created_at.strftime("%Y-%m-%d %H:%M:%S")}

---

## Campaign Configuration

| Field | Value |
|-------|-------|
| **Product** | {self.request.product_name} |
| **Description** | {self.request.product_description} |
| **Target Audience** | {self.request.target_audience} |
| **Goals** | {self.request.campaign_goals} |
| **Budget** | {self.request.budget_range or "Not specified"} |
| **Channels** | {channels} |
| **Brand Voice** | {self.request.brand_voice.value} |

---

## Full Campaign Brief

{raw_output}

---

*Generated by Multi-Agent Campaign Creator*
"""
