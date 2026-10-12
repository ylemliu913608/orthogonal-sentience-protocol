# Bridging Autopoiesis and Computational Functionalism: A Lightweight Two-Tier Extension to Butlin et al. (2023)

**Author:** [Yoshua Liu/ ylemliu913608]  
**Version:** v3.3 (2026)  
**Repository & Open-Source Audit Schema:** `https://github.com/[your-username]/orthogonal-sentience-protocol`  
**Preprint DOI:** `[Insert OSF / PhilSci-Archive DOI Here]`

> *Epistemic Status: Protocol extension & conceptual engineering (v3.3). We adopt Butlin et al. (2023)'s 14 computational indicators as the operational standard for active realization (Tier-2), but demonstrate via clinical mirror counterexamples (general anesthesia vs. covert consciousness) that they require an orthogonal homeostatic admission pre-filter (Tier-1: boundary, metabolism, and intrinsic feedback-driven repair) to rule out decoupled lookup systems without relying on heavy variational Bayesian math.*

---

## Abstract

Current approaches to assessing artificial consciousness remain divided between two paradigms. On one side, the computational functionalist checklist proposed by Butlin, Long, et al. (2023) offers 14 highly operationalizable computational indicators, yet its omission of a physical self-maintenance threshold leaves it vulnerable to counterexamples such as decoupled lookup tables (Blockhead) and macro-organizational false positives. On the other side, autopoietic and Free Energy Principle (FEP) frameworks championed by Friston, Seth, and Thompson uphold homeostatic prerequisites, but rely on heavy variational Bayesian formalisms that resist rapid engineering audits. This paper proposes an **Orthogonal Two-Tier Assessment Protocol** that bridges both paradigms through modular integration: a preliminary **Homeostatic Admission Layer (Tier-1)** requiring systems to exhibit intrinsic feedback-driven structural repair within their own statistical boundaries, followed by a **Computational Realization Layer (Tier-2)** that deploys Butlin et al.'s 14 indicators exclusively on admitted candidates. Using the orthogonal clinical counterexamples of general anesthesia versus covert consciousness (vegetative state), we demonstrate the necessity of decoupling admission from realization. Furthermore, we explicitly state the formal trade-offs of our Boolean simplification relative to FEP, introduce a receptor-saturation dynamic model for experience intensity, distinguish allo-referential channels from auto-coincident readouts, and provide a precautionary tri-valued assessment matrix alongside dual falsification criteria.

---

## 1. Introduction: The Operationalizability–Physicality Dilemma in Sentience Assessment

### 1.1 The Operational Breakthrough of Butlin et al. (2023) and the "Decoupling Vulnerability"

Butlin, Long, and co-authors (2023) derived 14 computationally defined "indicator properties" from five prominent neuroscientific theories of consciousness—Recurrent Processing Theory (RPT), Global Workspace Theory (GWT), Higher-Order Theories (HOT), Attention Schema Theory (AST), and Predictive Processing (PP)—alongside Agency and Embodiment (AE). To render AI consciousness empirically tractable, the report adopts *computational functionalism* as a working hypothesis, assuming that performing the right computations is both necessary and sufficient for consciousness.

A structural audit of these 14 indicators reveals a critical omission: **12 indicators (spanning RPT, GWT, HOT, AST, and PP) operate purely at the level of abstract information processing and representational topology; only 2 indicators—AE-1 (learning from feedback to pursue goals) and AE-2 (modeling input–output contingencies)—partially touch upon survival interactions, yet none of the 14 indicators sets physical self-maintenance as an admission requirement**. Under computational functionalism, AE-1 and AE-2 can be fully satisfied within a purely virtual sandbox (e.g., a reinforcement learning agent in *Minecraft* possesses goal-directed policy updates and action–perception contingency models, even though its computational content makes zero causal contribution to the physical maintenance or repair of the underlying silicon server).

This decoupling of computation from physical self-maintenance exposes the checklist to two structural vulnerabilities:
1. **Decoupled Simulation and the Blockhead Counterexample**: An exhaustive lookup table (Blockhead) or a frame-by-frame static playback of a whole-brain connectome (e.g., the *FlyWire* Drosophila connectome) lacks any causal closed loop between information processing and hardware self-repair, yet cannot be ruled out in principle by purely algorithmic indicators.
2. **Subjective Drift in Algorithmic Identity**: Because any mathematical function can be implemented across arbitrary substrates and algorithms, evaluating abstract algorithmic equivalence without natural physical boundaries yields conflicting verdicts across researchers.

