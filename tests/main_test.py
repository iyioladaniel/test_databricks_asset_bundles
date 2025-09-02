import os
import sys
import pytest

from test_databricks_asset_bundles.main import get_taxis, get_spark

@pytest.mark.skipif(
    os.getenv('CI') == 'true' or os.getenv('GITHUB_ACTIONS') == 'true',
    reason="Skipping Databricks Connect tests in CI environment"
)
def test_main():
    """Test the main function - only runs in local development"""
    taxis = get_taxis(get_spark())
    assert taxis.count() > 5


def test_placeholder():
    """Placeholder test that always passes in CI"""
    # This ensures CI doesn't fail when all other tests are skipped
    assert True
