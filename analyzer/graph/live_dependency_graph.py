import requests
import networkx as nx


JAEGER_URL = "http://localhost:16686"


def get_traces(service="checkout", limit=50):
    url = f"{JAEGER_URL}/api/traces"
    params = {
        "service": service,
        "limit": limit,
        "lookback": "1h"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


def get_service_map(trace):
    service_map = {}

    for process in trace.get("processes", {}).items():
        process_id, process_data = process
        service_name = process_data.get("serviceName")

        if service_name:
            service_map[process_id] = service_name

    return service_map


def find_complete_trace(trace_data):
    for trace in trace_data.get("data", []):
        services = set(get_service_map(trace).values())

        if {
            "checkout",
            "inventory",
            "payment"
        }.issubset(services):
            return trace

    return None


def build_dependency_graph(trace):
    graph = nx.DiGraph()

    service_map = get_service_map(trace)

    spans = trace.get("spans", [])

    span_service = {}

    for span in spans:
        service = service_map.get(span.get("processID"))

        if service:
            span_service[span.get("spanID")] = service
            graph.add_node(service)

    for span in spans:
        child_service = span_service.get(span.get("spanID"))

        if not child_service:
            continue

        for reference in span.get("references", []):
            if reference.get("refType") != "CHILD_OF":
                continue

            parent_span_id = reference.get("spanID")
            parent_service = span_service.get(parent_span_id)

            if (
                parent_service
                and parent_service != child_service
            ):
                graph.add_edge(
                    parent_service,
                    child_service
                )

    return graph


def print_graph(graph):
    print()
    print("LIVE DEPENDENCY GRAPH")
    print("=====================")

    print()
    print("Services:")

    for node in sorted(graph.nodes):
        print(f"  {node}")

    print()
    print("Dependencies:")

    if graph.number_of_edges() == 0:
        print("  No cross-service dependencies detected")
    else:
        for source, target in sorted(graph.edges):
            print(f"  {source} -> {target}")

    print()
    print("Graph nodes:", graph.number_of_nodes())
    print("Graph edges:", graph.number_of_edges())


if __name__ == "__main__":

    print("Fetching traces from Jaeger...")

    trace_data = get_traces()

    print(
        "Traces received:",
        len(trace_data.get("data", []))
    )

    trace = find_complete_trace(trace_data)

    if trace is None:
        print()
        print("ERROR: No complete checkout -> inventory -> payment trace found.")
        raise SystemExit(1)

    print()
    print("Complete trace found:")
    print(trace.get("traceID"))

    graph = build_dependency_graph(trace)

    print_graph(graph)

    print()
    print("TRACE SPANS")
    print("===========")

    service_map = get_service_map(trace)

    for span in trace.get("spans", []):

        service = service_map.get(
            span.get("processID"),
            "unknown"
        )

        print(
            f"{service:<12} "
            f"{span.get('operationName'):<35} "
            f"{span.get('spanID')}"
        )
