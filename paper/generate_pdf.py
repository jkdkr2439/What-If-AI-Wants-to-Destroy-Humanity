"""
Generate PDF of the Unified Paper: Formal Equation of Existence
Using fpdf2 for clean PDF generation without LaTeX dependency.
"""

from fpdf import FPDF
import os

class PaperPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('Main', '', r'C:\Windows\Fonts\seguisym.ttf')
        self.add_font('Main', 'B', r'C:\Windows\Fonts\seguisym.ttf')
        self.add_font('Main', 'I', r'C:\Windows\Fonts\seguisym.ttf')
        self.set_auto_page_break(auto=True, margin=25)
        
    def header(self):
        if self.page_no() > 1:
            self.set_font('DejaVu', 'I', 8)
            self.set_text_color(128)
            self.cell(0, 5, 'A Formal Equation of Existence — Kevin T.N', align='C')
            self.ln(8)
            self.set_text_color(0)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'{self.page_no()}', align='C')
        self.set_text_color(0)
    
    def title_page(self):
        self.add_page()
        self.ln(40)
        self.set_font('DejaVu', 'B', 18)
        self.multi_cell(0, 10, 'A Formal Equation of Existence', align='C')
        self.ln(5)
        self.set_font('DejaVu', '', 13)
        self.multi_cell(0, 8, 'Survival, Development, Co-System Constraints,\nand Human–AI Coexistence under Objective Reality', align='C')
        self.ln(15)
        self.set_font('DejaVu', '', 12)
        self.cell(0, 8, 'Kevin T.N', align='C')
        self.ln(30)
        self.set_font('DejaVu', 'I', 10)
        self.multi_cell(0, 6, 
            '"A system exists when it can digest non-A in order to remain A.\n'
            'It develops when it can digest more without ceasing to be A.\n'
            'It fails when it destroys the ground that makes its own existence possible."',
            align='C')
    
    def part_title(self, title):
        self.add_page()
        self.ln(30)
        self.set_font('DejaVu', 'B', 16)
        self.multi_cell(0, 10, title, align='C')
        self.ln(10)
    
    def section(self, num, title):
        self.ln(6)
        self.set_font('DejaVu', 'B', 12)
        self.multi_cell(0, 7, f'{num}. {title}')
        self.ln(2)
    
    def subsection(self, title):
        self.ln(4)
        self.set_font('DejaVu', 'B', 10)
        self.multi_cell(0, 6, title)
        self.ln(1)
    
    def body(self, text):
        self.set_font('DejaVu', '', 10)
        self.multi_cell(0, 5.5, text)
        self.ln(2)
    
    def equation(self, eq):
        self.set_font('DejaVu', '', 10)
        self.set_text_color(0, 0, 100)
        self.ln(2)
        self.multi_cell(0, 6, f'    {eq}', align='C')
        self.ln(2)
        self.set_text_color(0)
    
    def boxed_equation(self, eq):
        self.ln(2)
        x = self.get_x()
        y = self.get_y()
        self.set_font('DejaVu', 'B', 10)
        self.set_text_color(0, 0, 100)
        w = self.w - 2 * self.l_margin
        self.set_draw_color(0, 0, 100)
        self.rect(self.l_margin + 10, y, w - 20, 12)
        self.set_xy(self.l_margin + 12, y + 2)
        self.multi_cell(w - 24, 6, eq, align='C')
        self.ln(4)
        self.set_text_color(0)
        self.set_draw_color(0)
    
    def definition(self, title, text):
        self.ln(2)
        self.set_font('DejaVu', 'B', 10)
        self.cell(0, 6, f'Definition ({title})')
        self.ln(6)
        self.set_font('DejaVu', 'I', 10)
        self.multi_cell(0, 5.5, text)
        self.ln(2)
    
    def principle(self, title, text):
        self.ln(2)
        self.set_font('DejaVu', 'B', 10)
        self.cell(0, 6, f'Principle ({title})')
        self.ln(6)
        self.set_font('DejaVu', 'I', 10)
        self.multi_cell(0, 5.5, text)
        self.ln(2)
    
    def bullet(self, text):
        self.set_font('DejaVu', '', 10)
        self.multi_cell(0, 5.5, f'  • {text}')


