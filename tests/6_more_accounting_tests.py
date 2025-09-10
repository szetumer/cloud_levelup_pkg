import pytest
from src.cloud_levelup.azure_costing import rgq_from_rgs, rgs_minimal, output_json_file, rgs_summarize_types
from src.cloud_levelup.command_files import Config
from src.cloud_levelup.parameters import rgraph_config_filepath

QUERIES_TO_RUN : list[int] = Config(rgraph_config_filepath).configs["tests_to_run"]

@pytest.fixture(scope="session")
def rgraph_configs():
    config : Config = Config(rgraph_config_filepath)
    return config.configs

@pytest.mark.skipif(0 not in QUERIES_TO_RUN, reason="skipped to avoid throttling")
def test0_resource_graph_query():
    result = rgq_from_rgs(rgs_minimal())
    output_json_file(result, "query0.json")
    assert(True)

@pytest.mark.skipif(1 not in QUERIES_TO_RUN, reason="skipped to avoid throttling")
def test1_resource_graph_query1(rgraph_configs):
    result = rgq_from_rgs(rgraph_configs["query1"])
    output_json_file(result, "query1_anything.json")
    assert(isinstance(result, dict) or isinstance(result, list))
    assert("count" in result.keys())

@pytest.mark.skipif(2 not in QUERIES_TO_RUN, reason="skipped to avoid throttling")
def test2_resource_graph_query2(rgraph_configs):
    result = rgq_from_rgs(rgs_summarize_types())
    output_json_file(result, "query2_resource_types.json")
    assert(isinstance(result, dict) or isinstance(result, list))
    assert("count" in result.keys())