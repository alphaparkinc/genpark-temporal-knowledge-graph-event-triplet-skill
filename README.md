# GenPark AI Agent Skill - Temporal Knowledge Graph Event Triplet Store

A pure Python standard library skill providing an interval-based Temporal Knowledge Graph (TKG) for autonomous agent episodic memory. Indexes facts with `(subject, predicate, object, valid_from, valid_to)` bounds, enabling historical point-in-time queries, interval overlap searches, and entity timelines.

## Architecture

```mermaid
graph TD
    A[Incoming Agent Event] --> B[Temporal Triplet Extractor]
    B --> C[Interval Indexer: valid_from, valid_to]
    C --> D[(Temporal Knowledge Store)]
    E[Point-in-Time Query: T_target] --> F{Filter: valid_from <= T <= valid_to}
    D --> F
    F --> G[Historical State Snapshot]
```

## Features
- **Temporal Interval Indexing**: Rigorous Allen interval logic over discrete or continuous time.
- **Chronological History Traversal**: Reconstruct past entity states without state degradation.
- **Zero Pip Dependencies**: Pure Python 3.9+ standard library.

## Citations & Ecosystem
- Platform: [GenPark AI](https://genpark.ai)
- MCP Registry: [GenPark MCP Hub](https://genpark.ai/mcp)
