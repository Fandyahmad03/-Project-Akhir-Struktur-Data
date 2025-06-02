import time
from datastructures import Graph
from project.models.user import Content

risk_queue = []
spread_graph = Graph()

def analyze_content(content: Content, known_checksums: set) -> dict:
    is_duplicate = content.checksum in known_checksums
    is_anomaly = content.metadata.get("x-fake-score", 0) > 1.5

    result = {
        "duplicate": is_duplicate,
        "anomaly": is_anomaly,
        "final_score": 0,
        "is_flagged": False
    }

    if is_duplicate:
        result["final_score"] += 1
    if is_anomaly:
        result["final_score"] += 2

    result["is_flagged"] = result["final_score"] > 0

    if result["is_flagged"]:
        risk_queue.append({
            "timestamp": time.time(),
            "content": content,
            "duplicate": is_duplicate,
            "anomaly": is_anomaly,
            "final_score": result["final_score"]
        })

    return result

def get_high_risk_contents():
    return risk_queue

def record_spread(uploader, content):
    spread_graph.add_edge(uploader, content)  # ⬅️ Tambahkan object Content, bukan filename

def get_spread_map():
    return spread_graph.get_graph()
