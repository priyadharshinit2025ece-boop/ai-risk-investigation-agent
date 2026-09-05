import pandas as pd
import networkx as nx
from pathlib import Path


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

INPUT_FILE = Path("data/processed/response_results.csv")

NODES_FILE = Path("data/processed/risk_graph_nodes.csv")
EDGES_FILE = Path("data/processed/risk_graph_edges.csv")
CLUSTERS_FILE = Path("data/processed/risk_clusters.csv")


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print(f"Loaded {len(df)} transactions")


# ---------------------------------------------------------
# Select suspicious events
# ---------------------------------------------------------

suspicious = df[
    (df["overall_risk_score"] >= 50)
    | (df["early_warning"] == 1)
].copy()

print(f"Suspicious events selected: {len(suspicious)}")


# ---------------------------------------------------------
# Create graph
# ---------------------------------------------------------

G = nx.Graph()


def add_node(node_id, node_type, value):
    """Add a typed node to the graph."""

    if node_id not in G:
        G.add_node(
            node_id,
            node_type=node_type,
            value=str(value)
        )


def add_relationship(source, target, relationship):
    """Add relationship between two entities."""

    if G.has_edge(source, target):
        G[source][target]["weight"] += 1
    else:
        G.add_edge(
            source,
            target,
            relationship=relationship,
            weight=1
        )


# ---------------------------------------------------------
# Build relationships
# ---------------------------------------------------------

for _, row in suspicious.iterrows():

    user = str(row["user_id"])
    device = str(row["device_id"])
    ip = str(row["ip_address"])
    payment = str(row["payment_identifier"])
    merchant = str(row["merchant_id"])

    # Typed node IDs
    user_node = f"user:{user}"
    device_node = f"device:{device}"
    ip_node = f"ip:{ip}"
    payment_node = f"payment:{payment}"
    merchant_node = f"merchant:{merchant}"

    # Add nodes
    add_node(user_node, "USER", user)
    add_node(device_node, "DEVICE", device)
    add_node(ip_node, "IP", ip)
    add_node(payment_node, "PAYMENT_IDENTIFIER", payment)
    add_node(merchant_node, "MERCHANT", merchant)

    # Add relationships
    add_relationship(
        user_node,
        device_node,
        "USES_DEVICE"
    )

    add_relationship(
        user_node,
        ip_node,
        "USES_IP"
    )

    add_relationship(
        user_node,
        payment_node,
        "USES_PAYMENT_IDENTIFIER"
    )

    add_relationship(
        user_node,
        merchant_node,
        "TRANSACTS_WITH"
    )


# ---------------------------------------------------------
# Export graph nodes
# ---------------------------------------------------------

node_records = []

for node_id, attributes in G.nodes(data=True):

    node_records.append({
        "node_id": node_id,
        "node_type": attributes.get("node_type"),
        "value": attributes.get("value")
    })


nodes_df = pd.DataFrame(node_records)

nodes_df.to_csv(
    NODES_FILE,
    index=False
)


# ---------------------------------------------------------
# Export graph edges
# ---------------------------------------------------------

edge_records = []

for source, target, attributes in G.edges(data=True):

    edge_records.append({
        "source": source,
        "target": target,
        "relationship": attributes.get("relationship"),
        "weight": attributes.get("weight", 1)
    })


edges_df = pd.DataFrame(edge_records)

edges_df.to_csv(
    EDGES_FILE,
    index=False
)


# ---------------------------------------------------------
# Identify connected clusters
# ---------------------------------------------------------

clusters = []

components = list(nx.connected_components(G))

print(f"Connected clusters found: {len(components)}")


for cluster_number, component in enumerate(
    components,
    start=1
):

    cluster_nodes = G.subgraph(component)

    users = [
        node for node in component
        if node.startswith("user:")
    ]

    devices = [
        node for node in component
        if node.startswith("device:")
    ]

    ips = [
        node for node in component
        if node.startswith("ip:")
    ]

    payments = [
        node for node in component
        if node.startswith("payment:")
    ]

    merchants = [
        node for node in component
        if node.startswith("merchant:")
    ]

    # Find transactions belonging to this cluster
    cluster_users = {
        node.replace("user:", "")
        for node in users
    }

    cluster_events = suspicious[
        suspicious["user_id"]
        .astype(str)
        .isin(cluster_users)
    ]

    if len(cluster_events) > 0:

        max_risk = cluster_events[
            "overall_risk_score"
        ].max()

        avg_risk = cluster_events[
            "overall_risk_score"
        ].mean()

        early_warnings = cluster_events[
            "early_warning"
        ].sum()

    else:

        max_risk = 0
        avg_risk = 0
        early_warnings = 0


    # -----------------------------------------------------
    # Cluster risk level
    # -----------------------------------------------------

    if max_risk >= 80 and len(users) >= 2:

        cluster_risk = "CRITICAL"

    elif max_risk >= 60 and (
        len(users) >= 2
        or len(devices) >= 2
        or len(ips) >= 2
    ):

        cluster_risk = "HIGH"

    elif max_risk >= 50:

        cluster_risk = "MEDIUM"

    else:

        cluster_risk = "LOW"


    # -----------------------------------------------------
    # Explanation
    # -----------------------------------------------------

    explanation = (
        f"{len(users)} user(s) connected through "
        f"{len(devices)} device(s), "
        f"{len(ips)} IP(s), "
        f"{len(payments)} payment identifier(s), "
        f"and {len(merchants)} merchant(s). "
        f"{len(cluster_events)} suspicious event(s) detected."
    )


    clusters.append({

        "cluster_id":
            f"CLUSTER_{cluster_number}",

        "node_count":
            len(component),

        "unique_users":
            len(users),

        "unique_devices":
            len(devices),

        "unique_ips":
            len(ips),

        "unique_payment_identifiers":
            len(payments),

        "unique_merchants":
            len(merchants),

        "risky_event_count":
            len(cluster_events),

        "max_risk_score":
            round(float(max_risk), 2),

        "average_risk_score":
            round(float(avg_risk), 2),

        "early_warning_count":
            int(early_warnings),

        "cluster_risk_level":
            cluster_risk,

        "explanation":
            explanation
    })


# ---------------------------------------------------------
# Save clusters
# ---------------------------------------------------------

clusters_df = pd.DataFrame(clusters)

clusters_df = clusters_df.sort_values(
    by=[
        "max_risk_score",
        "risky_event_count"
    ],
    ascending=False
)

clusters_df.to_csv(
    CLUSTERS_FILE,
    index=False
)


# ---------------------------------------------------------
# Final output
# ---------------------------------------------------------

print("\n====================================")
print("RISK GRAPH ANALYSIS COMPLETE")
print("====================================")

print(f"Nodes saved: {NODES_FILE}")
print(f"Edges saved: {EDGES_FILE}")
print(f"Clusters saved: {CLUSTERS_FILE}")

print("\nTop connected risk clusters:")

print(
    clusters_df.head(10).to_string(index=False)
)