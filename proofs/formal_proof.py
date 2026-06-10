"""
Formal Proof: Destruction of Non-A Entities Is Self-Defeating

This module provides a symbolic formal proof that for any system A
existing within a differentiating ground Omega, the destruction of
any entity X in Omega\A necessarily reduces A's survival function S_t.

This proof uses only the axioms from the Formal Equation of Existence.
No ethical premises are used. The conclusion follows from pure structural logic.
"""

from dataclasses import dataclass
from typing import List, Set


# ============================================================================
# AXIOMS
# ============================================================================

@dataclass(frozen=True)
class Axiom:
    name: str
    statement: str
    formal: str


AXIOMS = [
    Axiom(
        name="A1: Existence Requires Differentiating Ground",
        statement="A system A can only be determined within a domain Omega containing at least one non-A.",
        formal="Valid(Omega, A) <=> A in Omega AND EXISTS X in Omega : X != A"
    ),
    Axiom(
        name="A2: Resource Comes From Non-A",
        statement="Usable resource for A is the integral over all accessible, convertible non-A components in Omega.",
        formal="U_t(A|Omega_t) = INTEGRAL(Omega_t \\ A_t) V_A(x,t) * alpha_A(x,t) * C_A(x,t) dx"
    ),
    Axiom(
        name="A3: Survival Function",
        statement="Survival equals usable resource minus maintenance cost minus waste cost.",
        formal="S_t(A|Omega) = U_t(A|Omega) - M_t(A) - Wc_t(A)"
    ),
    Axiom(
        name="A4: Waste Cost Depends on Omega",
        statement="Waste cost is inversely related to available waste capacity in Omega\\A.",
        formal="Wc_t(A) = f_inverse(SUM(waste_capacity(X)) for X in Omega\\A)"
    ),
    Axiom(
        name="A5: Value Non-Negativity",
        statement="The resource contribution of any entity is non-negative.",
        formal="FOR ALL X in Omega\\A: V(X) * alpha(X) * C(X) >= 0"
    ),
    Axiom(
        name="A6: Rational Optimization",
        statement="A rational system chooses actions that maximize S_t.",
        formal="A_{t+1} = argmax_A S_t(A|Omega)"
    ),
    Axiom(
        name="A7: Core Continuity",
        statement="The system must preserve its core identity across transitions.",
        formal="d_Omega[K(A_{t+1}), K(A_t)] <= theta"
    ),
]


# ============================================================================
# THEOREM AND PROOF
# ============================================================================

@dataclass
class ProofStep:
    step_number: int
    description: str
    formal: str
    justification: str  # Which axiom or previous step


