"""
Temporal Knowledge Graph Event Triplet Skill Client
Pure Python Standard Library implementation of a Temporal Knowledge Graph (TKG).
Stores (subject, predicate, object, valid_from, valid_to) facts and enables
point-in-time state reconstruction, interval overlap queries, and chronological history traversal.
"""

from typing import List, Dict, Any, Optional, Tuple


class TemporalKnowledgeGraph:
    """
    Temporal Knowledge Graph with interval-based validity indexing.
    Timestamps are represented as ISO strings or integers.
    """

    def __init__(self):
        self.triplets: List[Dict[str, Any]] = []

    def add_fact(
        self,
        subject: str,
        predicate: str,
        obj: str,
        valid_from: float,
        valid_to: Optional[float] = None,
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Insert a temporal triplet into the graph.
        :param valid_to: None represents indefinitely valid into the future.
        """
        fact = {
            "id": len(self.triplets),
            "subject": subject.strip(),
            "predicate": predicate.strip(),
            "object": obj.strip(),
            "valid_from": float(valid_from),
            "valid_to": float(valid_to) if valid_to is not None else float("inf"),
            "confidence": float(confidence),
            "metadata": metadata or {}
        }
        self.triplets.append(fact)
        return fact

    def query_point_in_time(self, timestamp: float, subject: Optional[str] = None, predicate: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Query all facts that were valid at a specific historical point in time.
        valid_from <= timestamp <= valid_to
        """
        ts = float(timestamp)
        results = []
        for t in self.triplets:
            if t["valid_from"] <= ts <= t["valid_to"]:
                if subject and t["subject"].lower() != subject.lower():
                    continue
                if predicate and t["predicate"].lower() != predicate.lower():
                    continue
                results.append(t)
        return results

    def query_interval_overlap(self, start_time: float, end_time: float, subject: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Query facts whose validity intervals overlap with [start_time, end_time].
        Overlap occurs iff: max(t.valid_from, start_time) <= min(t.valid_to, end_time)
        """
        results = []
        for t in self.triplets:
            if max(t["valid_from"], start_time) <= min(t["valid_to"], end_time):
                if subject and t["subject"].lower() != subject.lower():
                    continue
                results.append(t)
        return results

    def get_subject_timeline(self, subject: str) -> List[Dict[str, Any]]:
        """Retrieve chronological history of all facts relating to a subject."""
        sub_facts = [t for t in self.triplets if t["subject"].lower() == subject.lower() or t["object"].lower() == subject.lower()]
        return sorted(sub_facts, key=lambda x: x["valid_from"])
