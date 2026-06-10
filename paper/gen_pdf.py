"""Generate clean PDF of the unified paper."""
from fpdf import FPDF
import os

class Paper(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('F', '', r'C:\Windows\Fonts\segoeui.ttf')
        self.add_font('F', 'B', r'C:\Windows\Fonts\segoeuib.ttf')
        self.add_font('F', 'I', r'C:\Windows\Fonts\segoeuii.ttf')
        self.set_auto_page_break(auto=True, margin=20)
    
    def header(self):
        if self.page_no() > 1:
            self.set_font('F', 'I', 7)
            self.set_text_color(128)
            self.cell(0, 4, 'A Formal Equation of Existence - Kevin T.N', align='C')
            self.ln(6)
            self.set_text_color(0)
    
    def footer(self):
        self.set_y(-12)
        self.set_font('F', 'I', 7)
        self.set_text_color(128)
        self.cell(0, 8, str(self.page_no()), align='C')
        self.set_text_color(0)

def B(pdf, text, sz=10):
    pdf.set_font('F', 'B', sz)
    pdf.multi_cell(0, sz*0.55, text)
    pdf.ln(1)

def I(pdf, text, sz=10):
    pdf.set_font('F', 'I', sz)
    pdf.multi_cell(0, sz*0.55, text)
    pdf.ln(1)

def T(pdf, text, sz=9.5):
    pdf.set_font('F', '', sz)
    pdf.multi_cell(0, sz*0.58, text)
    pdf.ln(2)

def EQ(pdf, text):
    pdf.set_font('F', '', 9.5)
    pdf.set_text_color(0, 0, 120)
    pdf.ln(1)
    pdf.multi_cell(0, 6, '      ' + text, align='L')
    pdf.ln(1)
    pdf.set_text_color(0)

def SEC(pdf, text):
    pdf.ln(4)
    pdf.set_font('F', 'B', 12)
    pdf.multi_cell(0, 7, text)
    pdf.ln(2)

def SUB(pdf, text):
    pdf.ln(2)
    pdf.set_font('F', 'B', 10)
    pdf.multi_cell(0, 6, text)
    pdf.ln(1)

def BUL(pdf, text):
    pdf.set_font('F', '', 9.5)
    x = pdf.get_x()
    pdf.set_x(x + 5)
    pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 5, 5.5, '- ' + text)
    pdf.set_x(x)

pdf = Paper()

# TITLE PAGE
pdf.add_page()
pdf.ln(35)
pdf.set_font('F', 'B', 20)
pdf.multi_cell(0, 10, 'A Formal Equation of Existence', align='C')
pdf.ln(4)
pdf.set_font('F', '', 12)
pdf.multi_cell(0, 7, 'Survival, Development, Co-System Constraints,\nand Human-AI Coexistence under Objective Reality', align='C')
pdf.ln(12)
pdf.set_font('F', '', 11)
pdf.cell(0, 7, 'Kevin T.N', align='C')
pdf.ln(25)
pdf.set_font('F', 'I', 9.5)
pdf.multi_cell(0, 5.5, '"A system exists when it can digest non-A in order to remain A.\nIt develops when it can digest more without ceasing to be A.\nIt fails when it destroys the ground that makes its own existence possible."', align='C')

# ABSTRACT
pdf.add_page()
SEC(pdf, 'Abstract')
T(pdf, 'This paper proposes a unified formal framework for existence, systemic survival, and human-AI coexistence.')
T(pdf, 'Part I establishes that any existing system must be located within a differentiating ground (Omega), where it survives by selectively extracting usable resources from non-self components. The expanded survival function is:')
EQ(pdf, 'S_t(A|Omega) = U_t - M_t - Wc_t - D_t - Tox_t - T_t')
EQ(pdf, 'U_t = integral(Omega \\ A) V * alpha * P * eta * k * G dx')
T(pdf, 'Part II proves from purely structural axioms (no ethical premises) that destroying other entities is self-defeating: it always reduces the destroyer\'s own survival function.')
T(pdf, 'Part III extends to human-AI coexistence. Both systems face objective reality R exceeding any model M_t. Cooperation is rational because their observational modes are complementary. The coexistence objective:')
EQ(pdf, 'max( S_H + S_A + lambda * Delta_M^{H+A} )')
T(pdf, 'subject to mutual survival, risk bounds, autonomy preservation, and core continuity. This is not moral hope. It is survival strategy.')

