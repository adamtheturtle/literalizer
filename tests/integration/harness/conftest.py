"""Isolated configuration inputs for golden harness tests."""

from argparse import Namespace

import pytest


@pytest.fixture(name="regeneration_config")
def fixture_regeneration_config(*, regenerate: bool) -> pytest.Config:
    """Configure regeneration without starting pytest plugins."""
    config = pytest.Config(pluginmanager=pytest.PytestPluginManager())
    config.option = Namespace(regen_all=regenerate)
    return config
