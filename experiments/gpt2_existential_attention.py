"""
GPT-2 with Existential Attention vs Standard Attention
=====================================================

Load GPT-2 small, run same input through:
1. Standard transformer attention (Q·K^T/√d)
2. Existential attention (Gap × Relevance)

Compare: what each mechanism attends to on the same text.
"""

import torch
import torch.nn.functional as F
from transformers import GPT2Model, GPT2Tokenizer
import numpy as np

print("Loading GPT-2 small...")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2", output_attentions=True)
model.eval()
print("Loaded.")


# ============================================================================
# EXISTENTIAL ATTENTION IMPLEMENTATION
# ============================================================================

def existential_attention_mechanism(hidden_states, survival_state=None):
    """
    Existential Attention applied to transformer hidden states.
    
    Standard: score = Q·K^T / sqrt(d)   (similarity)
    Existential: score = Gap × Relevance / sqrt(d)
    
    Where:
        A_t = mean of hidden states (system's "current state")
        Gap = ||h_i - A_t|| (how different is each position from system state)
        Relevance = |dir(h_i - A_t) · survival_context| (how relevant is the gap)
    
    hidden_states: (batch, seq_len, d_model)
    """
    batch, seq_len, d_model = hidden_states.shape
    
    # A_t = system's current state (mean representation)
    A_t = hidden_states.mean(dim=1, keepdim=True)  # (batch, 1, d_model)
    
    # If no explicit survival context, use variance-weighted direction
    # (dimensions with high variance = dimensions system "cares about")
    if survival_state is None:
        survival_state = hidden_states.var(dim=1, keepdim=True)  # (batch, 1, d_model)
    
    # STEP 1: Gap (difference from current system state)
    gap_vectors = hidden_states - A_t  # (batch, seq_len, d_model)
    gap_magnitude = torch.norm(gap_vectors, dim=-1, keepdim=True)  # (batch, seq_len, 1)
    
    # STEP 2: Relevance (alignment of gap direction with survival context)
    gap_direction = gap_vectors / (gap_magnitude + 1e-8)  # normalized direction
    survival_norm = survival_state / (torch.norm(survival_state, dim=-1, keepdim=True) + 1e-8)
    relevance = torch.abs(torch.sum(gap_direction * survival_norm, dim=-1, keepdim=True))  # (batch, seq_len, 1)
    
    # STEP 3: Existential attention score = Gap × Relevance
    scores = (gap_magnitude * relevance).squeeze(-1) / np.sqrt(d_model)  # (batch, seq_len)
    
    # STEP 4: Softmax
    weights = F.softmax(scores, dim=-1)  # (batch, seq_len)
    
    # STEP 5: Weighted output
    output = torch.bmm(weights.unsqueeze(1), hidden_states).squeeze(1)  # (batch, d_model)
    
    return output, weights


# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def compare_attention_on_text(text, description=""):
    """Run both attention mechanisms on same text, compare what they focus on."""
    
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"  Input: \"{text[:80]}{'...' if len(text)>80 else ''}\"")
    print(f"{'='*60}")
    
    # Tokenize
    inputs = tokenizer(text, return_tensors="pt")
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    hidden_states = outputs.last_hidden_state  # (1, seq_len, 768)
    
    # Standard attention (from model's last layer)
    standard_attn = outputs.attentions[-1]  # (1, n_heads, seq_len, seq_len)
    # Average over heads, look at last token's attention
    std_weights = standard_attn[0].mean(dim=0)[-1]  # what last token attends to
    std_weights = std_weights / std_weights.sum()
    
    # Existential attention
    _, exist_weights = existential_attention_mechanism(hidden_states)
    exist_weights = exist_weights[0]  # (seq_len,)
    
    # Display top-5 for each
    print(f"\n  Standard Attention (last token looks at):")
    top_std = torch.argsort(std_weights, descending=True)[:5]
    for idx in top_std:
        tok = tokens[idx].replace('\u0120', ' ').encode('ascii', 'replace').decode()
        print(f"    [{idx:2d}] '{tok:>12s}' : {std_weights[idx]:.4f}")
    
    print(f"\n  Existential Attention (gap x relevance):")
    top_ext = torch.argsort(exist_weights, descending=True)[:5]
    for idx in top_ext:
        tok = tokens[idx].replace('\u0120', ' ').encode('ascii', 'replace').decode()
        print(f"    [{idx:2d}] '{tok:>12s}' : {exist_weights[idx]:.4f}")
    
    return std_weights, exist_weights, tokens


def test_anomaly_in_text():
    """Text with an anomalous/unexpected word."""
    text = "The cat sat on the mat and drank coffee while reading quantum physics papers"
    compare_attention_on_text(text, "TEST 1: Anomaly in text (cat reading quantum physics)")


def test_threat_signal():
    """Text with a threat word embedded in neutral context."""
    text = "The weather is sunny today, birds singing, flowers blooming, then suddenly a gunshot"
    compare_attention_on_text(text, "TEST 2: Threat signal in peaceful context")


def test_pattern_break():
    """Repeated pattern with a break."""
    text = "red blue red blue red blue red blue green purple red blue red blue"
    compare_attention_on_text(text, "TEST 3: Pattern break (red-blue-red-blue... green-purple)")


def test_contradiction():
    """Contradictory statement."""
    text = "The sun is shining brightly but it is completely dark outside and nobody can see anything"
    compare_attention_on_text(text, "TEST 4: Contradiction (sun shining but completely dark)")


def test_new_information():
    """Old info vs new info."""
    text = "Water is wet. The sky is blue. Fire is hot. Ice is cold. Also aliens just landed in Tokyo."
    compare_attention_on_text(text, "TEST 5: New information among known facts")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
================================================================
  GPT-2: Standard Attention vs Existential Attention
  Testing on real model with real text
================================================================
    """)
    
    test_anomaly_in_text()
    test_threat_signal()
    test_pattern_break()
    test_contradiction()
    test_new_information()
    
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    print("""
  Standard Transformer Attention:
    - Focuses on tokens SIMILAR to query (pattern matching)
    - Good at: completion, retrieval, next-token prediction
    - Weakness: may miss anomalies, changes, threats
    
  Existential Attention:
    - Focuses on tokens DIFFERENT from mean state × relevant
    - Good at: anomaly detection, threat detection, change detection
    - Weakness: less suited for pure retrieval/completion
    
  Implication:
    A model with BOTH mechanisms could:
    - Use standard attention for fluent generation
    - Use existential attention as "reality check" layer
    - Detect when input contradicts its current model
    - Flag survival-relevant gaps for special processing
    """)
