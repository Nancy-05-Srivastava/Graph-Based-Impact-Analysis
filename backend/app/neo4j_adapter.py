class Neo4jAdapter:
    """Optional persistence adapter. The default demo uses NetworkX."""

    def __init__(self, uri: str, user: str = "neo4j", password: str = "change-me"):
        try:
            from neo4j import GraphDatabase
        except ImportError as exc:
            raise RuntimeError(
                "Install the optional Neo4j dependency first."
            ) from exc
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def upsert_graph(self, graph_json: dict):
        query = """
        MERGE (n:FRDGNode {id: $id})
        SET n.label=$label, n.type=$type, n.risk=$risk
        """
        with self.driver.session() as session:
            for node in graph_json["nodes"]:
                session.run(query, **node)