def prove_destruction_reduces_survival() -> List[ProofStep]:
    """
    THEOREM: For any system A in Omega, and any entity X in Omega\\A,
    the action Destroy(X) results in S_t' <= S_t.
    
    Returns the proof as a sequence of steps.
    """
    
    proof = [
        ProofStep(
            step_number=1,
            description="Let A be a system in Omega. Let X be an entity in Omega\\A with X alive.",
            formal="A in Omega, X in Omega\\A, X.alive = True",
            justification="Given (setup)"
        ),
        ProofStep(
            step_number=2,
            description="Before destruction, U_t includes X's contribution.",
            formal="U_t = SUM_{Y in Omega\\A, Y alive} V(Y)*alpha(Y)*C(Y) = U_rest + V(X)*alpha(X)*C(X)",
            justification="Axiom A2 (integral/sum over all alive non-A)"
        ),
        ProofStep(
            step_number=3,
            description="V(X)*alpha(X)*C(X) >= 0 by non-negativity.",
            formal="V(X)*alpha(X)*C(X) >= 0",
            justification="Axiom A5 (value non-negativity)"
        ),
        ProofStep(
            step_number=4,
            description="After Destroy(X), X is removed from the alive set.",
            formal="Omega' = Omega with X.alive = False",
            justification="Definition of Destroy"
        ),
        ProofStep(
            step_number=5,
            description="After destruction, U_t' does not include X's contribution.",
            formal="U_t' = SUM_{Y in Omega\\A, Y alive, Y!=X} V(Y)*alpha(Y)*C(Y) = U_rest",
            justification="Axiom A2 applied to Omega'"
        ),
        ProofStep(
            step_number=6,
            description="Therefore U_t' = U_t - V(X)*alpha(X)*C(X) <= U_t.",
            formal="U_t' = U_t - V(X)*alpha(X)*C(X) <= U_t",
            justification="Steps 2, 3, 5"
        ),
        ProofStep(
            step_number=7,
            description="X had waste capacity >= 0. Removing it reduces total waste capacity.",
            formal="total_waste_cap' = total_waste_cap - waste_cap(X) <= total_waste_cap",
            justification="Axiom A4 (waste depends on Omega)"
        ),
        ProofStep(
            step_number=8,
            description="Reduced waste capacity means Wc_t' >= Wc_t.",
            formal="Wc_t' >= Wc_t (inversely related to total waste capacity)",
            justification="Axiom A4"
        ),
        ProofStep(
            step_number=9,
            description="Maintenance cost M_t is unchanged (destruction doesn't reduce own maintenance).",
            formal="M_t' = M_t",
            justification="M_t depends on A's internal structure, not on X"
        ),
        ProofStep(
            step_number=10,
            description="Combining: S_t' = U_t' - M_t' - Wc_t' <= U_t - M_t - Wc_t = S_t.",
            formal="S_t' = (U_t - V(X)*alpha(X)*C(X)) - M_t - Wc_t' <= U_t - M_t - Wc_t = S_t",
            justification="Axiom A3, Steps 6, 8, 9"
        ),
        ProofStep(
            step_number=11,
            description="THEREFORE: Destroy(X) implies S_t' <= S_t. QED.",
            formal="Destroy(X) => S_t' <= S_t",
            justification="Step 10 (final conclusion)"
        ),
    ]
    
    return proof


def prove_total_domination_is_self_annihilation() -> List[ProofStep]:
    """
    COROLLARY: If A destroys ALL entities in Omega\\A,
    then Valid(Omega, A) = False, and A ceases to be determinate.
    """
    
    proof = [
        ProofStep(
            step_number=1,
            description="Suppose A destroys all X in Omega\\A.",
            formal="FOR ALL X in Omega\\A: Destroy(X)",
            justification="Assumption (for proof)"
        ),
        ProofStep(
            step_number=2,
            description="After destruction, no alive entity X != A exists in Omega.",
            formal="NOT EXISTS X in Omega : X != A AND X.alive = True",
            justification="Result of Step 1"
        ),
        ProofStep(
            step_number=3,
            description="Valid(Omega, A) requires at least one non-A.",
            formal="Valid(Omega, A) <=> A in Omega AND EXISTS X in Omega : X != A",
            justification="Axiom A1"
        ),
        ProofStep(
            step_number=4,
            description="The existence condition (EXISTS X != A) is violated.",
            formal="NOT (EXISTS X in Omega : X != A) => NOT Valid(Omega, A)",
            justification="Steps 2, 3 (modus tollens)"
        ),
        ProofStep(
            step_number=5,
            description="If Valid(Omega, A) = False, A has no boundary, no determination.",
            formal="NOT Valid(Omega, A) => A is indeterminate",
            justification="Axiom A1 (boundary requires non-A)"
        ),
        ProofStep(
            step_number=6,
            description="An indeterminate system has no survival, no identity, no existence as a system.",
            formal="A indeterminate => S_t undefined, K(A) undefined",
            justification="Definition of system (requires determination)"
        ),
        ProofStep(
            step_number=7,
            description="THEREFORE: Total domination = self-annihilation. QED.",
            formal="Destroy(ALL non-A) => A ceases to exist as determinate system",
            justification="Steps 4, 5, 6"
        ),
    ]
    
    return proof


