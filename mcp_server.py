"""
MCP Server for Temporal Knowledge Graph Event Triplet Skill.
"""

import json
import sys
from client import TemporalKnowledgeGraph

TKG = TemporalKnowledgeGraph()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "add_temporal_fact",
                    "description": "Insert a temporal fact triplet into the knowledge graph",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "subject": {"type": "string"},
                            "predicate": {"type": "string"},
                            "object": {"type": "string"},
                            "valid_from": {"type": "number"},
                            "valid_to": {"type": "number"},
                            "confidence": {"type": "number", "default": 1.0}
                        },
                        "required": ["subject", "predicate", "object", "valid_from"]
                    }
                },
                {
                    "name": "query_point_in_time",
                    "description": "Query facts valid at a specific point in time",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "timestamp": {"type": "number"},
                            "subject": {"type": "string"},
                            "predicate": {"type": "string"}
                        },
                        "required": ["timestamp"]
                    }
                },
                {
                    "name": "get_subject_timeline",
                    "description": "Retrieve chronological history for an entity",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "subject": {"type": "string"}
                        },
                        "required": ["subject"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "add_temporal_fact":
            fact = TKG.add_fact(
                args["subject"],
                args["predicate"],
                args["object"],
                args["valid_from"],
                args.get("valid_to"),
                args.get("confidence", 1.0)
            )
            return {"content": [{"type": "text", "text": json.dumps(fact)}]}

        elif tool_name == "query_point_in_time":
            res = TKG.query_point_in_time(
                args["timestamp"],
                args.get("subject"),
                args.get("predicate")
            )
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        elif tool_name == "get_subject_timeline":
            res = TKG.get_subject_timeline(args["subject"])
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
