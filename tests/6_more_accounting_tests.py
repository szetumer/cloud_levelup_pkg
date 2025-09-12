import pytest
import json
from src.cloud_levelup.azure_costing import rgq_from_rgs, rgs_minimal, output_json_file, rgs_summarize_types
from src.cloud_levelup.command_files import Config, GetAzure
from src.cloud_levelup.parameters import rgraph_config_filepath

QUERIES_TO_RUN : list[int] = Config(rgraph_config_filepath).configs["tests_to_run"]

@pytest.fixture(scope="session")
def rgraph_configs():
    config : Config = Config(rgraph_config_filepath)
    return config.configs

class TestLearningKQL:
    @pytest.mark.skipif(0 not in QUERIES_TO_RUN, reason="skipped to avoid throttling")
    def test0_resource_graph_query(self):
        result = rgq_from_rgs(rgs_minimal())
        output_json_file(result, "query0.json")
        assert(True)

    @pytest.mark.skipif(1 not in QUERIES_TO_RUN, reason="skipped to avoid throttling")
    def test1_resource_graph_query1(self, rgraph_configs):
        result = rgq_from_rgs(rgraph_configs["query1"])
        output_json_file(result, "query1_anything.json")
        assert(isinstance(result, dict) or isinstance(result, list))
        assert("count" in result.keys())

    @pytest.mark.skipif(2 not in QUERIES_TO_RUN, reason="skipped to avoid throttling")
    def test2_summarize_resource_types(self, rgraph_configs):
        result = rgq_from_rgs(rgs_summarize_types())
        output_json_file(result, "query2_resource_types.json")
        assert(isinstance(result, dict) or isinstance(result, list))
        assert("count" in result.keys())

    @pytest.mark.skipif(3 not in QUERIES_TO_RUN, reason="skipped to avoid throttling")
    def test3_resource_query3_for_getting_workspace_list(self, rgraph_configs):
        if rgraph_configs["query3"] is None:
            pytest.fail("no query entered for query3")
        result1 = rgq_from_rgs(rgraph_configs["query3"])
        assert(isinstance(result1, dict))
        output_json_file(result1, "query3_workspace_attrs.json")
        json_of_all_resources : list[dict] = GetAzure._json("az", "group", "list", "--output", "json")
        rg_names : list[str] = [d["name"] for d in json_of_all_resources]
        workspace_sum : int = 0
        print("CAPTURED RESOURCEGROUP:")
        for rg_name in rg_names:
            print(rg_name)
            print("\tworkspaces:")
            workspaces_in_resourcegroup : list[dict] = GetAzure._json("az", "databricks", "workspace", "list", "--resource-group", rg_name, "--output", "json")
            for ws in workspaces_in_resourcegroup:
                print(f"\t\t{ws["name"]}")
            workspace_sum = workspace_sum + len(workspaces_in_resourcegroup)
        assert(int(result1["count"]) == workspace_sum)

    @pytest.mark.skipif(4 not in QUERIES_TO_RUN, reason="skipped to avoid throttling")
    def test4_select_columns(self, rgraph_configs):
        if rgraph_configs["query4"] is None:
            pytest.fail("query4 is None. Please either disable this test or provide a resource graph query")
        result : dict = rgq_from_rgs(rgraph_configs["query4"])
        if not isinstance(result, dict):
            pytest.fail("query4 does not work well. Please either disable this test or provide a query")
        output_json_file(result, "query4_column_selection.json")
        assert(isinstance(result, dict) or isinstance(result, list))
        if result["count"] == 0:
            pytest.fail("query4 does not return anything")
        for workspace_attrs in result["data"]:
            assert("id" in workspace_attrs.keys())
            assert("name" in workspace_attrs.keys())
            assert("properties_parameters" in workspace_attrs.keys())
            assert(isinstance(workspace_attrs["properties_parameters"], dict))

class TestLearningAboutNatGateways:
    def test5_not_implemented(self):
        assert(True)

    @pytest.mark.skipif(6 not in QUERIES_TO_RUN, reason="skipped to avoid throttling")
    def test6_understanding_NAT_gateways(self, rgraph_configs):
        q : str = rgraph_configs["query6"]
        assert(q is not None)
        result : dict = rgq_from_rgs(q)
        assert(isinstance(result, dict))
        output_json_file(result, "query6_natgateways.json")
        if result["count"] == 0:
            pytest.skip("you don't have any NAT gateways to delete.")
            return
        data : list[dict] = result["data"]
        for ngateway in data:
            assert("id" in ngateway.keys())
            assert("name" in ngateway.keys())
            assert("subscriptions" in ngateway["id"])
            assert("tags" in ngateway.keys())
            assert("subnets" in ngateway.keys())
            assert("public_ip_addresses" in ngateway.keys())
            assert("id" in ngateway["subnets"][0])
            assert(len(ngateway.keys()) >= 5)
    
    @pytest.mark.skipif(7 not in QUERIES_TO_RUN, reason = "skipped to avoid throttling")
    def test7_virtualmachines(self, rgraph_configs):
        q : str = rgraph_configs["query7"]
        assert(q is not None)
        result : dict = rgq_from_rgs(q)
        assert(isinstance(result, dict))
        output_json_file(result, "query7_virtualmachines.json")
        if result["count"] == 0:
            pytest.skip("you don't have any NAT gateways associated with databricks..")
            return
        data : list[dict] = result["data"]
        assert(True)

    @pytest.mark.skipif(8 not in QUERIES_TO_RUN, reason = "skipped to avoid throttling")
    def test8_networkinterfaces(self, rgraph_configs):
        q : str = rgraph_configs["query8"]
        assert(q is not None)
        result : dict = rgq_from_rgs(q)
        assert(isinstance(result, dict))
        output_json_file(result, "query8_networkinterfaces.json")
        data : list[dict] = result["data"]
        assert(True)

    @pytest.mark.skipif(9 not in QUERIES_TO_RUN, reason = "skipped to avoid throttling")
    def test9(self, rgraph_configs):
        q : str = rgraph_configs["query9"]
        assert(q is not None)
        result : dict = rgq_from_rgs(q)
        assert(isinstance(result, dict))
        output_json_file(result, "query9_linkingthemtogether.json")
        if result["count"] == 0:
            pytest.skip("you don't have any NAT gateways associated with databricks..")
            return
        data : list[dict] = result["data"]
        assert(True)