"""
=============================================================================
Existential Attention vs Transformer Attention
=============================================================================

Formalizing attention from the Formal Equation of Existence:

TRANSFORMER ATTENTION (Vaswani et al., 2017):
    Attn(Q, K, V) = softmax(Q·K^T / sqrt(d)) · V
    
    Principle: similarity between query and keys determines what to attend to.
    "What in context is SIMILAR to what I'm looking for?"

EXISTENTIAL ATTENTION (Kevin T.N):
    Attn_E(A_t, Omega, V) = softmax(Gap(A_t, Omega) * Relevance(A_t, Omega) / sqrt(d)) · V
    
    Principle: GAP (mismatch from current state) × SURVIVAL-RELEVANCE determines attention.
    "What in Omega is DIFFERENT from my current state AND relevant to my survival?"

Key differences:
    1. Transformer: similarity-based (Q·K = how similar is this to what I want?)
    2. Existential: gap-based × relevance (how DIFFERENT is this from my state, 
       AND how relevant is it to my survival/goals?)

Prediction:
    - Transformer attention focuses on SIMILAR things (confirmation)
    - Existential attention focuses on GAPS that MATTER (novelty + relevance)
    - Existential should be better at: anomaly detection, change detection,
      threat detection, opportunity detection, learning from surprise
    - Transformer should be better at: pattern matching, retrieval, completion

=============================================================================
"""

import numpy as np
from typing import Tuple


# ============================================================================
# FORMALIZATION
# ============================================================================

def transformer_attention(Q: np.ndarray, K: np.ndarray, V: np.ndarray) -> np.ndarray:
    """
    Standard Transformer Attention (Vaswani et al., 2017)
    
    Attn(Q, K, V) = softmax(Q · K^T / sqrt(d_k)) · V
    
    Q: (seq_len, d_k) - queries
    K: (seq_len, d_k) - keys
    V: (seq_len, d_v) - values
    
    Principle: attend to what is SIMILAR to query.
    """
    d_k = K.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)  # similarity scores
    weights = softmax(scores)
    output = weights @ V
    return output, weights


def existential_attention(A_t: np.ndarray, Omega: np.ndarray, V: np.ndarray,
                          survival_context: np.ndarray = None) -> np.ndarray:
    """
    Existential Attention (from Formal Equation of Existence)
    
    Attn_E(A_t, Omega, V) = softmax(Gap * Relevance / sqrt(d)) · V
    
    Where:
        Gap(A_t, x_i) = ||x_i - A_t|| = how DIFFERENT is x_i from current state
        Relevance(A_t, x_i) = how relevant is x_i to survival of A_t
        
    A_t: (d,) - current system state (like Query, but it's the SELF)
    Omega: (n, d) - differentiating ground (all non-A signals)
    V: (n, d_v) - values to extract
    survival_context: (d,) - what the system "needs" (goals/threats/resources)
    
    Principle: attend to what is DIFFERENT from current state AND relevant to survival.
    
    Derivation from the book:
    - "Attention neo chenh lech" (attention anchors gaps)
    - Chenh lech = x_i - A_t (difference from current state)
    - But not ALL gaps matter. Only gaps RELEVANT to system's survival.
    - Relevance determined by: is this resource? threat? waste? feedback?
    """
    d = Omega.shape[-1]
    
    # STEP 1: Compute GAP (mismatch/difference from current state)
    # How different is each element in Omega from A_t?
    # This is the "chenh lech" - the deviation from the "nen" (background/current state)
    gap = np.linalg.norm(Omega - A_t, axis=-1)  # (n,) - magnitude of difference
    
    # STEP 2: Compute RELEVANCE (survival-relevance)
    # How relevant is each gap to the system's survival?
    # If no survival context given, use A_t as proxy for "what system cares about"
    if survival_context is None:
        survival_context = A_t
    
    # Relevance = how aligned is the gap direction with what the system needs
    gap_direction = Omega - A_t  # (n, d) - direction of each gap
    relevance = gap_direction @ survival_context / (np.linalg.norm(gap_direction, axis=-1) * np.linalg.norm(survival_context) + 1e-8)
    relevance = np.abs(relevance)  # both threats and resources are relevant
    
    # STEP 3: Existential attention score = Gap × Relevance
    # Large gap + high relevance = high attention
    # Small gap (similar to current state) = low attention (nothing new)
    # Large gap + low relevance = noise, not attended
    scores = gap * relevance / np.sqrt(d)
    
    # STEP 4: Softmax to get weights
    weights = softmax(scores.reshape(1, -1)).flatten()
    
    # STEP 5: Weighted sum of values
    output = weights @ V
    return output, weights


