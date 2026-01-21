#!/usr/bin/env python3
"""
Generic feature lookup script.
Usage: uv run scripts/lookup.py <gol-file> <type> <id>

Examples:
  uv run scripts/lookup.py data/monaco.gol node 4416197078
  uv run scripts/lookup.py data/monaco.gol way 626967072
  uv run scripts/lookup.py data/monaco.gol relation 2214022
"""
import argparse
from time import perf_counter

t_import_start = perf_counter()
from geodesk import Features
t_import = perf_counter() - t_import_start


def main():
    parser = argparse.ArgumentParser(
        description="Look up an OSM feature by type and ID"
    )
    parser.add_argument("gol", help="Path to the GOL file")
    parser.add_argument(
        "type",
        choices=["node", "way", "relation"],
        help="Feature type: node, way, or relation"
    )
    parser.add_argument("id", type=int, help="Feature ID")

    args = parser.parse_args()

    t_open_start = perf_counter()
    features = Features(args.gol)
    t_open = perf_counter() - t_open_start

    # Look up by type
    lookup = {"node": features.node, "way": features.way, "relation": features.relation}

    t_lookup_start = perf_counter()
    feature = lookup[args.type](args.id)
    t_lookup = perf_counter() - t_lookup_start

    if feature is None:
        print(f"{args.type}({args.id}): not found")
        return 1

    t_tags_start = perf_counter()
    tags = list(feature.tags)
    t_tags = perf_counter() - t_tags_start

    print(f"{args.type}({args.id}):")
    for key, value in tags:
        print(f"  {key} = {value}")

    print(f"\n--- Timing ---")
    print(f"import geodesk: {t_import*1000:7.2f} ms")
    print(f"open GOL file:  {t_open*1000:7.2f} ms")
    print(f"lookup by ID:   {t_lookup*1000:7.2f} ms")
    print(f"read tags:      {t_tags*1000:7.2f} ms")

    return 0


if __name__ == "__main__":
    exit(main())
