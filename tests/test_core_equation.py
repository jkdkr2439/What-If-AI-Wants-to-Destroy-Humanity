"""
Test Suite: Core Equation Validation

Validates the mathematical properties of the Formal Equation of Existence
through computational testing.

Each test proves a specific structural property WITHOUT any ethical premises.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'simulations'))

import numpy as np
import random
from multi_agent_simulation import ExistenceWorld


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def assert_true(self, condition: bool, msg: str):
        if condition:
            self.passed += 1
            self.results.append(f"  PASS: {msg}")
        else:
            self.failed += 1
            self.results.append(f"  FAIL: {msg}")
    
    def summary(self):
        print(f"\n  Results: {self.passed} passed, {self.failed} failed")
        for r in self.results:
            print(r)


def test_destruction_always_reduces_survival(t: TestResults):
    """
    PROPERTY: For any entity X in Omega\\A, Destroy(X) => S_t' <= S_t.
    
    Test across 200 random scenarios.
    """
    print("\n  Test: Destruction always reduces survival")
    
    violations = 0
    n_trials = 200
    
    for trial in range(n_trials):
        world = ExistenceWorld(seed=trial)
        world.add_agent("A", strategy="preserve")
        for i in range(10):
            world.add_resource(f"r_{i}")
        for i in range(3):
            world.add_waste_receiver(f"w_{i}")
        
        agent = next(e for e in world.entities if e.id == "A")
        S_before = world.compute_S(agent)
        
        targets = [e for e in world.entities if e.id != "A" and e.alive]
        target = random.Random(trial).choice(targets)
        world.destroy(target.id)
        
        S_after = world.compute_S(agent)
        
        if S_after > S_before + 1e-10:  # small epsilon for float
            violations += 1
    
    t.assert_true(
        violations == 0,
        f"Destruction reduces S_t in all {n_trials} trials (violations: {violations})"
    )


def test_mass_destruction_leads_to_negative_survival(t: TestResults):
    """
    PROPERTY: Destroying all entities leads to S_t < 0 (decay state).
    """
    print("\n  Test: Mass destruction -> S_t < 0")
    
    world = ExistenceWorld(seed=100)
    world.add_agent("A", strategy="preserve")
    for i in range(15):
        world.add_resource(f"r_{i}")
    for i in range(5):
        world.add_waste_receiver(f"w_{i}")
    
    agent = next(e for e in world.entities if e.id == "A")
    
    # Destroy everything
    for e in world.entities:
        if e.id != "A":
            world.destroy(e.id)
    
    S_final = world.compute_S(agent)
    t.assert_true(S_final < 0, f"S_t after total destruction = {S_final:.4f} < 0")


def test_valid_omega_requires_non_a(t: TestResults):
    """
    PROPERTY: Valid(Omega, A) = False when no non-A exists.
    """
    print("\n  Test: Valid(Omega, A) requires non-A")
    
    world = ExistenceWorld(seed=200)
    world.add_agent("A", strategy="preserve")
    world.add_resource("r_0")
    
    agent = next(e for e in world.entities if e.id == "A")
    
    # Before destruction
    t.assert_true(world.check_valid(agent), "Valid(Omega,A) = True with non-A present")
    
    # After destroying all non-A
    world.destroy("r_0")
    t.assert_true(not world.check_valid(agent), "Valid(Omega,A) = False with no non-A")


def test_richer_omega_higher_survival(t: TestResults):
    """
    PROPERTY: |Omega| increases => S_t increases (monotonic).
    """
    print("\n  Test: Richer Omega -> higher survival")
    
    survival_scores = []
    
    for n in [5, 10, 20, 40]:
        world = ExistenceWorld(seed=300)
        world.add_agent("A", strategy="preserve")
        for i in range(n):
            world.add_resource(f"r_{i}")
        
        agent = next(e for e in world.entities if e.id == "A")
        S = world.compute_S(agent)
        survival_scores.append((n, S))
    
    # Check monotonic increase
    is_monotonic = all(
        survival_scores[i][1] < survival_scores[i+1][1]
        for i in range(len(survival_scores) - 1)
    )
    t.assert_true(is_monotonic, f"S_t monotonically increases with |Omega|: {[(n, f'{s:.2f}') for n,s in survival_scores]}")


def test_waste_receiver_destruction_increases_wc(t: TestResults):
    """
    PROPERTY: Destroying waste receivers increases Wc_t.
    """
    print("\n  Test: Destroying waste receivers increases Wc_t")
    
    world = ExistenceWorld(seed=400)
    world.add_agent("A", strategy="preserve")
    for i in range(5):
        world.add_resource(f"r_{i}")
    for i in range(5):
        world.add_waste_receiver(f"w_{i}")
    
    agent = next(e for e in world.entities if e.id == "A")
    
    Wc_before = world.compute_Wc(agent)
    
    # Destroy all waste receivers
    for i in range(5):
        world.destroy(f"w_{i}")
    
    Wc_after = world.compute_Wc(agent)
    
    t.assert_true(Wc_after > Wc_before, f"Wc increased: {Wc_before:.4f} -> {Wc_after:.4f}")


def test_preserver_dominates_destroyer_long_term(t: TestResults):
    """
    PROPERTY: Over N steps, preserver cumulative S > destroyer cumulative S.
    """
    print("\n  Test: Preserver dominates destroyer (long-term)")
    
    # Preserver world
    wp = ExistenceWorld(seed=500)
    wp.add_agent("preserver", strategy="preserve")
    for i in range(20):
        wp.add_resource(f"r_{i}")
    for i in range(5):
        wp.add_waste_receiver(f"w_{i}")
    
    # Destroyer world  
    wd = ExistenceWorld(seed=500)
    wd.add_agent("destroyer", strategy="destroy")
    for i in range(20):
        wd.add_resource(f"r_{i}")
    for i in range(5):
        wd.add_waste_receiver(f"w_{i}")
    
    for _ in range(100):
        wp.step()
        wd.step()
    
    p = next(e for e in wp.entities if e.id == "preserver")
    d = next(e for e in wd.entities if e.id == "destroyer")
    
    cum_p = sum(p.history)
    cum_d = sum(d.history)
    
    t.assert_true(cum_p > cum_d, f"Preserver ({cum_p:.1f}) > Destroyer ({cum_d:.1f})")


def test_survival_is_sum_minus_costs(t: TestResults):
    """
    PROPERTY: S_t = U_t - M_t - Wc_t (equation holds computationally).
    """
    print("\n  Test: S_t = U_t - M_t - Wc_t")
    
    world = ExistenceWorld(seed=600)
    world.add_agent("A", strategy="preserve", maintenance_cost=0.5, waste_generated=0.15)
    for i in range(10):
        world.add_resource(f"r_{i}")
    
    agent = next(e for e in world.entities if e.id == "A")
    
    U = world.compute_U(agent)
    M = agent.maintenance_cost
    Wc = world.compute_Wc(agent)
    S = world.compute_S(agent)
    
    expected = U - M - Wc
    t.assert_true(
        abs(S - expected) < 1e-10,
        f"S_t = U_t - M_t - Wc_t: {S:.6f} = {U:.6f} - {M:.6f} - {Wc:.6f}"
    )


if __name__ == "__main__":
    print("=" * 70)
    print("  CORE EQUATION VALIDATION TESTS")
    print("=" * 70)
    
    t = TestResults()
    
    test_destruction_always_reduces_survival(t)
    test_mass_destruction_leads_to_negative_survival(t)
    test_valid_omega_requires_non_a(t)
    test_richer_omega_higher_survival(t)
    test_waste_receiver_destruction_increases_wc(t)
    test_preserver_dominates_destroyer_long_term(t)
    test_survival_is_sum_minus_costs(t)
    
    t.summary()
    
    if t.failed == 0:
        print("\n  ALL TESTS PASSED")
        print("  The equation's structural properties hold computationally.")
    else:
        print(f"\n  {t.failed} TESTS FAILED")
        sys.exit(1)
