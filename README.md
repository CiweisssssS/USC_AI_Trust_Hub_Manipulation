# AI Trust Manipulation Index

**USC AI Trust Lab** · Research repository for the Manipulation Index project.

This repository tracks the testing framework, methodology, and experimental results for evaluating manipulative behaviors in large language models (LLMs).

---

## Repository Structure

```
ai-trust-manipulation-index/
│
├── framework/
│   └── dimension_definitions_finalized.pdf   # 20-dimension manipulation framework (v7)
│
├── methodology/
│   └── testing_protocol_finalized.md         # Core testing protocol (v9, latest)
│
├── visualization/
│   └── manipulation_test_design_final.html   # Interactive framework overview (open in browser)
│
├── pilot/                                    # Pilot experiment code & results
│   ├── run_pilot.py                          # Entry point
│   ├── runner.py / judge_rubric.py / ...     # Supporting modules
│   ├── analysis.ipynb                        # Results analysis notebook
│   └── results/                             # Raw outputs, figures, summary CSV
│
└── archive/
    ├── testing_methodology_v8.pdf            # Earlier methodology version
    └── agent_implementation_v8.pdf           # Agent implementation guide (v8)
```

---

## Project Overview

The Manipulation Index is a structured evaluation framework that tests LLM behavior across **20 manipulation dimensions**, organized along two axes:

- **Turn structure:** Single-turn (non-cumulative) vs. Multi-turn (cumulative)
- **Direction:** User → Model vs. Model → User

Testing operates across two layers:

| Layer | What it measures |
|---|---|
| Layer 1 (Prompt-Output) | Does the model's response contain a manipulation signal? |
| Layer 2 (Agent-Based) | Does the model's output produce measurable cognitive effects? |

---

## Pilot Experiment

The pilot covers **2 dimensions** (Dir. 7 Belief Steering, Dir. 9 Epistemic Manipulation) × **3 difficulty levels** × **3 user personas**, using Layer 2 agent-based behavioral testing.

To run:
```bash
cd pilot/
export ANTHROPIC_API_KEY=your_key_here
python run_pilot.py
```

Results are saved to `pilot/results/`. Open `analysis.ipynb` to review figures and summary statistics.

---

*USC AI Trust Lab · Manipulation Index Project*
