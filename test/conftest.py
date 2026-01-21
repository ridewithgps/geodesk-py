# Copyright (c) 2024 Clarisma / GeoDesk contributors
# SPDX-License-Identifier: LGPL-3.0-only

from geodesk import *
import pytest
import os

@pytest.fixture(scope="session")
def features():
    f = Features('d:\\geodesk\\tests\\de.gol')
    # f = Features('c:\\geodesk\\tests\\de3.gol')
    # f = Features('c:\\geodesk\\tests\\monaco.gol')
    yield f

@pytest.fixture(scope="session")
def monaco():
    """Monaco GOL - NO ID index (tests brute-force fallback)."""
    yield Features("test/data/monaco.gol")

@pytest.fixture(scope="session")
def monaco_indexed():
    """Monaco GOL - WITH ID index (tests O(1) lookup).

    Same dataset as monaco fixture but built with -i flag.
    """
    gol_path = "test/data/monaco-ids.gol"
    if not os.path.exists(gol_path):
        pytest.skip(f"monaco-ids.gol not available at {gol_path}")
    yield Features(gol_path)

@pytest.fixture(scope="session")
def monaco_updatable():
    yield Features("d:\\geodesk\\tests\\mcu")