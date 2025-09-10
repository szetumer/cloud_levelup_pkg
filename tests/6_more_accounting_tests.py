import pytest
from src.cloud_levelup.azure_costing import _rgs_query, _rgs_minimal, _output_json_file, _rgs_return5
from src.cloud_levelup.command_files import Config
from src.cloud_levelup.parameters import rgraph_config_filepath

QUERIES_TO_RUN : list[int] = Config(rgraph_config_filepath).configs["tests_to_run"]

@pytest.fixture(scope="session")
def rgraph_configs():
    config : Config = Config(rgraph_config_filepath)
    return config.configs

@pytest.mark.skipif(0 not in QUERIES_TO_RUN, reason="skipped to avoid throttling")
def test0_resource_graph_query():
    result = _rgs_query(_rgs_minimal())
    _output_json_file(result, "query0.json")
    assert(True)

@pytest.mark.skipif(1 not in QUERIES_TO_RUN, reason="skipped to avoid throttling")
def test_resource_graph_query2(rgraph_configs):
    result = _rgs_query(rgraph_configs["query1"])
    _output_json_file(result, "query1.json")
    assert(isinstance(result, dict) or isinstance(result, list))
    assert("count" in result.keys())