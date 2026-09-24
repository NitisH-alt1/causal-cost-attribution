# Cloud Economics Intelligence Platform

## Overview

Cloud Economics Intelligence Platform is an intelligent cloud-cost analysis system designed to identify anomalous cost behavior and trace potential contributing services across distributed application dependencies.

The platform combines service dependency analysis, anomaly signals, temporal relationships, and causal candidate scoring to produce an explainable cost-attribution chain.

## Core Analysis

The current analysis pipeline evaluates relationships such as:

Payment Service
    ↓
Inventory Service
    ↓
Checkout Service

For a detected anomaly, the engine traces the dependency chain backward and identifies candidate root causes based on anomaly strength and propagation behavior.

## Architecture

- FastAPI-based analysis and dashboard services
- OpenTelemetry-based distributed telemetry
- Dependency graph analysis
- Temporal causal candidate analysis
- Anomaly scoring
- Cost attribution
- Explainable causal-chain visualization

## Current Status

The platform currently provides:

- Service dependency graph
- Anomaly analysis
- Causal candidate scoring
- Root-cause candidate identification
- Causal-chain visualization
- REST API endpoints
- Web dashboard

## Research Position

The system performs temporal causal candidate analysis rather than claiming definitive causal proof. Its objective is to provide explainable, measurable evidence for potential cost-driving events in distributed cloud environments.

## Project Structure

- services/ — distributed application services
- collector/ — telemetry collection
- nalyzer/ — anomaly, graph, causal, and scoring components
- dashboard/ — analysis dashboard and API
- data/ — analysis datasets and generated results
- experiments/ — controlled experiments
- 	ests/ — validation and evaluation
- deployment/ — deployment configurations
