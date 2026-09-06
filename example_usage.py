"""
Example usage of Temporal Knowledge Graph Event Triplet Skill.
"""

from client import TemporalKnowledgeGraph


def main():
    print("=== Temporal Knowledge Graph Event Triplet Demonstration ===")
    tkg = TemporalKnowledgeGraph()

    # Add historical entity facts across years (2020 - 2026)
    tkg.add_fact("Alice", "role", "Junior Engineer", valid_from=2020.0, valid_to=2022.0)
    tkg.add_fact("Alice", "role", "Senior Engineer", valid_from=2022.0, valid_to=2024.5)
    tkg.add_fact("Alice", "role", "Staff Architect", valid_from=2024.5, valid_to=None)
    tkg.add_fact("Alice", "works_at", "Alpha Corp", valid_from=2020.0, valid_to=2023.0)
    tkg.add_fact("Alice", "works_at", "GenPark Labs", valid_from=2023.0, valid_to=None)

    # 1. Point-in-time snapshot query: What was Alice's role in 2021?
    print("\n--- Query Point in Time: Year 2021.5 ---")
    facts_2021 = tkg.query_point_in_time(2021.5, subject="Alice")
    for f in facts_2021:
        print(f"  {f['subject']} -[{f['predicate']}]-> {f['object']} (from {f['valid_from']} to {f['valid_to']})")

    # 2. Point-in-time snapshot query: What is Alice's role in 2025?
    print("\n--- Query Point in Time: Year 2025.0 ---")
    facts_2025 = tkg.query_point_in_time(2025.0, subject="Alice")
    for f in facts_2025:
        print(f"  {f['subject']} -[{f['predicate']}]-> {f['object']} (from {f['valid_from']} to {f['valid_to']})")

    # 3. Subject timeline traversal
    print("\n--- Alice Complete Career Timeline ---")
    timeline = tkg.get_subject_timeline("Alice")
    for item in timeline:
        print(f"  [{item['valid_from']} - {item['valid_to']}] {item['subject']} {item['predicate']} {item['object']}")


if __name__ == "__main__":
    main()