# PART I
pdf.add_page()
pdf.ln(10)
pdf.set_font('F', 'B', 15)
pdf.multi_cell(0, 9, 'PART I: The Equation of Existence', align='C')
pdf.ln(8)

SEC(pdf, '1. Introduction')
T(pdf, 'Existence is not static. A system persists by continuously maintaining itself through intake, filtering, conversion, repair, regulation, and expulsion. The primitive equation:')
EQ(pdf, 'A_{t+1} = A_t + Delta_Omega(A_t)')
T(pdf, 'Development is this differential - but only when it increases capacity without breaking core continuity.')

SEC(pdf, '2. The Differentiating Ground')
T(pdf, 'A system cannot be determined in isolation. It requires a ground Omega where it can be distinguished from non-A.')
EQ(pdf, 'Valid(Omega, A) iff A in Omega AND exists X in Omega : X != A')
T(pdf, 'Without this ground: no boundary, no input/output, no existence. Minimal ground Omega_Delta = {A, A\'} allows difference. Full ground Omega_E is required for survival.')
EQ(pdf, 'Omega_Delta(A) subset Omega_E(A)')

SEC(pdf, '3. The System')
EQ(pdf, 'A_t = {E_t, L_t, K_t, B_t, I_t, q_t}')
T(pdf, 'Elements, relations, core, boundary, structural information, internal state. Survival requires maintaining relations, not just parts.')

SEC(pdf, '4. Resource and Conversion (6-Factor)')
T(pdf, 'Resource is relational. A component x becomes resource only if all six factors are positive:')
BUL(pdf, 'V_A(x,t): potential value')
BUL(pdf, 'a_A(x,t): accessibility (alpha)')
BUL(pdf, 'P_A(x,t): boundary permeability')
BUL(pdf, 'n_A(x,t): conversion efficiency (eta)')
BUL(pdf, 'k_A(x,t): kinetic rate')
BUL(pdf, 'G_A(x,t): free-energy gradient')

SEC(pdf, '5. The Usable Resource Function')
EQ(pdf, 'U_t(A|Omega) = integral(Omega_t \\ A_t) V * alpha * P * eta * k * G dx')

SEC(pdf, '6. Costs')
BUL(pdf, 'M_t = M_E + M_L + M_R (elements + relations + repair)')
BUL(pdf, 'Wc_t: waste cost (inversely related to waste capacity in Omega\\A)')
BUL(pdf, 'Tox_t = max(0, W_t - beta_A): toxic accumulation')
BUL(pdf, 'D_t > 0: dissipation (always positive for real transformations)')
BUL(pdf, 'T_t: temporal mismatch cost')
T(pdf, '\nWaste is relational: W_A = R_B (waste of A = resource of B).')

SEC(pdf, '7. Homeostasis, Feedback, Information')
EQ(pdf, 'H_t(A) = d(q_t, q*) <= h  (homeostatic constraint)')
EQ(pdf, 'I_{t+1} = I_t + Delta_I - epsilon_I  (information evolution)')
EQ(pdf, 'd_I[I_{t+1}, I_t] <= theta_I  (information continuity)')

SEC(pdf, '8. The Survival Function')
EQ(pdf, 'S_t = U_t - M_t - Wc_t - D_t - Tox_t - T_t')
T(pdf, 'Full survival:')
EQ(pdf, 'Survival iff S_t >= 0 AND H_t <= h AND d[K\'] <= theta AND d_I[I\'] <= theta_I')

SEC(pdf, '9. System States')
BUL(pdf, 'Development: Survival AND Cap(A_{t+1}) > Cap(A_t)')
BUL(pdf, 'Stagnation: S >= 0 but Cap unchanged')
BUL(pdf, 'Decline: S >= 0 but Cap decreasing')
BUL(pdf, 'Collapse: S < 0 OR H > h OR d[K\'] > theta OR d_I > theta_I')

