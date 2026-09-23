import json
import networkx as nx


def _service_name(process):
    if not isinstance(process, dict):
        return None

    return (
        process.get("serviceName")
        or process.get("service_name")
        or process.get("tags", {}).get("service.name")
    )


def build_dependency_graph(trace_data):
    graph = nx.DiGraph()

    traces = trace_data.get("data", []) if isinstance(trace_data, dict) else []

    for trace in traces:
        processes = trace.get("processes", {}) or {}
        spans = trace.get("spans", []) or []

        # Map Jaeger process IDs to service names.
        process_services = {}

        for process_id, process in processes.items():
            service = _service_name(process)

            if service:
                process_services[process_id] = service
                graph.add_node(service)

        # Map span IDs to their service.
        span_service = {}

        for span in spans:
            span_id = span.get("spanID")
            process_id = span.get("processID")

            service = process_services.get(process_id)

            if span_id and service:
                span_service[span_id] = service

        # Build dependencies using parent/child references.
        for span in spans:
            child_span_id = span.get("spanID")
            child_service = span_service.get(child_span_id)

            if not child_service:
                continue

            references = span.get("references", []) or []

            for reference in references:
                if reference.get("refType") not in (None, "CHILD_OF", "FOLLOWS_FROM"):
                    continue

                parent_span_id = reference.get("spanID")
                parent_service = span_service.get(parent_span_id)

                if (
                    parent_service
                    and child_service
                    and parent_service != child_service
                ):
                    graph.add_edge(parent_service, child_service)

    return graph


def build_dependency_graph_from_file(path):
    with open(path, "r", encoding="utf-8") as file:
        trace_data = json.load(file)

    return build_dependency_graph(trace_data)


def print_graph(graph):
    print("\nDEPENDENCY GRAPH")
    print("================")

    print("\nServices:")

    for node in sorted(graph.nodes):
        print(f"  {node}")

    print("\nDependencies:")

    for source, target in sorted(graph.edges):
        print(f"  {source} -> {target}")

    print("\nGraph nodes:", graph.number_of_nodes())
    print("Graph edges:", graph.number_of_edges())


if __name__ == "__main__":
    graph = build_dependency_graph_from_file(
        "data/sample-trace.json"
    )

    print_graph(graph)