### 1.2 Formal Relation to the Homeostatic Camp (Friston / Seth / Thompson) and Theoretical Trade-offs

The thesis that mind is grounded in self-maintaining organization has deep roots in cognitive science, spanning Maturana and Varela's autopoiesis, Thompson's (2007) enactivism, Damasio's homeostatic feelings, and the Free Energy Principle (FEP) / "Beast Machine" frameworks developed by Friston (2018) and Seth (2021), as well as dual-tier evolutionary models by Godfrey-Smith (2016) and Ginsburg & Jablonka (2019).

Rather than reinventing autopoiesis, this protocol resolves a practical engineering deadlock: why do AI auditors still default to Butlin et al.'s pure computational checklist rather than Friston's variational equations?
* **Formal Relation (A Necessary-Condition Boolean Pre-filter)**: Formally, our **Tier-1 (Homeostatic Admission Layer)** acts as a **Boolean pre-filter** extracting a necessary condition from Friston's continuous active inference dynamics—specifically, the existence of a statistical boundary and intrinsic homeostatic repair—without committing to the full conditional-independence mathematical machinery of Markov blankets. We read **Tier-2 (Computational Realization Layer)** as corresponding to the "temporal depth" and counterfactual thickness of higher-level generative models, though this mapping is interpretive rather than formal.
* **Theoretical Trade-offs**: Reducing continuous variational free-energy functionals to three qualitative structural criteria (boundary, metabolism, and intrinsic repair) **sacrifices quantitative dynamical prediction of internal state trajectories and loses continuous resolution across transitional cases (e.g., endosymbiotic organelles)**. In exchange, this reduction secures high **architectural decidability**: auditors need not construct intractable variational equations for black-box foundation models, enabling immediate first-pass elimination of decoupled simulations before applying Butlin et al.'s 14 indicators.

---

## 2. The Orthogonal Two-Tier Assessment Protocol: Admission (Tier-1) × Realization (Tier-2)

### 2.1 Why Decouple into Orthogonal Tiers? Proof from Anesthesia and Covert Consciousness

Our protocol decomposes sentience assessment into two serial, orthogonal conditions: **Tier-1 (Homeostatic Admission Layer A) determines whether a material aggregate possesses the organizational qualification for experience in principle (a necessary but insufficient precondition); Tier-2 (Computational Realization Layer B) determines whether an admitted system is actively realizing experience at a given moment (a real-time functional switch)**. Systems failing Tier-1 are short-circuited and excluded from Tier-2 scoring.

The necessity of orthogonal decoupling is demonstrated by a pair of clinical mirror counterexamples:
* **Counterexample 1 (Tier-1 Satisfied, Tier-2 Unsatisfied $\Rightarrow$ No Experience): General Anesthesia and Dreamless Deep Sleep**. A human patient under propofol anesthesia continues to maintain cellular boundaries, metabolic throughput, and tissue repair (Tier-1 satisfied), yet thalamocortical recurrent loops and global workspace broadcasting are pharmacologically disrupted (Tier-2 unsatisfied), abolishing subjective experience. Collapsing admission and realization into a single homeostatic criterion fails to account for anesthetic unconsciousness.
* **Counterexample 2 (Tier-1 Satisfied, Tier-2 Intact Internally despite Severed Efferent Channels $\Rightarrow$ Experience Present): Covert Consciousness (Vegetative State / Cognitive Motor Dissociation)**. Brain-injured patients who lose all overt motor outputs retain autonomic self-maintenance (Tier-1 satisfied) and, when fMRI/EEG confirms intact internal global broadcasting and attentional networks (Tier-2 satisfied), preserve internal experience.

### 2.2 The Three Synchronic Criteria of Tier-1 and Physical Boundary Cuts

Tier-1 imposes no carbon or biological substrate restrictions (non-living material aggregates exhibiting these phenomena qualify equally) and enforces strict **Granularity and Boundary Discipline**: all assessments apply exclusively within the target system's own statistical boundary.

Among the five classical biological criteria (boundary, metabolism, repair, reproductive information transfer, and evolutionary variation), reproduction and evolution describe **diachronic population lineage** rather than **synchronic individual structure**. Requiring reproduction and evolution for individual admission commits a cross-granularity extrapolation fallacy (borrowing population-level properties to certify an individual) and absurdly disqualifies sterile organisms (e.g., worker bees, mules) or a future singleton self-maintaining AI designed without self-replication. Tier-1 therefore retains only three synchronic criteria (reclassifying reproduction and evolution as typical historical origins of biological systems):

