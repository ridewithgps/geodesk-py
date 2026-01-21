#!/usr/bin/env python3
"""
Standalone test script to verify ID lookup works correctly.
Run with: uv run scripts/test_id_lookup.py <path-to-gol>

Tests both indexed (O(1)) and brute-force paths depending on GOL file.
"""
import sys
import time
import os
from geodesk import Features

# Known IDs from Monaco dataset
MONACO_IDS = {
    'node': 4416197078,
    'way': 626967072,
    'relation': 2214022,
}

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/test_id_lookup.py <gol-file> [node_id] [way_id] [relation_id]")
        print()
        print("Examples:")
        print("  uv run scripts/test_id_lookup.py data/monaco.gol           # brute-force")
        print("  uv run scripts/test_id_lookup.py data/monaco-ids.gol       # O(1) indexed")
        print("  uv run scripts/test_id_lookup.py data/monaco.gol 4416197078 626967072 2214022")
        sys.exit(1)

    gol_path = sys.argv[1]

    if not os.path.exists(gol_path):
        print(f"Error: GOL file not found: {gol_path}")
        sys.exit(1)

    print(f"Loading: {gol_path}")
    features = Features(gol_path)
    print(f"✓ GOL loaded successfully")

    # Check for ID index by looking for index directory
    base_name = gol_path.replace('.gol', '')
    index_dir = base_name + '-indexes'
    has_index = os.path.isdir(index_dir)
    if has_index:
        print(f"✓ ID index detected: {index_dir}")
        print("  → Expecting O(1) lookup performance")
    else:
        print(f"⚠ No ID index found (looked for {index_dir})")
        print("  → Using brute-force fallback (slower)")

    # Get test IDs - from args, or use Monaco defaults
    if len(sys.argv) > 2:
        node_id = int(sys.argv[2])
        way_id = int(sys.argv[3]) if len(sys.argv) > 3 else None
        rel_id = int(sys.argv[4]) if len(sys.argv) > 4 else None
    else:
        # Use Monaco defaults
        node_id = MONACO_IDS['node']
        way_id = MONACO_IDS['way']
        rel_id = MONACO_IDS['relation']
        print(f"\n--- Using Monaco default IDs ---")
        print(f"  node: {node_id}, way: {way_id}, relation: {rel_id}")

    # Test basic functionality
    print("\n--- Basic Functionality Tests ---")

    if node_id:
        start = time.perf_counter()
        node = features.node(node_id)
        node_time = (time.perf_counter() - start) * 1000
        if node:
            tags = dict(list(node.tags)[:3])  # First 3 tags
            print(f"✓ node({node_id}): found in {node_time:.3f}ms - {tags}")
        else:
            print(f"✗ node({node_id}): not found ({node_time:.3f}ms)")

    if way_id:
        start = time.perf_counter()
        way = features.way(way_id)
        way_time = (time.perf_counter() - start) * 1000
        if way:
            tags = dict(list(way.tags)[:3])
            print(f"✓ way({way_id}): found in {way_time:.3f}ms - {tags}")
        else:
            print(f"✗ way({way_id}): not found ({way_time:.3f}ms)")

    if rel_id:
        start = time.perf_counter()
        rel = features.relation(rel_id)
        rel_time = (time.perf_counter() - start) * 1000
        if rel:
            tags = dict(list(rel.tags)[:3])
            print(f"✓ relation({rel_id}): found in {rel_time:.3f}ms - {tags}")
        else:
            print(f"✗ relation({rel_id}): not found ({rel_time:.3f}ms)")

    # Performance benchmark
    iterations = 1000 if has_index else 10  # Fewer iterations for brute-force
    print(f"\n--- Performance Benchmark ({iterations} iterations) ---")

    for name, lookup_fn, fid in [
        ("node", features.node, node_id),
        ("way", features.way, way_id),
        ("relation", features.relation, rel_id),
    ]:
        if fid is None:
            continue
        start = time.perf_counter()
        for _ in range(iterations):
            lookup_fn(fid)
        elapsed = (time.perf_counter() - start) * 1000
        avg = elapsed / iterations
        print(f"{name}({fid}): {elapsed:.2f}ms total, {avg:.3f}ms avg per lookup")

    # Test not-found performance
    not_found_iterations = 1000 if has_index else 50
    print(f"\n--- Not-Found Performance ({not_found_iterations} iterations) ---")
    start = time.perf_counter()
    for fake_id in range(1, not_found_iterations + 1):
        features.node(fake_id)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{not_found_iterations} not-found node lookups: {elapsed:.2f}ms ({elapsed/not_found_iterations:.3f}ms avg)")

    # Summary
    print("\n--- Summary ---")
    if has_index:
        print("✓ Using O(1) indexed lookup")
        print("  Expected: < 1ms per lookup")
    else:
        print("⚠ Using brute-force fallback")
        print("  Expected: Variable (depends on dataset size)")

    print("\n✓ All tests completed!")

if __name__ == "__main__":
    main()
