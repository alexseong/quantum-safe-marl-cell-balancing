## 1. Introduction

Lithium-ion battery packs are widely deployed in electric vehicles (EVs), grid energy storage systems (ESS), and portable electronics due to their high energy density and efficiency. However, inherent cell-to-cell variations caused by manufacturing inconsistencies, temperature gradients, and aging lead to imbalance among cells in a battery pack. This imbalance results in reduced usable capacity, accelerated degradation, and increased safety risks such as overvoltage and thermal runaway.

Traditional cell balancing methods can be broadly categorized into passive and active approaches. Passive balancing dissipates excess energy as heat through resistors, offering simplicity but suffering from energy inefficiency and thermal stress. In contrast, active balancing transfers energy between cells, significantly improving efficiency but introducing complex control challenges due to nonlinear dynamics, switching constraints, and hardware limitations.

Recent research has explored advanced control strategies, including model predictive control (MPC), mixed-integer linear programming (MILP), and reinforcement learning (RL), to address these challenges. Optimization-based methods provide constraint satisfaction and interpretability but rely heavily on accurate models and are computationally expensive. RL-based methods, on the other hand, offer adaptability and model-free learning but often lack safety guarantees and struggle with constraint violations.

Moreover, emerging trends in battery management systems (BMS) emphasize:

Safety-aware control (Safe RL)
Distributed decision-making (Multi-Agent RL)
Hybrid model-based and data-driven methods
Digital twin frameworks for training and validation

Despite these advances, existing approaches typically focus on a single paradigm and fail to integrate optimization, safety, and learning in a unified framework.

Contributions

This paper proposes a hierarchical hybrid framework for active cell balancing that integrates optimization scheduling, safe multi-agent reinforcement learning (Safe MARL), and a battery digital twin. The main contributions are:

Problem Reformulation
We formulate active cell balancing as a constrained multi-agent sequential decision problem incorporating energy transfer dynamics, safety constraints, and degradation-aware objectives.
Hierarchical Hybrid Control Architecture
We introduce a two-layer control framework:
Upper layer: optimization-based scheduler (MILP/MPC)
Lower layer: Safe Multi-Agent RL controller
Safety-Constrained Learning Mechanism
We incorporate a safety projection layer that ensures constraint satisfaction during RL execution.
Digital Twin Integration
A physics-informed digital twin is used for training, enabling robust generalization across varying operating conditions and aging states.
Multi-Objective Optimization
The framework jointly optimizes SoC balancing, energy efficiency, switching loss, thermal stress, and degradation cost.