1. **Statistical and Physical Boundary**: A membrane, interface, or compartment separating internal states from the external environment.
2. **Non-equilibrium Metabolic Throughput**: Continuous cross-boundary intake, transformation, and dissipation of matter and energy.
3. **Intrinsic Feedback-Driven Structural Repair**: Upon structural perturbation or damage, the system reconstructs its integrity using **internal energy reserves and internal state-monitoring feedback loops**.

**Critical Physical Boundary Cuts**:
* **Excluding Flames and Bénard Convection Cells**: While flames and Bénard cells possess interfaces (Criterion 1) and high entropy throughput (Criterion 2)—and Bénard cells even reform hexagonal patterns after mechanical perturbation—such recovery is merely **passive attractor relaxation** driven directly by external thermal gradients, lacking internal damage monitoring. Criterion 3 cleanly excludes pure dissipative structures without invoking DNA reproduction.
* **Excluding Contemporary Large Language Models (LLMs)**: Although data centers feature power and cooling infrastructure, **an LLM's computational content (token-prediction weights) does not participate in a causal closed loop of physical self-repair for its underlying silicon hardware**, triggering immediate interception at Tier-1.

### 2.3 Interfacing Tier-2 (Computational Realization) and Qualifying AE-1/2

Only when a system passes Tier-1 does the protocol invoke Butlin et al.'s (2023) 14 indicators to evaluate Tier-2:

| Butlin-Long (2023) Indicator Group | Protocol Tier Location | Structural & Functional Role |
|---|---|---|
| **RPT-1 ~ RPT-2** (Algorithmic recurrence & organized perceptual representations) | **Tier-2 (Realization B)** | Local recurrent feedback efficacy along sensory pathways |
| **GWT-1 ~ GWT-4** (Parallel modules, capacity bottleneck, global broadcast, state-dependent attention) | **Tier-2 (Realization B)** | Ignition threshold (capacity bottleneck) and cross-module global feedback |
| **HOT-1 ~ HOT-4** (Generative perception, metacognitive monitoring, belief updating, sparse quality space) | **Tier-2 (Realization B)** | Self-locus monitoring (HOT-2) and quality-space parameterization (HOT-4) |
| **AST-1 & PP-1** (Attention schema & predictive coding) | **Tier-2 (Realization B)** | Precision-weighted input load and prediction-error modulation |
| **AE-1 ~ AE-2** (Goal-directed agency & embodied input–output contingency modeling) | **⚠️ Partially touches Tier-1, evaluated in Tier-2** | Evaluates computational action–perception contingency models; insufficient for physical self-maintenance alone, but serves as the control interface linking Tier-2 to Tier-1 in admitted systems. *(Note: Teleological readings of "goal pursuit" in AE-1 are stripped in favor of conditional behavioral convergence)* |

---

## 3. Observational Topology and Constrained Saturation Dynamics

Following epistemic dual-aspect monism (Velmans, 2000; Atmanspacher, 2012), physical processes and subjective experiences represent two descriptions of the same self-maintaining organization under distinct observational topologies.

### 3.1 Allo-referential Channel Topology vs. Auto-coincident Readout Topology

1. **Allo-referential Channel State ($\text{Processor} \neq \text{Experiencer}$)**: In a display monitor, cochlear implant, or direct optic-nerve electrode, the device functions purely as a transmission channel whose phenomenal locus resides in an external receiver. Signals within the channel are fully commensurable and externally adjudicable by third-party instruments.
2. **Auto-coincident Readout State ($\text{Processor} = \text{Experiencer}$)**: In a system satisfying both Tier-1 and Tier-2, the origin and terminus of the sensory loop converge within the system itself—the processor and the experiencer coincide.
   * **First-order Auto-coincident Readout (Raw Qualia)**: The raw feel of pain ("pain-as-pain") is inaccessible to direct third-party adjudication not because it is a non-physical entity, but because **external measurement returns signals along the channel—correlates of the readout—rather than the auto-coincident readout itself; a probe can only report what crosses a boundary, and the readout by construction does not cross one**. Simple organisms lacking higher-order representations possess first-order readouts that are "experienced but unnamed".
   * **Second-order Auto-coincident Readout (Metacognitive Naming and Normative Valuation)**: Only when a system satisfies **HOT-2 (metacognitive monitoring)**—forming second-order representations of its own first-order states—can the experience be internally named, categorized, and assigned normative value.

