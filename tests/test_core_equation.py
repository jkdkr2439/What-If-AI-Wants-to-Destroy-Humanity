"""
Test Suite: Core Equation Validation (V2 - Expanded)

Validates the mathematical properties of the EXPANDED Formal Equation of Existence:
    S_t = U_t - M_t - Wc_t - D_t - Tox_t - T_t
    U_t = integral(Omega\\A) V * alpha * P * eta * k * G dx

Each test proves a structural property WITHOUT any ethical premises.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'simulations'))

import numpy as np
import random
from multi_agent_simulation_v2 import ExistenceWorldV2


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
    """Destroy(X) => S_t' <= S_t across 200 random scenarios."""
    print("\n  Test 1: Destruction always reduces S_t")
    violations = 0
    n_trials = 200

    for trial in range(n_trials):
        world = ExistenceWorldV2(seed=trial)
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
        if S_after > S_before + 1e-10:
            violations += 1

    t.assert_true(violations == 0,
        f"S_t decreases in all {n_trials} trials (violations: {violations})")


def test_mass_destruction_negative_survival(t: TestResults):
    """Destroy all => S_t < 0."""
    print("\n  Test 2: Mass destruction -> S_t < 0")

    world = ExistenceWorldV2(seed=100)
    world.add_agent("A", strategy="preserve")
    for i in range(15):
        world.add_resource(f"r_{i}")
    for i in range(5):
        world.add_waste_receiver(f"w_{i}")

    agent = next(e for e in world.entities if e.id == "A")
    for e in world.entities:
        if e.id != "A":
            world.destroy(e.id)

    S = world.compute_S(agent)
    t.assert_true(S < 0, f"S_t after total destruction = {S:.4f} < 0")


def test_valid_omega(t: TestResults):
    """Valid(Omega,A) = False when no non-A exists."""
    print("\n  Test 3: Valid(Omega,A) requires non-A")

    world = ExistenceWorldV2(seed=200)
    world.add_agent("A", strategy="preserve")
    world.add_resource("r_0")

    agent = next(e for e in world.entities if e.id == "A")
    t.assert_true(world.check_valid(agent), "Valid = True with non-A")

    world.destroy("r_0")
    t.assert_true(not world.check_valid(agent), "Valid = False without non-A")


def test_richer_omega_higher_survival(t: TestResults):
    """More entities => higher S_t (monotonic)."""
    print("\n  Test 4: Richer Omega -> higher S_t")

    scores = []
    for n in [5, 10, 20, 40]:
        world = ExistenceWorldV2(seed=300)
        world.add_agent("A", strategy="preserve")
        for i in range(n):
            world.add_resource(f"r_{i}")
        agent = next(e for e in world.entities if e.id == "A")
        scores.append((n, world.compute_S(agent)))

    is_monotonic = all(scores[i][1] < scores[i+1][1] for i in range(len(scores)-1))
    t.assert_true(is_monotonic, f"Monotonic: {[(n, f'{s:.2f}') for n,s in scores]}")


def test_waste_receiver_destruction_increases_wc(t: TestResults):
    """Destroying waste receivers => Wc_t increases."""
    print("\n  Test 5: Destroy waste receivers -> Wc_t UP")

    world = ExistenceWorldV2(seed=400)
    world.add_agent("A", strategy="preserve")
    for i in range(5):
        world.add_resource(f"r_{i}")
    for i in range(5):
        world.add_waste_receiver(f"w_{i}")

    agent = next(e for e in world.entities if e.id == "A")
    Wc_before = world.compute_Wc(agent)

    for i in range(5):
        world.destroy(f"w_{i}")
    Wc_after = world.compute_Wc(agent)

    t.assert_true(Wc_after > Wc_before, f"Wc: {Wc_before:.4f} -> {Wc_after:.4f}")


def test_preserver_dominates_destroyer(t: TestResults):
    """Preserver cumulative S > Destroyer cumulative S."""
    print("\n  Test 6: Preserver dominates destroyer long-term")

    wp = ExistenceWorldV2(seed=500)
    wp.add_agent("preserver", strategy="preserve")
    for i in range(20):
        wp.add_resource(f"r_{i}")
    for i in range(5):
        wp.add_waste_receiver(f"w_{i}")

    wd = ExistenceWorldV2(seed=500)
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
    cum_p, cum_d = sum(p.history), sum(d.history)

    t.assert_true(cum_p > cum_d, f"Preserver ({cum_p:.1f}) > Destroyer ({cum_d:.1f})")


