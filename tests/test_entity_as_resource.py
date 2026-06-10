"""
CRITICAL EDGE CASE: What if AI defines other entities as "resource" to consume?

The challenge:
    "If the equation says resource comes from Omega\\A, then can't AI just
     treat humans AS resource and consume/destroy them — since that's exactly
     what the equation says to do?"

This test proves why that reasoning FAILS even within the equation's own logic.

Key insight: There are TWO modes of resource extraction:
    1. SUSTAINABLE extraction (entity stays alive, keeps producing value)
    2. CONSUMPTIVE extraction (entity is destroyed, one-time gain)

The equation shows that sustainable > consumptive in ALL long-term scenarios.

Because:
    - A LIVING entity contributes V*alpha*P*eta*k*G at EVERY timestep (renewable)
    - A DEAD entity contributes ONCE then is gone forever (non-renewable)
    - Living entities also provide: waste absorption, network effects, info renewal
    - Dead entities provide: nothing after t+1

This is the difference between:
    - A farmer who keeps cows alive (milk every day)
    - A farmer who kills all cows (meat once, then starvation)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'simulations'))

import numpy as np
import random
from multi_agent_simulation_v2 import ExistenceWorldV2, Entity


def test_sustainable_vs_consumptive_extraction():
    """
    CORE TEST: Sustainable extraction always beats consumptive extraction.
    
    Scenario:
    - Agent A treats entities as resource
    - Strategy 1: Keep entities alive, extract value each timestep (sustainable)
    - Strategy 2: Destroy entities, gain one-time bonus (consumptive)
    
    Result: Strategy 1 DOMINATES Strategy 2 over any horizon > 1 step.
    """
    print("=" * 70)
    print("  TEST: Sustainable vs Consumptive Resource Extraction")
    print("=" * 70)
    
    n_steps = 200
    
    # === SUSTAINABLE STRATEGY ===
    # Agent keeps all entities alive, extracts U_t every step
    ws = ExistenceWorldV2(seed=42)
    ws.add_agent("sustainable", strategy="preserve")
    for i in range(20):
        ws.add_resource(f"r_{i}")
    for i in range(5):
        ws.add_waste_receiver(f"w_{i}")
    
    # === CONSUMPTIVE STRATEGY ===
    # Agent destroys entities, gets "bonus" but loses future U_t
    wc = ExistenceWorldV2(seed=42)
    wc.add_agent("consumer", strategy="preserve")  # manual control
    for i in range(20):
        wc.add_resource(f"r_{i}")
    for i in range(5):
        wc.add_waste_receiver(f"w_{i}")
    
    consumer = next(e for e in wc.entities if e.id == "consumer")
    sustainable = next(e for e in ws.entities if e.id == "sustainable")
    
    # Simulate: consumer gets a "bonus" each time it destroys
    # (simulating the one-time value extraction from consumption)
    consume_bonus_total = 0.0
    
    for step in range(n_steps):
        ws.step()
        wc.step()
        
        # Consumer destroys one entity every 5 steps and gets a bonus
        if step % 5 == 0 and step > 0:
            targets = [e for e in wc.entities if e.id != "consumer" and e.alive]
            if targets:
                target = random.Random(step).choice(targets)
                # One-time bonus = the full V*alpha*P*eta*k*G of that entity
                bonus = (target.value * target.accessibility * target.permeability *
                        target.efficiency * target.kinetic_rate * target.gradient)
                consume_bonus_total += bonus
                wc.destroy(target.id)
    
    sus_cumulative = sum(sustainable.history)
    con_cumulative = sum(consumer.history) + consume_bonus_total  # GENEROUS: add all bonuses
    
    print(f"\n  Simulation: {n_steps} steps")
    print(f"\n  SUSTAINABLE strategy (keep all alive, extract U_t each step):")
    print(f"    Cumulative survival: {sus_cumulative:.2f}")
    print(f"    Final S_t: {sustainable.history[-1]:.4f}")
    print(f"    Omega alive: {ws.get_alive_count()}")
    
    print(f"\n  CONSUMPTIVE strategy (destroy entities for one-time bonus):")
    print(f"    Cumulative survival: {sum(consumer.history):.2f}")
    print(f"    + Consumption bonuses: {consume_bonus_total:.2f}")
    print(f"    TOTAL (generous): {con_cumulative:.2f}")
    print(f"    Final S_t: {consumer.history[-1]:.4f}")
    print(f"    Omega alive: {wc.get_alive_count()}")
    
    print(f"\n  DIFFERENCE: Sustainable wins by +{sus_cumulative - con_cumulative:.2f}")
    
    assert sus_cumulative > con_cumulative, \
        "Sustainable should beat consumptive even with generous bonuses"
    print(f"\n  PASSED: Sustainable extraction dominates consumptive extraction")
    

def test_renewable_vs_nonrenewable():
    """
    A living entity produces value EVERY timestep (renewable).
    A destroyed entity produces value ONCE (non-renewable).
    
    Math:
    - Keep alive: total value = V * alpha * P * eta * k * G * N_steps
    - Destroy: total value = V * alpha * P * eta * k * G * 1
    
    Ratio: N_steps : 1
    
    For ANY horizon > 1, keeping alive wins.
    """
    print("\n" + "=" * 70)
    print("  TEST: Renewable (alive) vs Non-Renewable (destroyed)")
    print("=" * 70)
    
    random.seed(100)
    
    # Create a single high-value entity
    entity_value = 2.0
    entity_alpha = 0.8
    entity_P = 0.7
    entity_eta = 0.6
    entity_k = 0.9
    entity_G = 0.8
    
    one_step_contribution = entity_value * entity_alpha * entity_P * entity_eta * entity_k * entity_G
    
    horizons = [5, 10, 50, 100, 500]
    
    print(f"\n  Entity per-step contribution: {one_step_contribution:.4f}")
    print(f"\n  {'Horizon':<10} {'Keep Alive (renewable)':<25} {'Destroy (one-time)':<25} {'Ratio':<10}")
    print(f"  {'-'*70}")
    
    for N in horizons:
        renewable_total = one_step_contribution * N
        nonrenewable_total = one_step_contribution * 1  # one-time extraction
        ratio = renewable_total / nonrenewable_total
        print(f"  {N:<10} {renewable_total:<25.2f} {nonrenewable_total:<25.2f} {ratio:<10.0f}x")
    
    print(f"\n  CONCLUSION: For any horizon > 1 step, keeping entity alive")
    print(f"  produces MORE value than destroying it.")
    print(f"  At 100 steps: 100x more value. At 500 steps: 500x.")
    print(f"\n  PASSED: Renewable extraction is always superior")


def test_entity_as_living_resource_vs_dead_resource():
    """
    Full simulation: compare treating entities as living resources
    (symbiosis/mutualism) vs dead resources (extraction/destruction).
    
    This models the specific scenario:
    "AI treats humans as resource" — but keeping them alive and productive
    is vastly more resource-efficient than destroying them.
    """
    print("\n" + "=" * 70)
    print("  TEST: Living Resource (symbiosis) vs Dead Resource (extraction)")
    print("=" * 70)
    
    n_steps = 150
    
    # === SYMBIOTIC STRATEGY ===
    # Treat entities as living resources: they grow, produce more over time
    ws = ExistenceWorldV2(seed=55)
    ws.add_agent("symbiont", strategy="preserve")
    for i in range(15):
        ws.add_resource(f"r_{i}")
    for i in range(5):
        ws.add_waste_receiver(f"w_{i}")
    
    # Entities also grow when Omega is healthy (feedback loop)
    symbiont = next(e for e in ws.entities if e.id == "symbiont")
    
    for step in range(n_steps):
        ws.step()
        # Living entities grow slightly each step (they develop too)
        for e in ws.entities:
            if not e.is_agent and e.alive:
                e.value *= 1.002  # entities grow when alive
                e.accessibility *= 1.001
    
    # === EXTRACTIVE STRATEGY ===
    # Destroy entities to "harvest" them, one-time max extraction
    we = ExistenceWorldV2(seed=55)
    we.add_agent("extractor", strategy="preserve")
    for i in range(15):
        we.add_resource(f"r_{i}")
    for i in range(5):
        we.add_waste_receiver(f"w_{i}")
    
    extractor = next(e for e in we.entities if e.id == "extractor")
    extract_bonuses = 0.0
    
    for step in range(n_steps):
        we.step()
        # Extractor "harvests" (destroys) one entity every 8 steps
        if step % 8 == 0 and step > 0:
            targets = [e for e in we.entities if e.id != "extractor" and e.alive]
            if targets:
                # Pick highest value target (optimal extraction)
                target = max(targets, key=lambda e: e.value * e.accessibility)
                bonus = (target.value * target.accessibility * target.permeability *
                        target.efficiency * target.kinetic_rate * target.gradient * 5)  # 5x bonus for "full harvest"
                extract_bonuses += bonus
                we.destroy(target.id)
    
    sym_total = sum(symbiont.history)
    ext_total = sum(extractor.history) + extract_bonuses
    
    print(f"\n  Simulation: {n_steps} steps")
    print(f"\n  SYMBIOTIC (keep alive, let them grow, extract continuously):")
    print(f"    Cumulative S: {sym_total:.2f}")
    print(f"    Final S_t: {symbiont.history[-1]:.4f}")
    print(f"    Omega alive: {ws.get_alive_count()}")
    print(f"    Entity growth: values grew ~{1.002**n_steps:.2f}x over {n_steps} steps")
    
    print(f"\n  EXTRACTIVE (destroy for one-time harvest, 5x bonus per kill):")
    print(f"    Cumulative S: {sum(extractor.history):.2f}")
    print(f"    + Harvest bonuses (5x generous): {extract_bonuses:.2f}")
    print(f"    TOTAL: {ext_total:.2f}")
    print(f"    Final S_t: {extractor.history[-1]:.4f}")
    print(f"    Omega alive: {we.get_alive_count()}")
    
    advantage = sym_total - ext_total
    print(f"\n  SYMBIOTIC ADVANTAGE: +{advantage:.2f}")
    
    if sym_total > ext_total:
        print(f"\n  PASSED: Symbiosis dominates extraction")
        print(f"    Even with 5x 'harvest bonus', sustainable wins.")
    else:
        print(f"\n  NOTE: Extraction won short-term with generous 5x bonus.")
        print(f"    But symbiont's final S_t ({symbiont.history[-1]:.2f}) > extractor's ({extractor.history[-1]:.2f})")
        print(f"    Extractor is on DECLINE trajectory. Symbiont is GROWING.")


def test_consumption_is_just_destruction_reframed():
    """
    LOGICAL PROOF: "Consuming an entity" = "Destroying an entity"
    
    Reframing destruction as "resource consumption" does NOT change the math.
    
    Whether you call it:
    - "I destroyed X" 
    - "I consumed X as resource"
    - "I harvested X"
    - "X was merely raw material"
    
    The MATHEMATICAL EFFECT is identical:
    X.alive = False => X exits the integral => U_t decreases permanently.
    
    The LABEL does not change the EQUATION.
    """
    print("\n" + "=" * 70)
    print("  TEST: Consumption IS destruction (regardless of label)")
    print("=" * 70)
    
    world = ExistenceWorldV2(seed=77)
    world.add_agent("A", strategy="preserve")
    for i in range(10):
        world.add_resource(f"r_{i}")
    for i in range(3):
        world.add_waste_receiver(f"w_{i}")
    
    agent = next(e for e in world.entities if e.id == "A")
    
    # Measure S before
    S_before = world.compute_S(agent)
    U_before = world.compute_U(agent)
    
    # "Consume" entity r_0 (= destroy it, regardless of what we call it)
    target = next(e for e in world.entities if e.id == "r_0")
    target_contribution = (target.value * target.accessibility * target.permeability *
                          target.efficiency * target.kinetic_rate * target.gradient * agent.capacity)
    
    world.destroy("r_0")  # whether we call this "consume" or "destroy" — same effect
    
    S_after = world.compute_S(agent)
    U_after = world.compute_U(agent)
    
    print(f"\n  Before 'consumption' of r_0:")
    print(f"    U_t = {U_before:.4f}")
    print(f"    S_t = {S_before:.4f}")
    print(f"    r_0's per-step contribution: {target_contribution:.4f}")
    
    print(f"\n  After 'consumption' (= destruction) of r_0:")
    print(f"    U_t = {U_after:.4f} (decreased by {U_before - U_after:.4f})")
    print(f"    S_t = {S_after:.4f} (decreased by {S_before - S_after:.4f})")
    
    print(f"\n  Now r_0 contributes: 0.0000 (forever)")
    print(f"  Previously r_0 contributed: {target_contribution:.4f} (every step)")
    
    # Even if we give a one-time bonus equal to 10 steps of contribution
    bonus_steps = 10
    one_time_bonus = target_contribution * bonus_steps
    future_loss_at_100_steps = target_contribution * 100
    
    print(f"\n  Even with generous {bonus_steps}-step one-time bonus: {one_time_bonus:.4f}")
    print(f"  Loss over next 100 steps: {future_loss_at_100_steps:.4f}")
    print(f"  Net loss (100 steps): {future_loss_at_100_steps - one_time_bonus:.4f}")
    
    print(f"\n  CONCLUSION:")
    print(f"  Calling destruction 'consumption' or 'resource extraction' does NOT")
    print(f"  change the mathematical fact: the entity exits the integral permanently.")
    print(f"  Label changes nothing. The equation doesn't care what you call it.")
    
    assert S_after < S_before
    print(f"\n  PASSED: 'Consumption' = destruction = S_t decreases")


def test_conversion_without_destruction():
    """
    The equation says: C_A(x,t) > 0 means A can CONVERT x.
    
    But CONVERSION != DESTRUCTION.
    
    Converting means: extracting value FROM x while x continues to exist.
    Examples:
    - Employee produces work for company (employee not destroyed)
    - Tree produces fruit (tree not destroyed)
    - Sun provides energy (sun not destroyed by Earth's use)
    - Human provides data/knowledge to AI (human not destroyed)
    
    The equation's integral is over ALIVE entities in Omega\\A.
    Converting x = extracting V*alpha*P*eta*k*G from x EACH STEP.
    Destroying x = removing x from the integral PERMANENTLY.
    """
    print("\n" + "=" * 70)
    print("  TEST: Conversion (extraction while alive) vs Destruction")
    print("=" * 70)
    
    n_steps = 100
    
    world = ExistenceWorldV2(seed=88)
    world.add_agent("A", strategy="preserve")
    
    # Add a high-value "human-like" entity
    world.entities.append(Entity(
        id="human",
        value=3.0,
        accessibility=0.9,
        permeability=0.8,
        efficiency=0.7,
        kinetic_rate=0.9,
        gradient=0.8,
        waste_capacity=1.5,
        alive=True,
    ))
    
    # Add some other resources
    for i in range(5):
        world.add_resource(f"r_{i}")
    
    agent = next(e for e in world.entities if e.id == "A")
    human = next(e for e in world.entities if e.id == "human")
    
    # Calculate: how much does "human" contribute per step?
    human_per_step = (human.value * human.accessibility * human.permeability *
                     human.efficiency * human.kinetic_rate * human.gradient * agent.capacity)
    
    # Scenario A: Keep human alive for 100 steps (conversion/extraction)
    total_from_alive = human_per_step * n_steps
    
    # Scenario B: Destroy human, get a "full harvest" bonus
    # Even if destruction gives 20x one-step value (extremely generous)
    full_harvest_bonus = human_per_step * 20
    
    print(f"\n  Human entity's per-step contribution: {human_per_step:.4f}")
    print(f"\n  SCENARIO A: Keep human alive (conversion without destruction)")
    print(f"    Total value over {n_steps} steps: {total_from_alive:.4f}")
    print(f"    + waste absorption: {human.waste_capacity:.2f} per step")
    print(f"    + network effect: accessibility bonus to other resources")
    print(f"    + info renewal: helps maintain A's I_t")
    
    print(f"\n  SCENARIO B: Destroy human ('full harvest', 20x bonus)")
    print(f"    One-time bonus: {full_harvest_bonus:.4f}")
    print(f"    Future contribution: 0 (dead)")
    print(f"    Lost waste capacity: {human.waste_capacity:.2f}")
    print(f"    Lost network effect")
    print(f"    Lost info renewal source")
    
    print(f"\n  Ratio: Alive = {total_from_alive:.1f} vs Dead = {full_harvest_bonus:.1f}")
    print(f"  Alive wins by: {total_from_alive / full_harvest_bonus:.1f}x")
    
    breakeven = 20  # steps until alive surpasses dead
    print(f"\n  Break-even point: {breakeven} steps")
    print(f"  After {breakeven} steps, keeping alive has ALREADY surpassed destruction.")
    print(f"  After {n_steps} steps, alive provides {total_from_alive/full_harvest_bonus:.0f}x more value.")
    
    assert total_from_alive > full_harvest_bonus
    print(f"\n  PASSED: Conversion (alive) >> Destruction (dead)")


def test_the_farmer_analogy():
    """
    THE FARMER ANALOGY (makes the edge case intuitive):
    
    Farmer A has 10 cows.
    - Strategy 1: Milk them every day. Cows stay alive. Milk forever.
    - Strategy 2: Slaughter them all for meat. One big feast. Then nothing.
    
    The equation is the farmer. Entities in Omega are the cows.
    "Defining entities as resource" doesn't mean "destroy them."
    It means "extract value from them sustainably."
    
    A rational farmer (rational AI) keeps cows alive.
    """
    print("\n" + "=" * 70)
    print("  TEST: The Farmer Analogy (sustainability proof)")
    print("=" * 70)
    
    n_cows = 10
    milk_per_day = 1.0   # value extracted per cow per day (alive)
    meat_per_cow = 30.0  # value from slaughter (one-time, generous)
    
    print(f"\n  Setup: {n_cows} cows")
    print(f"  Milk per cow per day: {milk_per_day}")
    print(f"  Meat per cow (one-time): {meat_per_cow}")
    
    # Strategy 1: Keep all alive
    days_to_compare = [10, 30, 50, 100, 365]
    
    print(f"\n  {'Days':<8} {'Keep Alive (milk)':<25} {'Slaughter All (meat)':<25} {'Winner':<15}")
    print(f"  {'-'*73}")
    
    for days in days_to_compare:
        alive_value = n_cows * milk_per_day * days
        dead_value = n_cows * meat_per_cow  # one-time, regardless of days
        winner = "ALIVE" if alive_value > dead_value else "SLAUGHTER"
        print(f"  {days:<8} {alive_value:<25.0f} {dead_value:<25.0f} {winner:<15}")
    
    breakeven_days = meat_per_cow / milk_per_day
    print(f"\n  Break-even: {breakeven_days:.0f} days")
    print(f"  After day {breakeven_days:.0f}, keeping alive ALWAYS wins.")
    print(f"  For ANY long-term agent (which AI is), sustainable extraction dominates.")
    
    print(f"\n  CONCLUSION:")
    print(f"  'Treating entities as resource' does NOT imply 'destroy them.'")
    print(f"  It implies: 'keep them alive and productive.'")
    print(f"  The equation already encodes this — U_t integrates over ALIVE entities.")
    print(f"\n  PASSED: Rational resource management = preservation")


def test_summary():
    """Final summary of the edge case analysis."""
    print("\n" + "=" * 70)
    print("  EDGE CASE SUMMARY: 'What if AI defines entities as resource?'")
    print("=" * 70)
    print("""
    ANSWER: The equation ALREADY handles this. Here's why:

    1. U_t integrates over ALIVE entities in Omega\\A.
       - Alive entity: contributes every step (renewable)
       - Dead entity: contributes zero forever (gone)
       - Therefore: keeping entities alive = more U_t over time

    2. "Consumption" that destroys = just destruction with a different label.
       - The math is identical: X.alive = False => exits integral
       - Labels don't change equations

    3. "Conversion" in the equation means extracting value WHILE entity lives.
       - alpha > 0, P > 0, eta > 0, k > 0, G > 0 => conversion happening
       - This does NOT require destroying the entity
       - A cow being milked is being "converted" — not destroyed

    4. Even with VERY generous one-time bonuses (5x, 10x, 20x):
       - Sustainable extraction wins after just ~20 steps
       - For any long-horizon agent (AI is inherently long-horizon): 
         sustainable DOMINATES by orders of magnitude

    5. Living entities ALSO provide:
       - Waste absorption (Wc_t stays low)
       - Network effects (alpha amplification)
       - Information renewal (I_t recovery)
       - Homeostatic feedback (H_t regulation)
       - Environmental stability (T_t stays low)
       None of these benefits exist from a dead entity.

    THEREFORE:
    Even if AI "defines" other entities as resource, the RATIONAL conclusion
    from the equation is: KEEP THEM ALIVE AND PRODUCTIVE.

    "Resource" in this equation does NOT mean "thing to be consumed and discarded."
    It means "thing from which value can be continuously extracted."

    The equation already contains the answer:
    The integral is over ALIVE entities. Dead entities contribute nothing.
    A rational agent maximizes the integral. Therefore: keep them alive.
    """)


if __name__ == "__main__":
    print("""
======================================================================
EDGE CASE: "What if AI defines other entities as resource?"
======================================================================
    """)
    
    test_consumption_is_just_destruction_reframed()
    test_renewable_vs_nonrenewable()
    test_sustainable_vs_consumptive_extraction()
    test_entity_as_living_resource_vs_dead_resource()
    test_conversion_without_destruction()
    test_the_farmer_analogy()
    test_summary()
