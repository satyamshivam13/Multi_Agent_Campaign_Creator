"""Central configuration module.

Loads environment variables and provides validated settings
used across all agents, tools, and workflows.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
	"""Immutable application settings loaded once from environment."""

	groq_api_key: str = field(
		default_factory=lambda: os.getenv("GROQ_API_KEY", "")
	)
	groq_model: str = field(
		default_factory=lambda: os.getenv(
			"GROQ_MODEL", "llama-3.3-70b-versatile"
		)
	)
	temperature: float = field(
		default_factory=lambda: float(os.getenv("GROQ_TEMPERATURE", "0.7"))
	)
	serper_api_key: str = field(
		default_factory=lambda: os.getenv("SERPER_API_KEY", "")
	)
	output_dir: Path = field(
		default_factory=lambda: Path(os.getenv("OUTPUT_DIR", "src/output"))
	)

	def __post_init__(self) -> None:
		if not self.groq_api_key:
			raise EnvironmentError(
				"GROQ_API_KEY is required. Set it in your .env file."
			)
		# Ensure output directory exists
		self.output_dir.mkdir(parents=True, exist_ok=True)

	@property
	def has_serper(self) -> bool:
		"""Check whether real web-search is available."""
		return bool(self.serper_api_key)


# Module-level singleton — import this everywhere
settings = Settings()