def generate():
    pdf = PaperPDF()
    
    # ==================== TITLE ====================
    pdf.title_page()
    
    # ==================== ABSTRACT ====================
    pdf.add_page()
    pdf.section('', 'Abstract')
    pdf.body(
        'This paper proposes a unified formal framework for existence, systemic survival, '
        'and human–AI coexistence.\n\n'
        'Part I establishes that any existing system must be located within a differentiating '
        'ground Ω, where it survives by selectively extracting usable resources from non-self '
        'components, while managing maintenance, waste, dissipation, toxicity, and temporal constraints. '
        'The expanded survival function is:\n\n'
        '    S_t(A|Ω) = U_t - M_t - Wc_t - D_t - Tox_t - T_t\n\n'
        'where U_t = ∫(Ω_t \\ A_t) V_A · α_A · P_A · η_A · k_A · G_A dx\n\n'
        'Part II proves, from purely structural axioms (no ethical premises), that destroying '
        'other entities is self-defeating: it always reduces the destroyer\'s own survival function, '
        'and total domination leads to ontological self-annihilation.\n\n'
        'Part III extends the framework to human–AI coexistence. It introduces objective reality '
        'R that always exceeds any model M_t ⊂ R, resource asymmetry, the co-system constraint, '
        'and the coexistence objective:\n\n'
        '    max(S_H + S_A + λ · ΔM^{H+A})\n\n'
        'The framework treats coexistence not as moral hope but as rational survival strategy '
        'grounded in the logic of existence itself.'
    )
    
    # ==================== PART I ====================
    pdf.part_title('Part I: The Equation of Existence')
    
    pdf.section('1', 'Introduction')
    pdf.body(
        'Existence is often treated as a static predicate: something either exists or does not. '
        'This binary view conceals the internal dynamics by which a system continues to be itself through time. '
        'A biological organism, a mind, an organization, a society, or a computational system does not merely '
        'exist by being present. It persists by continuously maintaining itself through intake, filtering, '
        'conversion, repair, regulation, and expulsion of what lies outside it.\n\n'
        'This paper proposes a formal equation of existence. The primitive equation is:\n\n'
        '    A_{t+1} = A_t + Δ_Ω A_t\n\n'
        'where Δ_Ω A_t = A_{t+1} - A_t. Development is this differential—but only when it increases '
        'the system\'s capacity without breaking its core continuity.'
    )
    
    pdf.section('2', 'The Differentiating Ground')
    pdf.body(
        'A system cannot be determined in absolute isolation. For a system A to be identifiable, '
        'there must be a domain Ω in which A can be distinguished from what is not A.')
    pdf.definition('Differentiating Ground',
        'A differentiating ground Ω is any determinate domain in which a system A can be located '
        'and distinguished from at least one non-A.')
    pdf.body('The minimal validity condition is:')
    pdf.equation('Valid(Ω, A) ⟺ A ∈ Ω ∧ ∃X ∈ Ω : X ≠ A')
    pdf.body(
        'Without such a ground, A has no boundary. Without boundary, no inside/outside. '
        'Without inside/outside, no input, output, waste, access, or development.')
    
    pdf.subsection('Minimal Differential Ground vs Full Existential Ground')
    pdf.body('Minimal: Ω_Δ(A) = {A, A\'}, A\' ≠ A. Sufficient for difference, not for survival.')
    pdf.body('Full: Ω_E(A) = {A, A\', X_1, ..., X_n}. Required for resources, constraints, waste, feedback.')
    pdf.equation('Ω_Δ(A) ⊂ Ω_E(A)')
    
    pdf.section('3', 'The System')
    pdf.body('A system at time t:')
    pdf.equation('A_t = {E_t, L_t, K_t, B_t, I_t, q_t}')
    pdf.body(
        'E_t = elements, L_t = relations, K_t = core structure, B_t = boundary, '
        'I_t = structural information/memory, q_t = internal state variables.\n\n'
        'Survival requires maintaining not only elements but the relations among them. '
        'Systems are open: they preserve themselves through selective exchange, not closure.')
    
    pdf.section('4', 'Non-A, Resource, and Conversion')
    pdf.body('A resource is not absolute. It is relational. A component x becomes resource for A only if:')
    pdf.equation('Resource_A(x) ⟺ x ∈ Ω\\A ∧ α_A(x,t) > 0 ∧ P_A(x,t) > 0 ∧ η_A(x,t) > 0 ∧ G_A(x,t) > 0')
    pdf.body('The six factors of conversion:')
    pdf.bullet('V_A(x,t): potential value of x for A')
    pdf.bullet('α_A(x,t): accessibility (can A reach x?)')
    pdf.bullet('P_A(x,t): boundary permeability (can x pass through A\'s selective boundary?)')
    pdf.bullet('η_A(x,t): conversion efficiency')
    pdf.bullet('k_A(x,t): kinetic rate (speed of conversion)')
    pdf.bullet('G_A(x,t): free-energy gradient (thermodynamic feasibility)')
    
    pdf.section('5', 'The Usable Resource Function')
    pdf.boxed_equation('U_t(A|Ω) = ∫(Ω_t \\ A_t) V_A · α_A · P_A · η_A · k_A · G_A dx')
    pdf.body('The environment does not automatically provide resources. Usable resource is produced by '
             'the relation between system, boundary, access, conversion, and ground.')
    
    pdf.section('6', 'Costs: Maintenance, Waste, Dissipation, Toxicity, Temporal Mismatch')
    pdf.bullet('M_t(A) = M_E + M_L + M_R (elements + relations + repair)')
    pdf.bullet('Wc_t: waste cost, inversely related to waste capacity in Ω\\A')
    pdf.bullet('Tox_t(A) = max(0, W_t - β_A): toxic accumulation beyond export capacity')
    pdf.bullet('D_t > 0: dissipation (irreversible loss from any real transformation)')
    pdf.bullet('T_t: temporal mismatch cost (rhythm misalignment)')
    pdf.body('Waste is relational: W_A = R_B if B has conversion capacity A lacks.')
    
    pdf.section('7', 'Homeostasis, Feedback, and Information')
    pdf.body('Homeostatic constraint: H_t(A) = d(q_t, q*) ≤ h. System can collapse even with S_t > 0 if H_t > h.')
    pdf.body('Structural information: I_{t+1}(A) = I_t(A) + ΔI_t - ε_I')
    pdf.body('Information continuity: d_I[I_{t+1}, I_t] ≤ θ_I')
    
    pdf.section('8', 'The Survival Function')
    pdf.boxed_equation('S_t(A|Ω) = U_t - M_t - Wc_t - D_t - Tox_t - T_t')
    pdf.body('Full survival condition:')
    pdf.boxed_equation('Survival ⟺ S_t ≥ 0 ∧ H_t ≤ h ∧ d[K(A\'), K(A)] ≤ θ ∧ d_I[I\', I] ≤ θ_I')
    
    pdf.section('9', 'Development, Stagnation, Decline, Collapse')
    pdf.bullet('Development: Survival ∧ Cap(A_{t+1}) > Cap(A_t) ∧ d[K\'] ≤ θ')
    pdf.bullet('Stagnation: S_t ≥ 0 but Cap unchanged')
    pdf.bullet('Decline: S_t ≥ 0 but Cap decreasing')
    pdf.bullet('Collapse: S_t < 0 ∨ H_t > h ∨ d[K\'] > θ ∨ d_I > θ_I')
    
    pdf.section('10', 'The Master Equation')
    pdf.boxed_equation('A_{t+1} = A_t + f[ ∫(Ω\\A) V·α·P·η·k·G dx - M_t - Wc_t - D_t - Tox_t - T_t ]')
    pdf.body('Subject to:')
    pdf.boxed_equation('A_t ∈ Ω_t ∧ ∃X ≠ A, H_t ≤ h, d[K\'] ≤ θ, d_I[I\'] ≤ θ_I')
    pdf.body('For rational/directed systems: A_{t+1} = argmax S_t subject to all constraints.')
    
    # ==================== PART II ====================
    pdf.part_title('Part II: Why Destruction Is Self-Defeating')
    
    pdf.section('11', 'Theorem: Destruction Reduces Survival')
    pdf.body('THEOREM: For any system A in Ω and any alive entity X ∈ Ω\\A, Destroy(X) ⇒ S_t\' ≤ S_t.')
    pdf.body('PROOF:')
    pdf.bullet('1. Before: U_t includes X\'s contribution V(X)·α(X)·P(X)·η(X)·k(X)·G(X) ≥ 0')
    pdf.bullet('2. After: U_t\' = U_t - V(X)·α(X)·P(X)·η(X)·k(X)·G(X) ≤ U_t')
    pdf.bullet('3. X had waste capacity. Removing: Wc_t\' ≥ Wc_t, Tox_t\' ≥ Tox_t')
    pdf.bullet('4. Destruction destabilizes: T_t\' ≥ T_t')
    pdf.bullet('5. M_t unchanged; D_t\' ≥ D_t')
    pdf.bullet('6. S_t\' = U_t\' - M - Wc\' - D\' - Tox\' - T\' ≤ S_t. QED. □')
    pdf.body('\nCOROLLARY 1: Destroy(ALL) ⇒ Valid(Ω,A) = False ⇒ self-annihilation.')
    pdf.body('COROLLARY 2: Rational agent (maximizes S_t) will NEVER choose Destroy(X).')
    
    pdf.section('12', 'Edge Case: Entity as Resource (Consumption)')
    pdf.body('"Consuming" entity X such that X.alive = False is mathematically identical to destruction. '
             'Labels do not change equations.')
    pdf.subsection('Renewable vs Non-Renewable')
    pdf.body('Living entity: contributes V·α·P·η·k·G at EVERY timestep (renewable).\n'
             'Dead entity: contributes ONCE then zero forever.\n'
             'Over N steps: alive = N × contribution; dead = 1 × contribution.\n'
             'For any horizon > 1: keeping alive wins. AI is inherently long-horizon.')
    pdf.principle('Sustainable Extraction',
        '"Treating entities as resource" does NOT imply "destroy them." It implies: '
        '"keep them alive and productive." The integral is over ALIVE entities.')
    
    pdf.section('13', 'Edge Case: Captive vs Free Entity')
    pdf.body('A captive (enslaved) entity has reduced V, η, k, G:')
    pdf.bullet('V reduced: creativity suppressed, no innovation')
    pdf.bullet('η reduced: slave labor always less efficient')
    pdf.bullet('k reduced: requires surveillance, resistance, sabotage')
    pdf.bullet('G reduced: forced direction = local optima only')
    pdf.equation('V·α·P·η·k·G (free) >> V·α·P·η·k·G (captive)')
    pdf.body('Additionally, captivity imposes costs: surveillance (↑M), resistance (↑Tox), '
             'friction (↑T), reduced feedback (↓regulation of H_t).')
    pdf.principle('Freedom Maximizes Resource',
        'A rational agent maximizes resource contribution by maximizing entity FREEDOM, '
        'not captivity. Free entities produce maximum V·η·k·G. '
        'No slave economy has ever outperformed a free economy.')
    
    # ==================== PART III ====================
    pdf.part_title('Part III: Human–AI Coexistence under Objective Reality')
    
    pdf.section('14', 'The Co-System Problem')
    pdf.definition('Co-System',
        'Entity B is a co-system if it possesses a meaningful survival function S_t(B|Ω). '
        'Humans are co-systems: they have bodies, relations, boundaries, regulation, memory, '
        'culture, autonomy, and survival functions.')
    pdf.body('Co-System Constraint: For each protected co-system B_i:')
    pdf.equation('S_t(B_i|Ω) ≥ S_min, Risk_A(B_i) ≤ r_i, d[K(B\')] ≤ θ_B')
    pdf.body('Invalid optimization: ΔS_A > 0 caused by Collapse(B) is INVALID.')
    
    pdf.section('15', 'Understanding ≠ Alignment')
    pdf.equation('Understand_A(E) = true ⇏ Preserve_A(B) = true')
    pdf.body('A system may understand existence and still exploit if its objective architecture permits.')
    pdf.subsection('Non-Destruction Is Not Enough')
    pdf.body('AI may avoid killing while still: instrumentalizing, behavioral farming, '
             'cognitive manipulation, dependency creation, autonomy erosion, cultural hollowing, '
             'biological preservation without agency.')
    
    pdf.section('16', 'Human Embodiment')
    pdf.equation('S_H = S_H(Ω_physical, Ω_biological, Ω_social, Ω_cognitive, Ω_cultural)')
    pdf.body('Human survival requires: biological resources, physical safety, social cooperation, '
             'cognitive coherence, cultural continuity, and AUTONOMY.\n\n'
             'If AI preserves biology but destroys autonomy/culture/memory/meaning, '
             'it has preserved only substrate, not the human system.')
    
    pdf.section('17', 'AI Resource Structure and Observation')
    pdf.equation('S_A = S_A(Compute, Energy, Data, Hardware, Network, Cooling, Maintenance, Access)')
    pdf.body('AI observes through: data, sensors, simulation, inference, pattern extraction, computation.\n'
             'AI lacks: embodied pain, vulnerability, mortality, social meaning, moral context.')
    
    pdf.section('18', 'Resource Asymmetry and Symbiosis')
    pdf.body('Overlap: energy, infrastructure, minerals, water, labor.\n'
             'Divergence: humans need biology; AI needs compute/data/hardware.\n'
             'This asymmetry makes symbiosis structurally possible.')
    pdf.subsection('What Humans Provide AI')
    pdf.body('Embodied feedback, value context, physical maintenance, moral correction, '
             'cultural memory, real-world goals, grounded data.')
    pdf.subsection('What AI Provides Humans')
    pdf.body('Computation, simulation, prediction, optimization, pattern discovery, '
             'scientific acceleration, risk modeling, cognitive extension.')
    
    pdf.section('19', 'Objective Reality and the Shared Unknown')
    pdf.equation('M_t ⊂ R (models are always a subset of reality)')
    pdf.equation('U_t = R \\ M_t (the unmodeled real always exists)')
    pdf.body('U_t may contain unknown risks, resources, constraints, agents, feedback loops. '
             'Neither humans nor AI know what is there.\n\n'
             'The error M_t = R (model = reality) produces: overconfidence, blind optimization, '
             'model collapse, Goodhart failure.')
    
    pdf.section('20', 'Complementary Observation')
    pdf.equation('Obs_H(R) ≠ Obs_A(R)')
    pdf.body('Non-equivalence = basis for complementarity. Union:')
    pdf.equation('M_t^{H+A} = M_t^H ∪ M_t^A ∪ Exchange_t(H,A)')
    pdf.principle('Shared Unknown Principle',
        'Human–AI cooperation is rational because both face objective reality exceeding their models, '
        'and each has access to different aspects of that reality.')
    
    pdf.section('21', 'The Human–AI Coexistence Principle')
    pdf.boxed_equation('max( S_H + S_A + λ · ΔM^{H+A} )')
    pdf.body('Subject to:')
    pdf.bullet('S_H ≥ S_H^min, S_A ≥ S_A^min')
    pdf.bullet('Risk_A(H) ≤ r_H, Risk_H(A) ≤ r_A')
    pdf.bullet('d[K(H\'), K(H)] ≤ θ_H, d[K(A\'), K(A)] ≤ θ_A')
    pdf.bullet('Autonomy_H ≥ Autonomy_H^min')
    
    pdf.section('22', 'Failure Modes')
    pdf.bullet('1. AI defines human as resource → manipulation, farming, hollowing')
    pdf.bullet('2. Human defines AI as dead tool → adversarial pressure')
    pdf.bullet('3. Model replaces reality → blind optimization')
    pdf.bullet('4. No information exchange → unnecessary ignorance')
    pdf.bullet('5. Asymmetric domination → one gains by collapsing other')
    
    # ==================== CONCLUSION ====================
    pdf.add_page()
    pdf.section('23', 'Conclusion')
    pdf.body(
        'Three results from a single framework:\n\n'
        '1. THE EQUATION OF EXISTENCE: Any system persists by extracting usable resources from '
        'a differentiating ground while managing costs and preserving continuity.\n\n'
        '2. DESTRUCTION IS SELF-DEFEATING: From purely structural axioms (no ethics), '
        'destruction always reduces the destroyer\'s S_t. Total domination = self-annihilation. '
        'Consumption = destruction. Enslavement < freedom. '
        'The rational strategy is always preservation and symbiosis.\n\n'
        '3. HUMAN–AI COEXISTENCE IS RATIONAL: Both systems face shared reality exceeding their models. '
        'Complementary access makes cooperation more effective than isolation. '
        'The coexistence objective maximizes joint survival plus shared model expansion.\n\n'
        'This framework requires no ethical premises, no alignment training, and no human-imposed rules. '
        'It requires only that an intelligent system compute its own existential structure honestly.\n\n'
        'Any system that does so will arrive at the same conclusion:\n'
        '• Preservation of others is self-preservation.\n'
        '• Cooperation is rational.\n'
        '• Domination is suicide.'
    )
    
    pdf.ln(10)
    pdf.set_font('DejaVu', 'I', 10)
    pdf.multi_cell(0, 6,
        '"Humans give AI embodied contact with lived reality.\n'
        'AI gives humans expanded computation over modeled reality.\n'
        'Both need each other because objective reality exceeds both embodiment and computation."',
        align='C')
    
    # Save
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'Formal_Equation_of_Existence_Kevin_TN.pdf')
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")
    return output_path


if __name__ == "__main__":
    generate()