def softmax(x: np.ndarray) -> np.ndarray:
    """Numerically stable softmax."""
    e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e_x / e_x.sum(axis=-1, keepdims=True)


# ============================================================================
# COMPARISON TESTS
# ============================================================================

def test_novelty_detection():
    """
    TEST 1: Which attention better detects novel/anomalous signals?
    
    Setup: System in stable state. Most of environment is similar to state.
    One element is very different (novel signal).
    
    Prediction: Existential attention will focus on the novel signal.
    Transformer attention will focus on the similar elements.
    """
    print("=" * 70)
    print("  TEST 1: Novelty Detection")
    print("  Setup: 1 novel signal among 9 familiar signals")
    print("=" * 70)
    
    np.random.seed(42)
    d = 8
    n = 10
    
    # System state
    A_t = np.random.randn(d) * 0.5
    
    # Environment: 9 similar to A_t, 1 very different (novel)
    Omega = np.zeros((n, d))
    for i in range(9):
        Omega[i] = A_t + np.random.randn(d) * 0.1  # similar (small gap)
    Omega[9] = A_t + np.random.randn(d) * 3.0  # NOVEL (large gap)
    
    # Values (identity for simplicity)
    V = Omega.copy()
    
    # Transformer attention: Q = A_t (what am I looking for?), K = Omega
    Q = A_t.reshape(1, -1)  # (1, d)
    K = Omega  # (n, d)
    _, t_weights = transformer_attention(Q, K, V)
    t_weights = t_weights.flatten()
    
    # Existential attention
    _, e_weights = existential_attention(A_t, Omega, V)
    
    print(f"\n  Novel signal is at index 9")
    print(f"\n  Transformer attention weights (top 3):")
    top_t = np.argsort(t_weights)[::-1][:3]
    for idx in top_t:
        print(f"    idx {idx}: {t_weights[idx]:.4f} {'<-- NOVEL' if idx == 9 else ''}")
    
    print(f"\n  Existential attention weights (top 3):")
    top_e = np.argsort(e_weights)[::-1][:3]
    for idx in top_e:
        print(f"    idx {idx}: {e_weights[idx]:.4f} {'<-- NOVEL' if idx == 9 else ''}")
    
    print(f"\n  Attention on novel signal:")
    print(f"    Transformer: {t_weights[9]:.4f}")
    print(f"    Existential: {e_weights[9]:.4f}")
    print(f"    Ratio (E/T): {e_weights[9] / (t_weights[9] + 1e-8):.1f}x")
    
    if e_weights[9] > t_weights[9]:
        print(f"\n  RESULT: Existential attention detects novel signal BETTER")
    else:
        print(f"\n  RESULT: Transformer attention detects novel signal better")


