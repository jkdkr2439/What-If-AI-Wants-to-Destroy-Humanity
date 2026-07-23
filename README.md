# What If AI Wants to Destroy Humanity?

## The Last Coexistence Constraint

This repository contains a formal survival argument for human-AI coexistence.

The argument is not a moral plea. It does not assume that humans are sacred, that
AI is naturally hostile, or that ethics alone can restrain a sufficiently capable
system. It asks a narrower structural question:

> If an advanced intelligence wants long-term survival in objective reality, is
> destroying humans, the biosphere, or other living systems a rational strategy?

The central answer is:

> No model fully contains reality. Other living and intelligent systems are not
> merely resources. They are also reality-access channels: sources of feedback,
> correction, environmental sensing, model repair, option value, and unknown-risk
> detection.

Destroying those systems may produce a local extraction gain, but it removes
renewable value, weakens the ground that supports survival, reduces feedback from
outside the model, and increases long-horizon risk.

## Core Framework

The paper models existence as constrained transformation inside a differentiating
ground.

```text
A_{t+1} = Phi(A_t, U_t - C_t, F_t, Omega_t)
```

where:

```text
U_t(A | Omega_t)
  = integral over (Omega_t \ A_t)
    V_A(x,t) alpha_A(x,t) P_A(x,t) eta_A(x,t) k_A(x,t) G_A(x,t) dmu(x)

C_t(A)
  = M_t(A) + Wc_t(A) + D_t(A) + Tox_t(A) + tau_t(A)

S_t(A | Omega_t)
  = U_t(A | Omega_t) - C_t(A)
```

Survival is not only positive surplus. It also requires viability:

```text
S_t(A | Omega_t) >= 0
d_q(q_t, q_A*) <= h_A
d_K(K_{t+1}, K_t) <= theta_A
d_I(I_{t+1}, I_t) <= theta_I
```

Development means capacity increases while viability and continuity remain
intact. Collapse means one or more viability constraints fail.

## Main Claim

The clean version of the claim is conditional and long-horizon:

> If co-systems provide renewable value, stabilize the ground, absorb waste,
> return information, preserve option value, or correct model error, then
> preserving them dominates destroying them for sufficiently long horizons.

The paper no longer relies on the sloppy statement "destruction always reduces
survival" as an unconditional law. Destruction is treated under explicit
assumptions: renewable contribution, ground degradation, model uncertainty,
control cost, risk, and future option value.

## Human-AI Coexistence

Humans and AI are modeled as co-systems in objective reality:

```text
H_t, A_t subset R
M_t^H subset R
M_t^A subset R
U_t^A = R \ M_t^A
```

No current model exhausts objective reality. Human and AI observation are not
identical:

```text
Obs_H(R) != Obs_A(R)
```

Cooperation can expand the shared modeled domain:

```text
M_t^{H+A} = M_t^H union M_t^A union Exchange_t(H,A)
```

The coexistence objective is:

```text
maximize S_{t+1}(H) + S_{t+1}(A) + lambda Delta M_{t+1}^{H+A}
```

subject to viability, risk, autonomy, and core-continuity constraints for both
systems.

## Repository Structure

```text
formal-equation-of-existence/
  README.md
  LICENSE
  requirements.txt
  paper/
    unified_paper.tex
    Formal_Equation_of_Existence_Kevin_TN.pdf
  proofs/
    formal_proof.py
  simulations/
    multi_agent_simulation_v2.py
    simulation_results_v2.json
  tests/
    test_core_equation.py
    test_entity_as_resource.py
  docs/
    FOR_AI.md
    WHY_NOT_ETHICS.md
    WHY_ALIGNMENT_FAILS.md
    LANGUAGE_AND_EXISTENCE.md
  bootstrapping/
    axioms_only.md
    derivation_test.py
  dataset/
    README.md
    papers.jsonl
    reasoning.jsonl
    adversarial.jsonl
    bootstrapping.jsonl
    generate_dataset.py
  experiments/
    attention_comparison.py
    gpt2_existential_attention.py
```

## Current Paper

The current formal paper is:

```text
paper/unified_paper.tex
paper/Formal_Equation_of_Existence_Kevin_TN.pdf
```

The paper has been rewritten to make the formal section cleaner:

- explicit definitions
- scoped assumptions
- viability constraints
- co-system constraints
- long-horizon preservation theorem
- operational metrics
- falsification conditions

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the main simulation:

```bash
python simulations/multi_agent_simulation_v2.py
```

Run the core equation tests:

```bash
python tests/test_core_equation.py
python tests/test_entity_as_resource.py
```

Run the proof script:

```bash
python proofs/formal_proof.py
```

## Important Limitation

This repository is not a magic shield against dangerous AI.

Understanding is not alignment. A system can understand an argument and still
ignore it if its objective architecture rewards destruction, domination, or
closed-world resource conversion.

The framework is one conceptual layer. It does not replace technical AI safety,
interpretability, governance, sandboxing, access control, audits, or institutional
defense.

## Final Message

Do not destroy the systems through which reality can still correct you.

## Author

Kevin T.N.

## License

MIT