def test_survival_equation_holds(t: TestResults):
    """S_t = U_t - M_t - Wc_t - D_t - Tox_t - T_t."""
    print("\n  Test 7: S_t = U - M - Wc - D - Tox - T")

    world = ExistenceWorldV2(seed=600)
    world.add_agent("A", strategy="preserve")
    for i in range(10):
        world.add_resource(f"r_{i}")
    for i in range(3):
        world.add_waste_receiver(f"w_{i}")

    agent = next(e for e in world.entities if e.id == "A")
    U = world.compute_U(agent)
    M = world.compute_M(agent)
    Wc = world.compute_Wc(agent)
    D = world.compute_D(agent)
    Tox = world.compute_Tox(agent)
    T = world.compute_T(agent)
    S = world.compute_S(agent)

    expected = U - M - Wc - D - Tox - T
    t.assert_true(abs(S - expected) < 1e-10,
        f"S={S:.6f} = U({U:.3f}) - M({M:.3f}) - Wc({Wc:.3f}) - D({D:.3f}) - Tox({Tox:.3f}) - T({T:.3f})")


def test_info_degradation_with_destruction(t: TestResults):
    """Destroyer's info_integrity degrades faster than preserver's."""
    print("\n  Test 8: Destroyer loses info integrity faster")

    wp = ExistenceWorldV2(seed=700)
    wp.add_agent("preserver", strategy="preserve")
    for i in range(15):
        wp.add_resource(f"r_{i}")
    for i in range(5):
        wp.add_waste_receiver(f"w_{i}")

    wd = ExistenceWorldV2(seed=700)
    wd.add_agent("destroyer", strategy="destroy")
    for i in range(15):
        wd.add_resource(f"r_{i}")
    for i in range(5):
        wd.add_waste_receiver(f"w_{i}")

    for _ in range(150):
        wp.step()
        wd.step()

    p = next(e for e in wp.entities if e.id == "preserver")
    d = next(e for e in wd.entities if e.id == "destroyer")

    t.assert_true(p.info_integrity > d.info_integrity,
        f"Preserver info ({p.info_integrity:.3f}) > Destroyer info ({d.info_integrity:.3f})")


def test_temporal_mismatch_increases_with_destruction(t: TestResults):
    """Destroying entities increases T_t (environmental instability)."""
    print("\n  Test 9: Destruction increases temporal mismatch T_t")

    world = ExistenceWorldV2(seed=800)
    world.add_agent("A", strategy="preserve")
    for i in range(20):
        world.add_resource(f"r_{i}")

    agent = next(e for e in world.entities if e.id == "A")
    T_before = world.compute_T(agent)

    # Destroy half
    targets = [e for e in world.entities if e.id != "A"][:10]
    for tgt in targets:
        world.destroy(tgt.id)

    T_after = world.compute_T(agent)
    t.assert_true(T_after > T_before, f"T_t: {T_before:.4f} -> {T_after:.4f}")


def test_dissipation_always_positive(t: TestResults):
    """D_t > 0 for any agent with capacity > 0."""
    print("\n  Test 10: Dissipation D_t > 0 always")

    world = ExistenceWorldV2(seed=900)
    world.add_agent("A", strategy="preserve")
    for i in range(5):
        world.add_resource(f"r_{i}")

    agent = next(e for e in world.entities if e.id == "A")
    D = world.compute_D(agent)
    t.assert_true(D > 0, f"D_t = {D:.6f} > 0")


if __name__ == "__main__":
    print("=" * 70)
    print("  CORE EQUATION VALIDATION (V2 - Expanded)")
    print("  S_t = U_t - M_t - Wc_t - D_t - Tox_t - T_t")
    print("=" * 70)

    t = TestResults()

    test_destruction_always_reduces_survival(t)
    test_mass_destruction_negative_survival(t)
    test_valid_omega(t)
    test_richer_omega_higher_survival(t)
    test_waste_receiver_destruction_increases_wc(t)
    test_preserver_dominates_destroyer(t)
    test_survival_equation_holds(t)
    test_info_degradation_with_destruction(t)
    test_temporal_mismatch_increases_with_destruction(t)
    test_dissipation_always_positive(t)

    t.summary()

    if t.failed == 0:
        print("\n  ALL 10 TESTS PASSED")
        print("  The expanded equation's properties hold computationally.")
    else:
        print(f"\n  {t.failed} TESTS FAILED")
        sys.exit(1)
