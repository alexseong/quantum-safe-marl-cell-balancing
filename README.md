# Quantum-Safe MARL Cell Balancing

A quantum-compatible optimization scheduler with safe multi-agent reinforcement learning for active cell balancing in lithium-ion battery packs using a battery digital twin.

## Research Title
**A Quantum-Compatible Optimization Scheduler with Safe Multi-Agent Reinforcement Learning for Active Cell Balancing Using a Battery Digital Twin**

## Overview
This repository implements a research-grade framework for intelligent active cell balancing. The framework combines:
- Battery Digital Twin
- Active Cell Balancing Simulator
- QUBO Optimization Scheduler
- QUBO-to-Ising Mapping
- Cost Hamiltonian Construction
- QAOA Toy Experiment
- Safe PPO
- Safe MAPPO
- Baseline Comparison
- Ablation Study
- Scaling Analysis

## System Architecture
```text
Battery Digital Twin
   ↓
Quantum-Compatible QUBO Scheduler
   ↓
Ising / Hamiltonian Mapping
   ↓
QAOA / Simulated Annealing / Classical Solver
   ↓
Safe Multi-Agent RL Controller
   ↓
Safety Shield
   ↓
Active Balancing Execution
   ↓
Evaluation and Paper Figures