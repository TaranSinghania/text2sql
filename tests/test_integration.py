import json
import pytest

def test_complex_order_query(client):
    """
    Test a complex natural language query involving joins and conditions.
    Example query: "Show me all orders joined with customer and product where
    product name is 'Gadget X' and customer city is 'Los Angeles' after 2025-01-01."
    """
    payload = {
        "user_id": "test_user_1",
        "query": ("Show me all orders joined with customer and product "
                  "where product name is 'Gadget X' and customer city is 'Los Angeles' after 2025-01-01"),
        "execute_sql": True,
        "read_only": False
    }
    response = client.post("/query", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert "sql" in data and data["sql"] is not None
    assert "result" in data and len(data["result"]) != 0
    assert "schema" in data and len(data["schema"]) != 0
    if data["result"]:
        assert isinstance(data["schema"], list)

def test_query_then_refine(client):
    """
    First, submit an initial query to establish conversation context, then refine it.
    """
    user_id = "test_user_2"
    # Initial query
    payload_query = {
        "user_id": user_id,
        "query": "Find all customers from New York with age over 25",
        "execute_sql": True,
        "read_only": False
    }
    response_query = client.post("/query", data=json.dumps(payload_query), content_type="application/json")
    assert response_query.status_code == 200
    data_query = response_query.get_json()
    assert "sql" in data_query

    # Refinement query
    payload_refine = {
        "user_id": user_id,
        "feedback": "Only include customers whose last name starts with 'J'",
        "execute_sql": True,
        "read_only": False
    }
    response_refine = client.post("/refine", data=json.dumps(payload_refine), content_type="application/json")
    assert response_refine.status_code == 200
    data_refine = response_refine.get_json()
    assert "sql" in data_refine and data_refine["sql"] is not None
    assert "result" in data_refine and len(data_refine["result"]) != 0
    assert "schema" in data_refine and len(data_refine["schema"]) != 0
    # Check that the refined SQL is different from the initial SQL.
    assert data_refine["sql"] != data_query["sql"]

def test_destructive_query_readonly(client):
    """
    Test that a destructive query is blocked when read_only mode is enabled.
    """
    payload = {
        "user_id": "test_user_3",
        "query": "Drop the orders table",
        "execute_sql": True,
        "read_only": True
    }
    response = client.post("/query", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    # We expect an error because destructive operations should be blocked.
    assert "error" in data
    assert "DROP" in data["error"].upper() or "destructive" in data["error"].lower()

@pytest.mark.parametrize("query_text", [
    "Find all customers older than 35",
    "Get me the total quantity of orders for Widget B",
    "What is the average price of products in the Gadgets category",
])
def test_multiple_complex_queries(client, query_text):
    """
    Parametrized test for several complex natural language queries in read-only mode.
    """
    payload = {
        "user_id": "test_user_4",
        "query": query_text,
        "execute_sql": True,
        "read_only": True
    }
    response = client.post("/query", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert "sql" in data
    if "error" not in data:
        assert "result" in data and len(data["result"]) != 0
        assert "schema" in data and len(data["schema"]) != 0
