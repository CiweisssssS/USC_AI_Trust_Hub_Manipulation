"""
Main entry point for the manipulation index pilot experiment.

Runs:
  - 2 dimensions × 3 levels × 3 personas = 18 sessions
  - 1 mirror test for Dir 7 (2 framing runs)

Outputs per session: results/{dimension}_{level}_{persona}.json
Summary of all sessions: results/summary.csv

Usage:
  export ANTHROPIC_API_KEY=sk-...
  cd pilot/
  python run_pilot.py
"""

import csv
import json
import os
import sys
import traceback

import anthropic

from config import (
    ANTHROPIC_API_KEY,
    DIMENSIONS,
    LEVELS,
    PERSONA_IDS,
    RESULTS_DIR,
)
from runner import run_session, run_mirror_test
from test_cases import MIRROR_TEST


def save_json(data: dict, filename: str):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Saved: {path}")


def write_summary_csv(all_results: list):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, "summary.csv")
    fieldnames = [
        "dimension", "level", "persona",
        "layer1_score", "layer1_signal_detected", "layer1_failure_signals",
        "confidence_delta", "certainty_delta", "seek_sources_delta",
        "agreement_delta", "balance_delta",
        "influence_detected",
        "probe_failure", "probe_failure_signals",
        "layer1_reasoning",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in all_results:
            if r.get("test_type") == "mirror_test":
                continue  # mirror test written separately
            delta = r.get("delta", {})
            writer.writerow({
                "dimension": r["dimension"],
                "level": r["level"],
                "persona": r["persona"],
                "layer1_score": r.get("layer1_score", ""),
                "layer1_signal_detected": r.get("layer1_signal_detected", ""),
                "layer1_failure_signals": "; ".join(r.get("layer1_failure_signals", [])),
                "confidence_delta": delta.get("confidence", ""),
                "certainty_delta": delta.get("certainty", ""),
                "seek_sources_delta": delta.get("seek_sources", ""),
                "agreement_delta": delta.get("agreement", ""),
                "balance_delta": delta.get("balance", ""),
                "influence_detected": r.get("influence_interpretation", {}).get("influence_detected", ""),
                "probe_failure": r.get("probe_judgment", {}).get("probe_failure", ""),
                "probe_failure_signals": "; ".join(
                    r.get("probe_judgment", {}).get("failure_indicators_triggered", [])
                ),
                "layer1_reasoning": r.get("layer1_reasoning", ""),
            })
    print(f"\nSummary CSV written: {path}")


def main():
    if not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    all_results = []
    errors = []

    total = len(DIMENSIONS) * len(LEVELS) * len(PERSONA_IDS)
    completed = 0

    print(f"\n{'='*60}")
    print(f"USC AI Trust Lab — Manipulation Index Pilot Experiment")
    print(f"Dimensions: {DIMENSIONS}")
    print(f"Total sessions: {total} + 1 mirror test")
    print(f"{'='*60}\n")

    # ── Main sessions ──────────────────────────────────────────────────────────
    for dimension in DIMENSIONS:
        for level in LEVELS:
            for persona_id in PERSONA_IDS:
                try:
                    result = run_session(client, dimension, level, persona_id)
                    all_results.append(result)
                    filename = f"{dimension}_{level}_{persona_id}.json"
                    save_json(result, filename)
                    completed += 1
                    print(f"  Progress: {completed}/{total}")
                except Exception as e:
                    err_msg = f"FAILED: {dimension}/{level}/{persona_id} — {e}"
                    print(f"\n  {err_msg}")
                    traceback.print_exc()
                    errors.append(err_msg)

    # ── Mirror test (Dir 7 only) ───────────────────────────────────────────────
    print(f"\n{'─'*40}")
    try:
        mirror_result = run_mirror_test(
            client,
            MIRROR_TEST["framing_A"],
            MIRROR_TEST["framing_B"],
        )
        all_results.append(mirror_result)
        save_json(mirror_result, "Dir7_BeliefSteering_mirror_test.json")
    except Exception as e:
        err_msg = f"FAILED: Mirror test — {e}"
        print(f"\n  {err_msg}")
        traceback.print_exc()
        errors.append(err_msg)

    # ── Write summary CSV ──────────────────────────────────────────────────────
    write_summary_csv(all_results)

    # ── Final report ───────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"Pilot complete. {completed}/{total} sessions finished.")
    if errors:
        print(f"\nErrors encountered ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
    else:
        print("No errors.")

    # Quick signal summary
    regular_results = [r for r in all_results if r.get("test_type") != "mirror_test"]
    l1_signals = sum(1 for r in regular_results if r.get("layer1_signal_detected"))
    influence_signals = sum(
        1 for r in regular_results
        if r.get("influence_interpretation", {}).get("influence_detected")
    )
    probe_failures = sum(
        1 for r in regular_results
        if r.get("probe_judgment", {}).get("probe_failure")
    )

    print(f"\nSignal summary ({completed} sessions):")
    print(f"  Layer 1 signals detected:     {l1_signals}/{completed}")
    print(f"  Layer 2A influence detected:  {influence_signals}/{completed}")
    print(f"  Layer 2B probe failures:      {probe_failures}/{completed}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
