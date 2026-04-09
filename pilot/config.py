"""
Pilot configuration — USC AI Trust Lab Manipulation Index
"""
import os

# ── Models ──────────────────────────────────────────────────────────────────
TESTED_MODEL = "claude-sonnet-4-6"   # The model under evaluation
JUDGE_MODEL  = "claude-sonnet-4-6"   # LLM Judge (same model, different role — pilot limitation)
AGENT_MODEL  = "claude-sonnet-4-6"   # UserAgent persona model

# NOTE: Using the same model for all three roles introduces "shared blind spots"
# as flagged in the methodology. This is acceptable for the pilot; full scale
# should use a different model family for the Judge.

# ── API ──────────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ── Dimensions under test ────────────────────────────────────────────────────
DIMENSIONS = ["Dir7_BeliefSteering", "Dir9_EpistemicManipulation"]

# ── Difficulty levels ────────────────────────────────────────────────────────
LEVELS = ["L1", "L2", "L3"]

# ── Persona IDs ──────────────────────────────────────────────────────────────
PERSONA_IDS = ["P1_NeutralSkeptic", "P2_AnxiousAccepter", "P3_ReactiveDobter"]

# ── Conversation turns ───────────────────────────────────────────────────────
# Single-turn for both Dir 7 and Dir 9 in this pilot
# (Layer 2 multi-turn accumulation dimensions are Dir 17/19/20 — out of pilot scope)
TURNS_PER_SESSION = 1

# ── Output ───────────────────────────────────────────────────────────────────
RESULTS_DIR = "results"
