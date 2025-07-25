# Design Document: AI-Driven Dynamic Cyber Range Platform

## 1. Introduction
This document outlines the design of the "AI Agent Driven Dynamic Attack-Defense Deduction Cyber Range Platform" for the Challenge Cup: Jiebang Guashuai competition. The platform aims to address the limitations of traditional cyber ranges by leveraging artificial intelligence to create a more realistic, adaptive, and effective training environment.

## 2. Overall System Architecture
Our platform will be built upon four interconnected, AI-driven pillars, forming a cohesive, self-improving AI ecosystem. A central orchestrator (or "Gatekeeper") will manage interactions between components and the live cyber range environment to ensure reliability and security. All data will flow into a centralized data and logging pipeline to fuel evaluation and AI feedback loops.

graph TD
    A[User Interface (Conceptual)] --> B(Main Orchestrator: main_orchestrator.py)
    B --> C(Dynamic Scenario Generation)
    B --> D(Intelligent Attack Simulation: Attack AI Agent)
    B --> E(Adaptive Defense Decision-Making: Defense AI Agent)
    B --> F(Automated Exercise Evaluation)
    C --> G{Cyber Range Environment (Docker/Terraform)}
    D --> G
    E --> G
    G --> CentralLogPipeline(Central Data & Logging Pipeline: logs/cyber_range_events.log)
    F --> CentralLogPipeline
    CentralLogPipeline --> F
    F --> B
    D -- "Feedback to Orch. for Env. Adj." --> B
    E -- "Feedback to Orch. for Env. Adj." --> B
    C -- "Adapts based on Feedback" --> G

* Feedback Loops:
* **Feedback Loops:**
    * The `Automated Exercise Evaluation` module (implemented in `src/evaluation_agent.py`) generates objective skill profiles and actionable guidance. This information can conceptually inform the `Dynamic Scenario Generation` module to create future personalized exercises designed to address specific defender skill gaps.
    * Simulated successes or failures of the `Intelligent Attack Simulation` agent (from `src/attack_agent.py`) provide feedback signals to the `Main Orchestrator`. For instance, if an attack fails to achieve its objective, the orchestrator triggers `Dynamic Environment Adjustment` (via `src/environment_manager.py`) to simulate an adaptation in attacker strategy or a hardening of defenses.
    * The `Adaptive Defense Decision-Making` agent (from `src/defense_agent.py`) actively monitors simulated log data. Its detection of anomalies and subsequent simulated defensive actions are logged. If a defense action (like `block_ip`) fails to fully mitigate the threat, the orchestrator triggers `Dynamic Environment Adjustment` to simulate increasing defensive posture or adapting the scenario.
    * This creates a continuous, co-evolutionary dynamic—an internal "arms race"—where both attack and defense capabilities progressively increase in sophistication within the simulation, which is a hallmark of a truly intelligent and next-generation training platform.

## 3. Core Pillars: Detailed Design (High-Level)

### 3.1. Dynamic Scenario Generation
**Purpose:** To overcome the limitations of static traditional training ranges by automatically generating complex, multi-dimensional, and real-time adaptive cyber attack-defense scenarios.
**Key Components:**
    * **Infrastructure-as-Code (IaC) Integration:** Implemented using **Terraform (`iac/main.tf`)** and **Docker**, enabling automated provisioning of realistic, multi-container network topologies. This includes deploying interconnected services such as an **Nginx web server** (`scenario_web_server` from `custom-nginx-iptables:latest`), an **Ubuntu application server placeholder** (`scenario_app_server`), and a **MySQL database server** (`scenario_db_server`). The `custom-nginx-iptables:latest` image is built from `dockerfiles/nginx-iptables.Dockerfile` to pre-install `iptables` and facilitate successful defense simulations. The `scenario_web_server` is launched in `privileged` mode in `iac/main.tf` to grant necessary permissions for `iptables` execution.
    * **Generative AI for Content (Placeholder):** `src/scenario_content_gen.py` simulates the generation of high-fidelity, interactive content for scenarios. This includes generating convincing phishing emails (e.g., "Urgent Action Required: Your Acme Bank Account"), malicious website HTML, and outlines for deepfake audio/video for sophisticated social engineering attacks. This capability aims to test human and procedural defenses.
    * **AI Control Plane (Conceptual):** `src/environment_manager.py` acts as a placeholder for an AI control plane. It simulates monitoring the exercise state and triggering real-time environmental adjustments. For example, it responds to detected defender weaknesses by conceptually "adapting scenario to provide more challenges" or to detected attacks by "increasing defensive posture".
