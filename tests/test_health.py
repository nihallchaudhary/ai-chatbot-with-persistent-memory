from health import get_health_status


def test_health_status():
    result = get_health_status()

    assert result["status"] == "healthy"
    assert "service" in result
    assert "timestamp" in result