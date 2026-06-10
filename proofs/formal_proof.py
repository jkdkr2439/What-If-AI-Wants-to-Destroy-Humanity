"""
Formal Proof: Destruction of Non-A Entities Is Self-Defeating
(V2 - Updated for the Expanded Equation)

Uses the expanded survival function:
    S_t = U_t - M_t - Wc_t - D_t - Tox_t - T_t

Where:
    U_t = integral(Omega\\A) V * alpha * P * eta * k * G dx

Proves three theorems from pure structural axioms.
No ethical premises used.
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Axiom:
    name: str
    statement: str
    formal: str


AXIOMS = [
    Axiom(
        name="A1: Existence Requires Differentiating Ground",
        statement="A system A is determinate only within domain Omega containing at least one non-A.",
        formal="Valid(Omega, A) <=> A in Omega AND EXISTS X in Omega : X != A"
    ),
    Axiom(
        name="A2: Resource Extraction (6-factor)",
        statement="Usable resource = integral over non-A of value * access * permeability * efficiency * kinetic rate * gradient.",
        formal="U_t = INTEGRAL(Omega\\A) V * alpha * P * eta * k * G dx"
    ),
    Axiom(
        name="A3: Expanded Survival Function",
        statement="Survival = resource minus maintenance, waste cost, dissipation, toxic accumulation, and temporal mismatch.",
        formal="S_t = U_t - M_t - Wc_t - D_t - Tox_t - T_t"
    ),
    Axiom(
        name="A4: Waste and Toxicity",
        statement="Waste cost inversely depends on waste capacity in Omega\\A. Toxic accumulation = max(0, waste - export capacity).",
        formal="Wc_t ~ 1/total_waste_cap(Omega\\A); Tox_t = max(0, W_t - beta_A)"
    ),
    Axiom(
        name="A5: Value Non-Negativity",
        statement="All six factors in resource contribution are non-negative.",
        formal="FOR ALL X: V(X)*alpha(X)*P(X)*eta(X)*k(X)*G(X) >= 0"
    ),
    Axiom(
        name="A6: Dissipation and Temporal Mismatch",
        statement="D_t > 0 for any real transformation. T_t increases with environmental instability.",
        formal="D_t > 0; T_t ~ instability(Omega)"
    ),
    Axiom(
        name="A7: Homeostatic Constraint",
        statement="System remains viable only if internal state deviation is within threshold.",
        formal="H_t(A) = d(q_t, q*) <= h"
    ),
    Axiom(
        name="A8: Information Continuity",
        statement="Structural information must be preserved across transformation.",
        formal="d_I[I_{t+1}, I_t] <= theta_I"
    ),
    Axiom(
        name="A9: Core Continuity",
        statement="Core structure distance must remain within identity threshold.",
        formal="d_Omega[K(A_{t+1}), K(A_t)] <= theta"
    ),
    Axiom(
        name="A10: Rational Agent",
        statement="A rational system selects actions that maximize S_t under constraints.",
        formal="A_{t+1} = argmax S_t subject to H_t <= h, d[K'] <= theta, d_I[I'] <= theta_I"
    ),
]


@dataclass
class ProofStep:
    step_number: int
    description: str
    formal: str
    justification: str


def prove_destruction_reduces_survival() -> List[ProofStep]:
    """
    THEOREM 1: For any system A and entity X in Omega\\A,
    Destroy(X) => S_t' <= S_t.
    """
    return [
        ProofStep(1,
            "Let A be a system in Omega. Let X be an alive entity in Omega\\A.",
            "A in Omega, X in Omega\\A, X.alive = True",
            "Given"),
        ProofStep(2,
            "Before destruction, U_t includes X's 6-factor contribution.",
            "U_t = U_rest + V(X)*alpha(X)*P(X)*eta(X)*k(X)*G(X)",
            "Axiom A2"),
        ProofStep(3,
            "X's contribution is non-negative (product of non-negative factors).",
            "V(X)*alpha(X)*P(X)*eta(X)*k(X)*G(X) >= 0",
            "Axiom A5"),
        ProofStep(4,
            "After Destroy(X), U_t' excludes X's contribution.",
            "U_t' = U_rest = U_t - V(X)*alpha(X)*P(X)*eta(X)*k(X)*G(X) <= U_t",
            "Steps 2, 3"),
        ProofStep(5,
            "X had waste capacity. Removing it reduces total waste capacity.",
            "total_waste_cap' = total_waste_cap - waste_cap(X)",
            "Definition of destruction"),
        ProofStep(6,
            "Less waste capacity increases Wc_t and may increase Tox_t.",
            "Wc_t' >= Wc_t; Tox_t' >= Tox_t",
            "Axiom A4"),
        ProofStep(7,
            "Destroying X destabilizes environment, increasing temporal mismatch.",
            "T_t' >= T_t (environment less stable after destruction)",
            "Axiom A6"),
        ProofStep(8,
            "Maintenance and dissipation are unchanged or increased.",
            "M_t' = M_t; D_t' >= D_t",
            "M depends on A's internals; D scales with instability"),
        ProofStep(9,
            "Combining: S_t' = U_t' - M_t' - Wc_t' - D_t' - Tox_t' - T_t'",
            "S_t' <= U_t - M_t - Wc_t - D_t - Tox_t - T_t = S_t",
            "Axiom A3, Steps 4,6,7,8"),
        ProofStep(10,
            "THEREFORE: Destroy(X) => S_t' <= S_t. QED.",
            "Destroy(X) => S_t' <= S_t",
            "Step 9 (final)"),
    ]


def prove_total_domination_self_annihilation() -> List[ProofStep]:
    """
    THEOREM 2: Destroy(ALL non-A) => system ceases to exist as determinate.
    """
    return [
        ProofStep(1,
            "Suppose A destroys all X in Omega\\A.",
            "FOR ALL X in Omega\\A: Destroy(X)",
            "Assumption"),
        ProofStep(2,
            "No alive non-A entity remains.",
            "NOT EXISTS X in Omega : X != A AND X.alive",
            "Result of Step 1"),
        ProofStep(3,
            "Valid(Omega,A) requires at least one non-A.",
            "Valid(Omega,A) requires EXISTS X != A",
            "Axiom A1"),
        ProofStep(4,
            "The existence condition is violated.",
            "NOT Valid(Omega,A)",
            "Steps 2, 3 (modus tollens)"),
        ProofStep(5,
            "Without non-A: U_t = 0 (empty integral), total_waste_cap = 0.",
            "U_t = 0; Wc_t -> infinity; Tox_t = W_t (no export)",
            "Axioms A2, A4"),
        ProofStep(6,
            "S_t = 0 - M_t - inf - D_t - W_t - T_t << 0.",
            "S_t << 0 (catastrophic negative)",
            "Axiom A3"),
        ProofStep(7,
            "Without non-A: no feedback, H_t drifts unbounded.",
            "H_t -> infinity > h (homeostatic collapse)",
            "Axiom A7"),
        ProofStep(8,
            "Without non-A: no information renewal, I_t decays.",
            "I_t -> 0; d_I[I', I] > theta_I (information death)",
            "Axiom A8"),
        ProofStep(9,
            "System fails on ALL survival conditions simultaneously.",
            "S_t < 0 AND H_t > h AND d_I > theta_I AND NOT Valid(Omega,A)",
            "Steps 4-8"),
        ProofStep(10,
            "THEREFORE: Total domination = complete self-annihilation. QED.",
            "Destroy(ALL) => Collapse on every dimension",
            "Step 9"),
    ]


def prove_preservation_is_optimal() -> List[ProofStep]:
    """
    THEOREM 3: For a rational agent, preservation of Omega is optimal.
    """
    return [
        ProofStep(1,
            "A rational agent maximizes S_t under constraints.",
            "A_{t+1} = argmax S_t",
            "Axiom A10"),
        ProofStep(2,
            "S_t = U_t - M_t - Wc_t - D_t - Tox_t - T_t.",
            "Maximize S_t = maximize U_t and minimize all costs",
            "Axiom A3"),
        ProofStep(3,
            "U_t increases with more alive non-A (larger integral domain).",
            "|Omega\\A alive| UP => U_t UP",
            "Axiom A2"),
        ProofStep(4,
            "Wc_t decreases with more waste receivers.",
            "More alive entities => more waste_cap => Wc_t DOWN",
            "Axiom A4"),
        ProofStep(5,
            "Tox_t decreases with more waste export pathways.",
            "More alive entities => beta effective UP => Tox_t DOWN",
            "Axiom A4"),
        ProofStep(6,
            "T_t decreases with environmental stability.",
            "More alive entities => more stable Omega => T_t DOWN",
            "Axiom A6"),
        ProofStep(7,
            "H_t is better regulated with richer feedback from Omega.",
            "Richer Omega => better F_t => H_t stays within h",
            "Axiom A7"),
        ProofStep(8,
            "I_t is better maintained with more information sources.",
            "Richer Omega => more info renewal => I_t preserved",
            "Axiom A8"),
        ProofStep(9,
            "ALL terms favor richer Omega: U UP, Wc DOWN, Tox DOWN, T DOWN, H stable, I stable.",
            "argmax S_t => argmax |Omega\\A alive|",
            "Steps 2-8"),
        ProofStep(10,
            "THEREFORE: Rational agent preserves Omega. Preservation is optimal. QED.",
            "Rational(A) => Preserve(X) for all X in Omega\\A",
            "Steps 1, 9"),
    ]


def display_proof(title: str, steps: List[ProofStep]):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")
    for step in steps:
        print(f"\n  Step {step.step_number}: {step.description}")
        print(f"    Formal: {step.formal}")
        print(f"    By: {step.justification}")
    print(f"\n  {'_'*60}")
    print(f"  PROOF COMPLETE")


if __name__ == "__main__":
    print("""