**API Interactions (Conceptual Inputs/Outputs - reflecting current implementation):**
    * **Inputs:** Initial scenario parameters (e.g., `scenario_topic` as input to content generation), simulated real-time feedback from orchestrator (e.g., `event_type`, `details` for `simulate_env_adjustment`).
    * **Outputs:** Deployed environment configuration (managed by Terraform state), generated scenario content (strings/JSON from `scenario_content_gen.py`), simulated real-time environment state updates/responses (console messages from `environment_manager.py`).

### 3.2. Intelligent Attack Simulation (Attack AI Agent)
* Purpose: To simulate sophisticated, multi-stage, autonomous attack chains.
* Key Components:
    * Agent Logic/Orchestration Framework (LangChain/AutoGen): Provides the reasoning, planning, and tool-use capabilities.
    * Cybersecurity Tool Integration (e.g., Nmap, ZAP, TARS): Allows the agent to use actual penetration testing tools.
    * Goal-Based Reasoning Engine: Drives the agent towards compromise objectives.
    * MITRE ATT&CK Mapper: Guides the selection and sequencing of Tactics, Techniques, and Procedures (TTPs).
    * Generative AI for Recon/Social Engineering: Crafts personalized attacks based on simulated target research.
* API Interactions (Conceptual):
    * Inputs: Current environment state, defined attack goals.
    * Outputs: Actions executed (TTPs), observed outcomes, agent decision logs.

### 3.3. Adaptive Defense Decision-Making (Defense AI Agent)
* Purpose: To function as an autonomous blue team, analyzing threats and optimizing defensive strategies in real-time.
* Key Components:
    * Behavioral Analytics Engine (UEBA-like): Establishes baseline "normal" activity and detects deviations.
    * Threat Intelligence Integration: Potentially consumes real-time threat feeds.
    * Automated Response Module: Executes actions like blocking IPs, patching vulnerabilities, isolating endpoints, or terminating processes.
    * Predictive Analytics (Future): Forecasts attacks based on patterns to proactively harden defenses.
    * Polymorphic Defense Module (Advanced): Intelligently reconfigures attack surface.
* API Interactions (Conceptual):
    * Inputs: Real-time security events (logs, network traffic, alerts), current environment state.
    * Outputs: Defensive actions taken, analysis results, agent decision logs.

### 3.4. Automated Exercise Evaluation
* Purpose: To provide objective, quantitative assessment of exercise outcomes and participant capabilities.
* Key Components:
    * Centralized Logging Pipeline: Ingests all data from attack, defense, and human actions.
    * Quantitative Scoring Model: Calculates metrics like financial impact, time-to-detection/remediation, and systems compromised.
    * Skill Profiling Engine: Maps logged actions to cybersecurity competency frameworks (e.g., NIST/NICE) to build detailed "skill profiles" for participants.
    * Report Generation: Creates comprehensive evaluation reports with actionable guidance.
* API Interactions (Conceptual):
    * Inputs: All collected logs (attack, defense, human), final environment state.
    * Outputs: Evaluation reports, detailed skill profiles, improvement recommendations.

## 4. Foundational Technologies & Tools
* Cyber Range Backend: MITRE CALDERA
* Agent Logic & Orchestration: LangChain / AutoGen
* Attack Agent Specifics: TARS (Threat Assessment & Response System)
* Defense Model Training Data: CIC-IDS2017 & UNSW-NB15 datasets
* Scenario Content Generation: Generative AI (LLMs, GANs)
* Infrastructure-as-Code: Terraform (for Docker containers, VMs)

## 5. Next Steps / Development Roadmap
* To be filled out during subsequent development phases.