"""MCP Stdio Server for Levenshtein Fuzzy Tool Matcher.
100% Python Standard Library.
"""
import sys
import json
from client import LevenshteinFuzzyToolMatcher

matcher = LevenshteinFuzzyToolMatcher()

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-levenshtein-fuzzy-tool-matcher-skill", "version": "1.0.1"},
            "capabilities": {"tools": {}}
        }
        send_response(req_id, res)
    elif method == "tools/list":
        tools = [
            {
                "name": "find_best_match",
                "description": "Find closest tool signature for typo or hallucinated function name",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target": {"type": "string"},
                        "candidates": {"type": "array", "items": {"type": "string"}},
                        "min_similarity": {"type": "number", "default": 0.6}
                    },
                    "required": ["target", "candidates"]
                }
            },
            {
                "name": "compute_distance",
                "description": "Calculate Levenshtein distance and similarity score between two strings",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "str1": {"type": "string"},
                        "str2": {"type": "string"}
                    },
                    "required": ["str1", "str2"]
                }
            },
            {
                "name": "suggest_alternatives",
                "description": "Return ranked candidate tools with similarity scores",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target": {"type": "string"},
                        "candidates": {"type": "array", "items": {"type": "string"}},
                        "top_k": {"type": "integer", "default": 3}
                    },
                    "required": ["target", "candidates"]
                }
            }
        ]
        send_response(req_id, {"tools": tools})
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "find_best_match":
            out = matcher.find_best_match(args.get("target", ""), args.get("candidates", []), float(args.get("min_similarity", 0.6)))
        elif name == "compute_distance":
            dist, sim = matcher.compute_distance(args.get("str1", ""), args.get("str2", ""))
            out = {"edit_distance": dist, "similarity": sim}
        elif name == "suggest_alternatives":
            out = {"suggestions": matcher.suggest_alternatives(args.get("target", ""), args.get("candidates", []), int(args.get("top_k", 3)))}
        else:
            send_error(req_id, -32601, f"Unknown tool: {name}")
            return
        send_response(req_id, {"content": [{"type": "text", "text": json.dumps(out, indent=2)}]})

def send_response(req_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}) + "\n")
    sys.stdout.flush()

def send_error(req_id, code, message):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