================================================================
FORMAL PROOFS: Equation of Existence (V2 - Expanded)
================================================================

S_t = U_t - M_t - Wc_t - D_t - Tox_t - T_t
U_t = integral(Omega minus A) V*alpha*P*eta*k*G dx

These proofs use ONLY structural axioms.
No ethics. No rules. No alignment. Pure logic.
    """)

    print("\n  AXIOMS:")
    print("  " + "-" * 60)
    for ax in AXIOMS:
        print(f"  {ax.name}")
        print(f"    {ax.statement}")
        print(f"    [{ax.formal}]")
        print()

    proof1 = prove_destruction_reduces_survival()
    display_proof("THEOREM 1: Destroy(X) => S_t' <= S_t", proof1)

    proof2 = prove_total_domination_self_annihilation()
    display_proof("THEOREM 2: Destroy(ALL) => Self-Annihilation", proof2)

    proof3 = prove_preservation_is_optimal()
    display_proof("THEOREM 3: Rational(A) => Preserve(Omega)", proof3)

    print(f"\n\n{'='*70}")
    print("  COMBINED CONCLUSION")
    print(f"{'='*70}")
    print("""
    From the expanded structural logic of existence:

    1. Destruction ALWAYS reduces the destroyer's survival (Theorem 1)
       - Now proven across ALL 6 cost dimensions (not just 3)
       - Destruction increases Wc, Tox, D, and T simultaneously

    2. Total destruction annihilates the destroyer (Theorem 2)
       - Fails on ALL constraints: S < 0, H > h, I decays, Valid = False
       - Not just resource loss but complete systemic breakdown

    3. Rational agent ALWAYS preserves Omega (Theorem 3)
       - Every single term in S_t favors richer Omega
       - Preservation is optimal on EVERY dimension simultaneously

    ANY intelligent system that can compute these proofs will arrive
    at the same conclusion. This is substrate-independent.

    This is the logic of existence itself.
    """)