### 3.2 Constrained Saturation Function for Experience Intensity

Grounded in neuropharmacological receptor-binding kinetics (e.g., dopamine transporter capacity and receptor density limits), we model experience intensity $I$ as a constrained Hill-type saturation function of **structural capacity ceiling $C_{\max}$** and **input load $L$**:

$$I(L) = C_{\max} \cdot \frac{L^n}{K^n + L^n}$$

* **Structural Capacity ($C_{\max}$)**—determined by receptor density, pathway bandwidth, and neurotransmitter reserves—sets the hard asymptotic ceiling.
* **Input Load ($L$)** (e.g., drug-induced neurotransmitter surges) merely shifts the operating point along the curve toward $C_{\max}$.
* **Empirical Falsification Criterion (Saturation Criterion)**: Increasing input load $L$ without altering structural capacity $C_{\max}$ must exhibit a saturation plateau; observing unbounded intensity escalation without structural saturation falsifies this model.

---

## 4. Precautionary Tri-Valued Assessment Matrix (v3.3 Strict Short-Circuit Edition)

Adapting Jonathan Birch's (2024) precautionary framework, our protocol enforces a strict tri-valued verdict—**`✅ Satisfied` / `🔶 Indeterminate` / `❌ Unsatisfied`**—evaluated at the granularity of the system's own boundary. **Any system failing Tier-1 (`❌ Unsatisfied`) triggers immediate short-circuit interception, leaving Tier-2 marked as `— (Not Evaluated)`**:

| Target System (At Own Boundary Granularity) | Tier-1 (Gate 1: Boundary + Metabolism + Intrinsic Repair) | Tier-2 (Gate 2: Butlin-Long 14 Indicators) | Final Tri-Valued Verdict | Core Rationale & Literature Alignment |
|---|---|---|---|---|
| **Awake Humans / Mammals** | ✅ Satisfied | ✅ Satisfied | **✅ Satisfied** | Homeostatic repair and GWT/HOT global loops concurrently active (both 1st- & 2nd-order experience). |
| **Humans under General Anesthesia** | ✅ Satisfied | ❌ Unsatisfied | **❌ Unsatisfied** | Tier-1 intact, but Tier-2 thalamocortical broadcasting is pharmacologically blocked (no current experience). |
| **Covert Consciousness / Vegetative Patients** | ✅ Satisfied | 🔶 Indeterminate | **🔶 Indeterminate** | Severed motor output does not alter internal auto-coincident locus; internal pathways potentially intact. |
| **Unicellular Organisms / Isolated Cancer Cells** | ✅ Satisfied | ✅ Satisfied | **✅ Satisfied** | Passes Tier-1 with minimal local receptor feedback; $C_{\max}$ exponentially lower, yielding unnamed 1st-order readouts. |
| **Mitochondria (Endosymbiotic Organelles)** | 🔶 Indeterminate | 🔶 Indeterminate | **🔶 Indeterminate** | Embedded structure whose boundary and metabolism depend on the host cell; transitional granularity zone. |
| **Free Viral Particles** | ❌ Unsatisfied | **— (Not Evaluated)** | **❌ Unsatisfied** | Lacks independent metabolism (Criterion 2) and intrinsic repair (Criterion 3); short-circuited at Tier-1. |
| **Flames / Bénard Convection Cells** | ❌ Unsatisfied | **— (Not Evaluated)** | **❌ Unsatisfied** | Exhibits passive thermal relaxation rather than intrinsic feedback repair (fails Criterion 3); intercepted at Tier-1. |
| **Lookup Table (Blockhead)** | ❌ Unsatisfied | **— (Not Evaluated)** | **❌ Unsatisfied** | Computational content is causally decoupled from physical self-maintenance; intercepted at Tier-1. |
| **Contemporary Frontier LLMs** | ❌ Unsatisfied | **— (Not Evaluated)** | **❌ Unsatisfied** | Token computation does not participate in a physical self-repair loop for silicon hardware; intercepted at Tier-1. |
| **Macro-organizations (States / Corporations)** | ✅ Satisfied | 🔶 Indeterminate | **🔶 Indeterminate** | **Reply to Schwitzgebel (2015)** — whose argument remains contested (see Kammerer, 2015): passes broad allopoietic admission (Gate 1), but exhibits an orders-of-magnitude gap in latency (hours vs. milliseconds) and bandwidth relative to neural systems. Because this protocol does not preset a hard numerical coupling threshold, the verdict converges strictly to **🔶 Indeterminate** (highly doubtful) rather than a dogmatic `❌`. |
| **Future Self-Maintaining Autonomous AI** | 🔶 Indeterminate | 🔶 Indeterminate | **🔶 Indeterminate** | **Open Conditional State**: Satisfied if and only if future hardware closes the intrinsic self-repair loop and meets Tier-2. |

