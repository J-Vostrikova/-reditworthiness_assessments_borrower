def test_response_time():
    """Критерий качества: время отклика <500мс"""
    start = time.time()
    response = requests.post(API_URL, json=test_data)
    assert (time.time() - start) < 0.5  # 500 мс

def test_error_handling():
    """Критерий: обработка ошибок"""
    response = invalid_request()
    assert "error" in response.json()