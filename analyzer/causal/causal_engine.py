import json
from pathlib import Path

from analyzer.graph.dependency_graph import (
    build_dependency_graph,
    build_dependency_graph_from_file,
)

BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_TRACE_FILE = BASE_DIR / "data" / "sample-trace.json"


def analyze_causal_chain(
    anomalous_service,
    anomalous_event_time=None,
    graph=None,
):
    """
    Build a backward causal candidate chain from the anomalous service.

    For a dependency graph:
        checkout -> inventory -> payment

    If payment is anomalous, the causal chain is:
        payment -> inventory -> checkout

    The anomalous service is treated as the leading root-cause candidate.
    """

    if graph is None:
        graph = build_dependency_graph_from_file(DEFAULT_TRACE_FILE)

    if anomalous_service not in graph.nodes:
        raise ValueError(
            f"Service '{anomalous_service}' not found in dependency graph"
        )

    chain = [anomalous_service]
    current = anomalous_service

    while True:
        parents = list(graph.predecessors(current))

        if not parents:
            break

        parent = parents[0]
        chain.append(parent)
        current = parent

    return {
        "anomalous_service": anomalous_service,
        "event_time": anomalous_event_time,
        "causal_chain": chain,
        "candidate_root_cause": anomalous_service,
        "dependency_depth": max(len(chain) - 1, 0),
    }


def build_dependency_graph(trace_data=None):
    """
    Compatibility wrapper.
    """
    if trace_data is None:
        return build_dependency_graph_from_file(DEFAULT_TRACE_FILE)

    return build_dependency_graph(trace_data)


if __name__ == "__main__":
    result = analyze_causal_chain("payment")
    print(json.dumps(result, indent=2))