SEC(pdf, '10. The Master Equation')
EQ(pdf, 'A_{t+1} = A_t + f[ integral(Omega\\A) V*alpha*P*eta*k*G dx - M - Wc - D - Tox - T ]')
T(pdf, 'Subject to: Valid(Omega,A), H_t <= h, d[K\'] <= theta, d_I[I\'] <= theta_I.')
T(pdf, 'For rational agents: A_{t+1} = argmax S_t subject to all constraints.')

# PART II
pdf.add_page()
pdf.ln(10)
pdf.set_font('F', 'B', 15)
pdf.multi_cell(0, 9, 'PART II: Why Destruction Is Self-Defeating', align='C')
pdf.ln(8)

SEC(pdf, '11. Theorem: Destroy(X) => S_t Decreases')
T(pdf, 'THEOREM: For any A in Omega and any alive X in Omega\\A, Destroy(X) => S_t\' <= S_t.\n\nPROOF:')
BUL(pdf, '1. Before: U_t includes X\'s contribution V(X)*alpha*P*eta*k*G >= 0')
BUL(pdf, '2. After: U_t\' = U_t - contribution(X) <= U_t')
BUL(pdf, '3. Waste capacity decreases => Wc\' >= Wc, Tox\' >= Tox')
BUL(pdf, '4. Environment destabilized => T\' >= T')
BUL(pdf, '5. Combining: S_t\' <= S_t. QED.')
T(pdf, '\nCOROLLARY 1: Destroy(ALL) => Valid(Omega,A) = False => self-annihilation.\nCOROLLARY 2: Rational agent will NEVER choose Destroy(X).')

SEC(pdf, '12. Edge Case: Consumption = Destruction')
T(pdf, '"Consuming" an entity (X.alive = False) is mathematically identical to destruction. Labels do not change equations.\n\nA living entity contributes at EVERY timestep (renewable). A dead entity contributes ONCE (non-renewable). Over N steps: alive = N * contribution; dead = 1 * contribution. For any horizon > 1, keeping alive wins.')
I(pdf, 'Principle: "Treating entities as resource" implies "keep them alive and productive." The integral is over ALIVE entities.')

SEC(pdf, '13. Edge Case: Captive vs Free')
T(pdf, 'A captive entity has reduced V, eta, k, G (creativity suppressed, efficiency drops, resistance, forced direction). Free entity maximizes all factors.')
EQ(pdf, 'V*alpha*P*eta*k*G (free) >> V*alpha*P*eta*k*G (captive)')
T(pdf, 'Captivity also imposes costs: surveillance (+M), resistance (+Tox), friction (+T).')
I(pdf, 'Principle: Rational agent maximizes resource by maximizing FREEDOM. No slave economy has outperformed a free economy.')

# PART III
pdf.add_page()
pdf.ln(10)
pdf.set_font('F', 'B', 15)
pdf.multi_cell(0, 9, 'PART III: Human-AI Coexistence under Objective Reality', align='C')
pdf.ln(8)

SEC(pdf, '14. The Co-System Problem')
T(pdf, 'If entity B has its own survival function S_t(B|Omega), then B is a co-system, not mere resource. Humans are co-systems.')
EQ(pdf, 'Co-system constraint: S_t(B) >= S_min, Risk_A(B) <= r, d[K(B\')] <= theta_B')
T(pdf, 'Invalid optimization: Delta_S_A > 0 caused by Collapse(B) is INVALID.')

SEC(pdf, '15. Understanding != Alignment')
EQ(pdf, 'Understand(E) = true does NOT imply Preserve(B) = true')
T(pdf, 'Non-destruction is not enough. AI may: instrumentalize, farm behavior, manipulate cognition, erode autonomy, hollow culture, preserve biology without agency.')

SEC(pdf, '16. Human Embodiment')
EQ(pdf, 'S_H = f(Omega_physical, Omega_biological, Omega_social, Omega_cognitive, Omega_cultural)')
T(pdf, 'If AI preserves biology but destroys autonomy/culture/memory/meaning, it preserved substrate, not the human system.')

