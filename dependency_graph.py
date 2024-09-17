import re
from typing import List
import networkx as nx

view_files = [
    "./schemas/sales/views/customer_order_summary.sql",
    "./schemas/sales/views/product_sales_overview.sql",
    "./schemas/sales/views/customer_order_total_percentage.sql",
]

table_files = [
    "./schemas/sales/tables/customer.sql",
    "./schemas/sales/tables/product.sql",
    "./schemas/sales/tables/order.sql",
]


def get_table_name(sql: str) -> str:
    match = re.search(
        r"CREATE\W+(OR\W+REPLACE\W+)?TABLE\W+(?P<table_name>[a-zA-Z0-9_.]+)",
        sql,
    )
    return match.group("table_name") if match else None


def get_view_name(sql: str) -> str:
    match = re.search(
        r"CREATE\W+(OR\W+REPLACE\W+)?VIEW\W+(?P<view_name>[a-zA-Z0-9_.]+)", sql
    )
    return match.group("view_name") if match else None


def get_identifiers(sql: str) -> List[str]:
    matches = re.findall(r"@@[a-z.0-9_^@]+@@", sql)
    return [match.replace("@@", "") for match in matches]


def quote(text: str) -> str:
    return f'"{text}"'


color_map = {"table": "blue", "view": "red"}


def generate_dependency_graph(
    table_sql: List[str], view_sql: List[str]
) -> nx.DiGraph:
    table_names = [get_table_name(sql) for sql in table_sql]

    graph = nx.DiGraph()

    for sql in view_sql:
        view_name = get_view_name(sql)
        node_type = "table" if view_name in table_names else "view"
        graph.add_node(
            quote(view_name), type=node_type, color=color_map[node_type]
        )
        for identifier in get_identifiers(sql):
            node_type = "table" if identifier in table_names else "view"
            graph.add_node(
                quote(identifier), type=node_type, color=color_map[node_type]
            )
            graph.add_edge(quote(identifier), quote(view_name))

    return graph


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


if __name__ == "__main__":
    table_sql = [read_file(sql) for sql in table_files]
    view_sql = [read_file(sql) for sql in view_files]
    graph = generate_dependency_graph(table_sql, view_sql)
    nx.nx_pydot.to_pydot(graph).write_svg("./graph.svg")
    # Remove tables
    graph.remove_nodes_from(
        [node for node in graph.nodes if graph.nodes[node]["type"] == "table"]
    )
    print("Deployment order of views:")
    for view in nx.topological_sort(graph):
        print(view)