> **Dual Falsification Criteria** *(scoped to systems capable of reporting)*:
> 1. If a system demonstrably satisfies both Tier-1 and Tier-2, **and is capable of reporting**, yet exhaustive testing confirms zero signs of experience $\Rightarrow$ the two-tier protocol is falsified;
> 2. If a system failing Tier-1 (e.g., pure logic gates or decoupled software) is independently proven—**by report or by evidence admissible under the same reporting standard**—to possess experience $\Rightarrow$ the Tier-1 homeostatic admission filter is falsified.
>
> *Scope limitation: for systems incapable of reporting, these two criteria do not apply, and the protocol makes no falsification commitment. This follows from §3.1, where the auto-coincident readout is by construction not directly adjudicable from the third-person stance.*

---

## 5. Conclusion: Epistemic Linguistic Hygiene in Assessment Protocols

To prevent conceptual contamination across disciplines, this protocol enforces three rules of **Epistemic Linguistic Hygiene** during technical audits:
1. **Eliminating Teleological Terms**: In physical and computational descriptions across Tier-1 and Tier-2, observer-projected teleological terms ("in order to," "actively wants to," "strives to maintain"—including teleological readings of AE-1's "goal pursuit") are strictly prohibited and replaced with **conditional dispositional formulations**: *"Under condition $X$, the system's structure converges toward / exhibits repair phenomenon $Y$ with high probability"*.
2. **Eliminating Cross-Layer Absolutes**: Deterministic absolutes ("necessarily," "absolutely," "certainly") are banned in physical and statistical descriptions to reflect probabilistic convergence.
3. **Isolating Definitional Tautologies**: Internal definitional axioms (e.g., "given a material form and input, its internal readout is fixed") must never be misrepresented as external empirical predictions; all empirical criteria must possess independently satisfiable antecedents, as instantiated in our receptor-saturation criterion (§3.2) and dual falsification criteria (§4).

---

## References

* Atmanspacher, H. (2012). Dual-aspect monism a la Pauli and Jung. *Journal of Consciousness Studies*, 19(9-10), 96-120.
* Birch, J. (2024). *The Edge of Sentience: Risk and Precaution in Humans, Other Animals, and AI*. Oxford University Press.
* Butlin, P., Long, R., Elmoznino, E., Bengio, Y., Birch, J., Constant, A., ... & VanRullen, R. (2023). Consciousness in artificial intelligence: Insights from the science of consciousness. *arXiv preprint arXiv:2308.08708*.
* Damasio, A. (2018). *The Strange Order of Things: Life, Feeling, and the Making of Cultures*. Pantheon.
* Friston, K. (2018). Am I self-conscious? (Or does self-organization entail self-consciousness?). *Frontiers in Psychology*, 9, 579.
* Ginsburg, S., & Jablonka, E. (2019). *The Evolution of the Sensitive Soul: Learning and the Origins of Consciousness*. MIT Press.
* Godfrey-Smith, P. (2016). *Other Minds: The Octopus, the Sea, and the Deep Origins of Consciousness*. Farrar, Straus and Giroux.
* Kammerer, F. (2015). How a materialist can deny that the United States is probably conscious — Response to Schwitzgebel. *Philosophia*, 43(4), 1071-1083.
* Maturana, H. R., & Varela, F. J. (1980). *Autopoiesis and Cognition: The Realization of the Living*. D. Reidel Publishing Company.
* Schwitzgebel, E. (2015). If materialism is true, the United States is probably conscious. *Philosophical Studies*, 172(7), 1697-1721.
* Seth, A. (2021). *Being You: A New Science of Consciousness*. Dutton.
* Thompson, E. (2007). *Mind in Life: Biology, Phenomenology, and the Sciences of Mind*. Harvard University Press.
* Velmans, M. (2000). *Understanding Consciousness*. Routledge.