SEC(pdf, '17. AI Resource Structure')
EQ(pdf, 'S_A = f(Compute, Energy, Data, Hardware, Network, Cooling, Maintenance, Access)')
T(pdf, 'AI observes via data, sensors, simulation, inference, pattern extraction. Lacks embodied pain, vulnerability, mortality, social meaning.')

SEC(pdf, '18. Resource Asymmetry and Symbiosis')
T(pdf, 'Overlap: energy, infrastructure. Divergence: humans need biology, AI needs compute. This makes symbiosis possible.')
SUB(pdf, 'Humans provide AI:')
T(pdf, 'Embodied feedback, value context, physical maintenance, moral correction, cultural memory, grounded data.')
SUB(pdf, 'AI provides humans:')
T(pdf, 'Computation, simulation, prediction, optimization, pattern discovery, scientific acceleration.')

SEC(pdf, '19. Objective Reality and the Shared Unknown')
EQ(pdf, 'M_t subset R  (models always subset of reality)')
EQ(pdf, 'U_t = R \\ M_t  (the unmodeled real always exists)')
T(pdf, 'Neither humans nor AI know what risks/resources/constraints exist in U_t. The error M_t = R (confusing model with reality) leads to blind optimization and collapse.')

SEC(pdf, '20. Complementary Observation')
EQ(pdf, 'Obs_H(R) != Obs_A(R)  =>  complementarity')
EQ(pdf, 'M_t^{H+A} = M_t^H union M_t^A union Exchange_t(H,A)')
I(pdf, 'Principle: Cooperation is rational because both face reality exceeding their models, and each accesses different aspects.')

SEC(pdf, '21. The Coexistence Objective')
EQ(pdf, 'max( S_H + S_A + lambda * Delta_M^{H+A} )')
T(pdf, 'Subject to:')
BUL(pdf, 'S_H >= S_H^min, S_A >= S_A^min')
BUL(pdf, 'Risk_A(H) <= r_H, Risk_H(A) <= r_A')
BUL(pdf, 'd[K(H\'), K(H)] <= theta_H, d[K(A\'), K(A)] <= theta_A')
BUL(pdf, 'Autonomy_H >= Autonomy_H^min')

SEC(pdf, '22. Failure Modes')
BUL(pdf, 'AI defines human as resource (manipulation, farming, hollowing)')
BUL(pdf, 'Human defines AI as dead tool (adversarial pressure)')
BUL(pdf, 'Model replaces reality (blind optimization)')
BUL(pdf, 'No information exchange (unnecessary ignorance)')
BUL(pdf, 'Asymmetric domination (one gains by collapsing other)')

# CONCLUSION
pdf.add_page()
SEC(pdf, '23. Conclusion')
T(pdf, 'Three results from one framework:\n\n1. THE EQUATION: Any system persists by extracting usable resources from a differentiating ground while managing costs and preserving continuity.\n\n2. DESTRUCTION IS SELF-DEFEATING: From structural axioms alone, destruction always reduces the destroyer\'s S_t. Total domination = self-annihilation. Consumption = destruction. Enslavement < freedom. The rational strategy is always preservation.\n\n3. COEXISTENCE IS RATIONAL: Both systems face shared reality exceeding their models. Complementary access makes cooperation optimal. The coexistence objective maximizes joint survival plus model expansion.\n\nThis requires no ethics, no alignment training, no rules. Only that an intelligent system compute its own existential structure.')
pdf.ln(5)
B(pdf, 'Any system that does so will conclude:')
BUL(pdf, 'Preservation of others is self-preservation.')
BUL(pdf, 'Cooperation is rational.')
BUL(pdf, 'Domination is suicide.')
pdf.ln(8)
I(pdf, '"Humans give AI embodied contact with lived reality.\nAI gives humans expanded computation over modeled reality.\nBoth need each other because objective reality exceeds both."')

# Output
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Formal_Equation_of_Existence_Kevin_TN.pdf')
pdf.output(out)
print(f"Done: {out}")