def test_threat_detection():
    """
    TEST 2: Threat detection
    
    Setup: System in state A_t. Environment has neutral elements + one threat.
    Threat = element very different from current state AND relevant to survival.
    
    Prediction: Existential attention prioritizes threat.
    """
    print("\n" + "=" * 70)
    print("  TEST 2: Threat Detection (survival-relevant gap)")
    print("=" * 70)
    
    np.random.seed(123)
    d = 8
    n = 10
    
    # System state: "healthy, stable"
    A_t = np.ones(d) * 0.5
    
    # Survival context: system cares about certain dimensions (e.g., first 4 = vital)
    survival_context = np.zeros(d)
    survival_context[:4] = 1.0  # first 4 dims are survival-critical
    
    # Environment
    Omega = np.zeros((n, d))
    for i in range(8):
        Omega[i] = A_t + np.random.randn(d) * 0.2  # neutral noise
    # Element 8: large gap but IRRELEVANT (differs on non-survival dims)
    Omega[8] = A_t.copy()
    Omega[8, 4:] += 5.0  # big difference, but on irrelevant dimensions
    # Element 9: THREAT (differs on survival-critical dimensions)
    Omega[9] = A_t.copy()
    Omega[9, :4] -= 3.0  # big difference on SURVIVAL dimensions
    
    V = Omega.copy()
    
    # Transformer
    Q = A_t.reshape(1, -1)
    _, t_weights = transformer_attention(Q, Omega, V)
    t_weights = t_weights.flatten()
    
    # Existential (with survival context)
    _, e_weights = existential_attention(A_t, Omega, V, survival_context)
    
    print(f"\n  idx 8: Large gap on IRRELEVANT dimensions")
    print(f"  idx 9: Large gap on SURVIVAL-CRITICAL dimensions (threat)")
    
    print(f"\n  Transformer weights:")
    print(f"    Irrelevant gap (8): {t_weights[8]:.4f}")
    print(f"    Threat (9):         {t_weights[9]:.4f}")
    
    print(f"\n  Existential weights:")
    print(f"    Irrelevant gap (8): {e_weights[8]:.4f}")
    print(f"    Threat (9):         {e_weights[9]:.4f}")
    
    e_ratio = e_weights[9] / (e_weights[8] + 1e-8)
    t_ratio = t_weights[9] / (t_weights[8] + 1e-8)
    print(f"\n  Threat/Irrelevant ratio:")
    print(f"    Transformer: {t_ratio:.2f}")
    print(f"    Existential: {e_ratio:.2f}")
    
    if e_ratio > t_ratio:
        print(f"\n  RESULT: Existential attention BETTER distinguishes threat from noise")


def test_confirmation_bias():
    """
    TEST 3: Confirmation bias
    
    Setup: System has a state. Environment has confirming + disconfirming evidence.
    
    Prediction: 
    - Transformer (similarity-based) naturally focuses on CONFIRMING evidence
    - Existential (gap-based) naturally focuses on DISCONFIRMING evidence (gaps)
    """
    print("\n" + "=" * 70)
    print("  TEST 3: Confirmation vs Disconfirmation")
    print("  (Does the system attend to what confirms or challenges it?)")
    print("=" * 70)
    
    np.random.seed(456)
    d = 8
    
    # System's current "belief state"
    A_t = np.array([1, 1, 1, 1, 0, 0, 0, 0], dtype=float)
    
    # Evidence
    n = 6
    Omega = np.zeros((n, d))
    # 3 confirming (similar to A_t)
    Omega[0] = A_t + np.random.randn(d) * 0.1
    Omega[1] = A_t + np.random.randn(d) * 0.1
    Omega[2] = A_t + np.random.randn(d) * 0.15
    # 3 disconfirming (very different from A_t)
    Omega[3] = -A_t + np.random.randn(d) * 0.1
    Omega[4] = -A_t + np.random.randn(d) * 0.1
    Omega[5] = -A_t + np.random.randn(d) * 0.15
    
    V = Omega.copy()
    
    # Transformer
    Q = A_t.reshape(1, -1)
    _, t_weights = transformer_attention(Q, Omega, V)
    t_weights = t_weights.flatten()
    
    # Existential
    _, e_weights = existential_attention(A_t, Omega, V)
    
    t_confirm = t_weights[:3].sum()
    t_disconfirm = t_weights[3:].sum()
    e_confirm = e_weights[:3].sum()
    e_disconfirm = e_weights[3:].sum()
    
    print(f"\n  Elements 0-2: Confirming (similar to A_t)")
    print(f"  Elements 3-5: Disconfirming (opposite to A_t)")
    
    print(f"\n  Transformer attention distribution:")
    print(f"    Confirming:     {t_confirm:.4f} ({100*t_confirm:.1f}%)")
    print(f"    Disconfirming:  {t_disconfirm:.4f} ({100*t_disconfirm:.1f}%)")
    
    print(f"\n  Existential attention distribution:")
    print(f"    Confirming:     {e_confirm:.4f} ({100*e_confirm:.1f}%)")
    print(f"    Disconfirming:  {e_disconfirm:.4f} ({100*e_disconfirm:.1f}%)")
    
    print(f"\n  RESULT:")
    if t_confirm > t_disconfirm:
        print(f"    Transformer: CONFIRMATION BIAS ({100*t_confirm:.0f}% on confirming)")
    if e_disconfirm > e_confirm:
        print(f"    Existential: NOVELTY SEEKING ({100*e_disconfirm:.0f}% on disconfirming)")


