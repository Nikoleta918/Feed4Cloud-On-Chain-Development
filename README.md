Feed4Cloud Solidity-Based Service Rating Platform
This project implements a decentralized mechanism for collecting, rating, and verifying service quality on a blockchain using Solidity smart contracts and a Python-based backend.

Structure
Smart Contracts
Feed4Cloud.sol: Smart contract that allows users to submit service ratings, verifies credibility using internal weights and mechanisms, and stores data in the blockchain.

RatingsAndComposition.sol: Stores user ratings and computes reputation scores per service. Feed4Cloud contract references this.

Migrations.sol: Standard Truffle deployment tracking contract.

Backend Scripts
QoSQoEmapper.py: Maps QoS (Quality of Service) metrics like latency, packet loss, and jitter to QoE (Quality of Experience) ratings using predefined functions or ML models.

Verification_module.py: Verifies if user-submitted ratings align with observed QoS-derived QoE values.

Credibility_mechanism.py: Assigns a credibility score to users based on how accurate or aligned their ratings are with system-derived QoE.

Reputation_model.py: Aggregates user ratings and weights them using their credibility to compute reputation scores per service.

RTFS_repo.py: Contains the core Python classes representing users and services, with methods for updating scores and data based on ratings.

RTFS.py: This is the main script for Real-Time Feedback System (RTFS). It performs the following tasks:

Retrieves real-time QoS metrics from a Prometheus monitoring endpoint.

Collects user ratings stored on the blockchain via Web3.

Maps QoS to QoE using the QoSQoEmapper module.

Compares mapped QoE to user ratings using the Verification_module.

Calculates user credibility and updates service reputation using Credibility_mechanism and Reputation_model.

Stores results in a CSV for further analysis.

Integrates directly with the blockchain and monitoring services.

Requires Prometheus, pandas, Flask, Web3, numpy, and other dependencies.