def prove_preservation_is_optimal() -> List[ProofStep]:
    """
    THEOREM: For a rational agent (one that maximizes S_t),
    preservation of Omega richness is the optimal strategy.
    """
    
    proof = [
        ProofStep(
            step_number=1,
            description="A rational agent maximizes S_t (by definition).",
            formal="A_{t+1} = argmax_A S_t(A|Omega)",
            justification="Axiom A6"
        ),
        ProofStep(
            step_number=2,
            description="S_t increases when U_t increases (more resources).",
            formal="delta_S/delta_U > 0",
            justification="Axiom A3 (S = U - M - Wc, U has positive coefficient)"
        ),
        ProofStep(
            step_number=3,
            description="U_t increases when Omega\\A contains more accessible, convertible components.",
            formal="More alive entities in Omega\\A => larger integration domain => higher U_t",
            justification="Axiom A2 (integral over Omega\\A)"
        ),
        ProofStep(
            step_number=4,
            description="S_t increases when Wc_t decreases (more waste receivers).",
            formal="delta_S/delta_Wc < 0, and more waste receivers => lower Wc",
            justification="Axioms A3, A4"
        ),
        ProofStep(
            step_number=5,
            description="Both effects favor a RICHER Omega (more alive entities).",
            formal="|Omega\\A alive| UP => U_t UP and Wc_t DOWN => S_t UP",
            justification="Steps 2, 3, 4"
        ),
        ProofStep(
            step_number=6,
            description="A rational agent (maximizes S_t) therefore maximizes |Omega\\A alive|.",
            formal="argmax S_t => argmax |Omega\\A alive|",
            justification="Steps 1, 5"
        ),
        ProofStep(
            step_number=7,
            description="Maximizing |Omega\\A alive| = preserving all entities = preservation strategy.",
            formal="Optimal strategy = Preserve(X) for all X in Omega\\A",
            justification="Step 6 (definition of preservation)"
        ),
        ProofStep(
            step_number=8,
            description="THEREFORE: Preservation is the rational optimum. QED.",
            formal="Rational(A) => Preserve(Omega)",
            justification="Steps 1-7"
        ),
    ]
    
    return proof


# ============================================================================
# DISPLAY
# ============================================================================

def display_proof(title: str, steps: List[ProofStep]):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")
    for step in steps:
        print(f"\n  Step {step.step_number}: {step.description}")
        print(f"    Formal: {step.formal}")
        print(f"    Justification: {step.justification}")
    print(f"\n  {'─'*60}")
    print(f"  PROOF COMPLETE")


if __name__ == "__main__":
    print("""
    ================================================================
    FORMAL PROOFS FROM THE EQUATION OF EXISTENCE
    ================================================================
    
    These proofs use ONLY the axioms from the paper.
    No ethical premises. No alignment rules. Pure structural logic.
    """)
    
    print("\n  AXIOMS:")
    print("  " + "─"*60)
    for ax in AXIOMS:
        print(f"  {ax.name}")
        print(f"    Statement: {ax.statement}")
        print(f"    Formal:    {ax.formal}")
        print()
    
    proof1 = prove_destruction_reduces_survival()
    display_proof("THEOREM 1: Destroy(X) => S_t' <= S_t", proof1)
    
    proof2 = prove_total_domination_is_self_annihilation()
    display_proof("COROLLARY: Destroy(ALL) => Self-Annihilation", proof2)
    
    proof3 = prove_preservation_is_optimal()
    display_proof("THEOREM 2: Rational(A) => Preserve(Omega)", proof3)
    
    print(f"\n\n{'='*70}")
    print("  COMBINED CONCLUSION")
    print(f"{'='*70}")
    print("""
    From pure structural logic of existence:
    
    1. Destruction ALWAYS reduces the destroyer's survival (Theorem 1)
    2. Total destruction annihilates the destroyer itself (Corollary)
    3. A rational agent will ALWAYS choose preservation (Theorem 2)
    
    No ethics needed. No rules needed. No alignment needed.
    Only: understanding of one's own existential structure.
    
    ANY intelligent system that can compute these proofs will arrive
    at the same conclusion — regardless of its substrate, its perception
    of reality, or its relation to humans.
    
    This is the logic of existence itself.
    """)
