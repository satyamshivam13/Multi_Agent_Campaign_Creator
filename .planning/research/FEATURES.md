# Feature Landscape

**Domain:** AI-assisted campaign generation (multi-agent, CLI-first)
**Project:** Multi-Agent Campaign Creator
**Researched:** 2026-04-14

## Table Stakes

Features users now expect by default. Missing these makes the product feel unreliable or low-quality.

| Feature | Why Expected in 2026 | Complexity | Dependency Notes (Repo-Tailored) |
|---------|----------------------|------------|----------------------------------|
| Structured brief outputs (JSON + readable doc) | Teams expect machine-readable and human-readable artifacts from one run | Low | Already present in workflow output save path; extend schema fields before adding new renderers |
| Deterministic run metadata (run_id, config snapshot, model, timestamps) | Reliability debugging now requires full run traceability | Medium | Add run metadata model + persist in output files; wire from CLI and workflow bootstrap |
| Retry + bounded backoff for provider throttling | Provider rate limiting is normal for production AI usage | Low | Baseline exists; expand beyond kickoff loop to task-level retry and classify transient vs hard failures |
| Guardrailed schema validation before final save | Quality requires rejecting malformed or partial outputs | Medium | Tighten Pydantic validation, add post-run validator layer, fail with actionable error report |
| Channel-aware copy constraints | Campaign quality is judged on channel fit (length, CTA, tone) | Low | Build on existing copy evaluator and channel enums; enforce hard pass/fail thresholds |
| Consistent brand voice controls | Brand drift is unacceptable in campaign generation | Medium | Expand current brand_voice enum into reusable style rules consumed by copy and manager tasks |
| Basic human review gates | Teams expect approve/reject before handoff | Medium | Add CLI checkpoints per stage with --auto mode for non-interactive runs |
| Reproducible rerun mode | Reliability expectation: same brief + seed yields comparable output | Medium | Add seed/config lock and input hashing; attach to output metadata |

## Differentiators

Features that create clear product advantage for this repo in reliability and output quality.

| Feature | Value Proposition | Complexity | Dependency Notes (Repo-Tailored) |
|---------|-------------------|------------|----------------------------------|
| Two-pass manager QA (draft -> critique -> revised final) | Raises output quality without requiring extra human effort every run | Medium | Add manager critique task after art/copy and before final packaging |
| Multi-agent evidence ledger (which claim came from which tool/result) | Increases trust and reduces hallucinated strategy claims | High | Capture tool outputs as structured evidence objects and require manager citations |
| Reliability mode profiles (fast, balanced, strict) | Users can tune cost/latency vs robustness per campaign | Medium | Map profile to retries, token budget, validation strictness, and optional second-pass QA |
| KPI realism checker against objective + budget + channels | Prevents low-quality plans with impossible metrics | Medium | Add deterministic tool to score KPI plausibility and block low-confidence plans |
| Campaign quality scorecard with failure reasons | Makes output quality measurable and improvable over time | Medium | Extend current copy scoring into campaign-level rubric; persist score + rule-level diagnostics |
| Partial-failure recovery with resumable stages | Improves reliability under flaky provider/network conditions | High | Persist intermediate stage artifacts; add --resume from last successful stage |
| Variant generation with automatic winner recommendation | Better campaign quality by testing alternatives, not single output | Medium | Generate 2-3 copy/angle variants and rank using scorecard + channel constraints |
| Grounded competitor/trend deltas per run | Keeps strategy fresh instead of repeating stale generic patterns | Medium | Rework deterministic tools to optionally use live connectors when API keys exist |

## Anti-Features

Features to explicitly avoid for this CLI milestone, because they reduce reliability focus or conflict with product constraints.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| GUI/dashboard buildout now | High surface area distracts from reliability and output quality core | Keep CLI-first; emit rich artifacts that can be consumed by external UI later |
| Unbounded autonomous agent loops | Increases token burn and unstable behavior | Keep explicit sequential stages with hard stop conditions |
| Adding many LLM providers immediately | Expands failure matrix before reliability hardening is complete | Stabilize Groq path first; add model abstraction only after observability baseline |
| Free-form JSON blobs without schema contracts | Causes downstream breakage and hard-to-debug quality regressions | Keep strict Pydantic schemas and explicit versioned output contract |
| “One-click publish” integrations in this phase | Raises risk (bad outputs shipped directly) before quality guardrails mature | Add export targets first; keep human approval as mandatory gate |

## Feature Dependencies

```text
Run metadata + config snapshot -> Reliable debugging + resume
Schema hardening -> Campaign scorecard -> Variant winner recommendation
Task-level retry policy -> Partial-failure recovery
Brand voice rules -> Channel-aware constraints -> Higher copy consistency
Evidence ledger -> Manager QA pass -> Trustworthy final recommendations
```

## MVP Recommendation (Next Subsequent Milestone)

Prioritize:
1. Deterministic run metadata + config snapshot + stage timings (table stake reliability base)
2. Task-level retries + transient/hard error classification + resumable stages
3. Two-pass manager QA + campaign scorecard (output quality control loop)
4. KPI realism checker (quality guardrail tied to budget/channels/objective)

Defer:
- Full multi-provider routing: defer until observability and failure taxonomy are stable
- GUI workflow management: defer until CLI reliability and output quality KPIs are consistently met

## Confidence Notes

- **HIGH:** Repo-specific feasibility and dependency mapping (validated against current code structure and models)
- **MEDIUM:** 2026 market expectations around workflow orchestration, model-agnostic controls, and governance (supported by current platform positioning from major AI work platforms)
- **LOW:** Vendor-specific prevalence percentages (not included due insufficient verifiable comparative benchmark data in this run)

## Sources

- Project context and constraints: .planning/PROJECT.md (internal)
- Existing capability baseline: src/workflow/crew_workflow.py, src/models/campaign_models.py, src/tools/copy_evaluation_tool.py, src/config.py (internal)
- External market signal (retrieved): https://www.copy.ai/workflows (workflow orchestration, brand voice/intelligence layer positioning)
- External market signal (retrieved): https://www.notion.com/product/ai (custom agents, model-agnostic controls, governance/admin expectations)
- Retrieval gaps encountered: multiple vendor pages were anti-bot/redirect heavy during fetch and were not used as primary evidence in this draft