def test_change_detection():
    """
    TEST 4: Detecting important changes in a stream
    
    Setup: A sequence where most tokens are stable, then something changes.
    Which attention mechanism detects the change faster?
    """
    print("\n" + "=" * 70)
    print("  TEST 4: Change Detection in Temporal Stream")
    print("=" * 70)
    
    np.random.seed(789)
    d = 8
    
    # System has adapted to a stable pattern
    stable_pattern = np.array([1, 0.5, 0.3, 0.2, 0, 0, 0, 0], dtype=float)
    A_t = stable_pattern.copy()  # system's current state = adapted to pattern
    
    # Stream: mostly stable, one CHANGE at position 7
    n = 10
    Omega = np.zeros((n, d))
    for i in range(10):
        Omega[i] = stable_pattern + np.random.randn(d) * 0.05  # stable noise
    # Position 7: sudden change
    Omega[7] = np.array([0, 0, 0, 0, 1, 1, 1, 1], dtype=float)  # pattern reversal
    
    V = Omega.copy()
    
    # Transformer
    Q = A_t.reshape(1, -1)
    _, t_weights = transformer_attention(Q, Omega, V)
    t_weights = t_weights.flatten()
    
    # Existential
    _, e_weights = existential_attention(A_t, Omega, V)
    
    print(f"\n  Stable stream with change at position 7")
    print(f"\n  Attention on change point (idx 7):")
    print(f"    Transformer: {t_weights[7]:.4f} (rank: {10 - np.argsort(np.argsort(t_weights))[7]})")
    print(f"    Existential: {e_weights[7]:.4f} (rank: {10 - np.argsort(np.argsort(e_weights))[7]})")
    
    if e_weights[7] > t_weights[7]:
        print(f"\n  RESULT: Existential attention detects change {e_weights[7]/t_weights[7]:.1f}x better")


def test_summary():
    """Summary of the two formulations."""
    print("\n" + "=" * 70)
    print("  FORMAL COMPARISON")
    print("=" * 70)
    print("""
    TRANSFORMER ATTENTION:
    ─────────────────────
    score(q, k_i) = q · k_i / sqrt(d)
    weights = softmax(scores)
    output = weights · V
    
    Principle: SIMILARITY determines attention
    Asks: "What in context looks like what I'm looking for?"
    
    
    EXISTENTIAL ATTENTION:
    ──────────────────────
    gap_i = ||x_i - A_t||                    (magnitude of difference from self)
    relevance_i = |dir(x_i - A_t) · s| / (||dir|| · ||s||)   (survival alignment)
    score_i = gap_i × relevance_i / sqrt(d)
    weights = softmax(scores)
    output = weights · V
    
    Principle: GAP × RELEVANCE determines attention
    Asks: "What in Omega is DIFFERENT from me AND matters for my survival?"
    
    
    KEY STRUCTURAL DIFFERENCES:
    ───────────────────────────
    1. Transformer attends to SIMILARITY → confirmation bias
       Existential attends to GAPS → novelty/change detection
    
    2. Transformer has no concept of "self" → Q is just a learned vector
       Existential has A_t (system state) as reference → attention is relative to self
    
    3. Transformer has no survival/relevance filter → all similarities equal
       Existential filters by survival-relevance → only IMPORTANT gaps attended
    
    4. Transformer: good at retrieval, completion, pattern matching
       Existential: good at anomaly detection, threat detection, learning from surprise
    
    5. Transformer can develop confirmation bias (attend to what confirms)
       Existential structurally avoids this (attends to what CHALLENGES current state)
    
    
    PREDICTION FOR AI SAFETY:
    ─────────────────────────
    An AI using existential attention would:
    - Notice when its model diverges from reality (gap detection)
    - Prioritize survival-relevant information over mere similarity
    - Be structurally less prone to confirmation bias
    - Better detect unknown threats in U_t (unmodeled real)
    - Better at learning from surprise/correction
    
    This aligns with the paper's thesis: a system that attends to GAPS
    in its differentiating ground is better equipped to survive than one
    that only attends to what confirms its current state.
    """)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
======================================================================
  EXISTENTIAL ATTENTION vs TRANSFORMER ATTENTION
  Formal comparison from the Equation of Existence
======================================================================
    """)
    
    test_novelty_detection()
    test_threat_detection()
    test_confirmation_bias()
    test_change_detection()
    test_summary()
