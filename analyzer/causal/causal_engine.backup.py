from pathlib import Path

from analyzer.graph.dependency_graph import (
    build_dependency_graph,
    build_dependency_graph_from_file,
)


DEFAULT_TRACE_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "sample-trace.json"
)


def analyze_causal_chain(
    anomalous_service,
    anomalous_event_time=None,
    graph=None,
):
    """
    Analyze the upstream dependency chain for an anomalous service.

    This function identifies upstream dependency candidates.
    It does NOT claim statistical or experimental proof of causality.
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
        chain.insert(0, parent)
        current = parent

    return {
        "anomalous_service": anomalous_service,
        "event_time": anomalous_event_time,
        "causal_chain": chain,
        "candidate_root_cause": chain[0] if chain else None,
        "dependency_depth": max(len(chain) - 1, 0),
    }


def build_dependency_graph(trace_data=None):
    """
    Compatibility wrapper.

    If trace data is not supplied, load the project's sample trace.
    """

    if trace_data is None:
        return build_dependency_graph_from_file(DEFAULT_TRACE_FILE)

    return build_dependency_graph(trace_data)
