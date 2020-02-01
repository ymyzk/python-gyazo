import pytest
from requests.structures import CaseInsensitiveDict

from gyazo.api import Api
from gyazo.error import GyazoError


@pytest.fixture
def api():
    return Api()


def test_parse_and_check_success(api, mocker):
    mock_response = mocker.MagicMock()
    headers = CaseInsensitiveDict()
    headers["X-Runtime"] = "0.008495"
    mock_response.headers = headers
    data = {
        "height": 320,
        "provider_name": "Gyazo",
        "provider_url": "https://gyazo.com",
        "type": "photo",
        "url": "https://bot.gyazo.com/e72675b15a56b1.png",
        "version": "1.0",
        "width": 640
    }
    mock_response.json.return_value = data
    mock_response.status_code = 200

    actual_headers, actual_data = api._parse_and_check(mock_response)

    assert actual_headers == headers
    assert actual_data == data


def test_parse_and_check_error_exception(api, mocker):
    mock_response = mocker.MagicMock()
    headers = CaseInsensitiveDict()
    headers["X-Runtime"] = "0.008495"
    mock_response.headers = headers
    mock_response.json.side_effect = ValueError
    mock_response.status_code = 200

    with pytest.raises(ValueError):
        api._parse_and_check(mock_response)


def test_parse_and_check_error_status_code(api, mocker):
    mock_response = mocker.MagicMock()
    headers = CaseInsensitiveDict()
    headers["X-Runtime"] = "0.008495"
    mock_response.headers = headers
    data = {
        "message": "image not found."
    }
    mock_response.json.return_value = data
    mock_response.status_code = 404

    with pytest.raises(GyazoError):
        api._parse_and_check(mock_response)


def test_parse_and_check_error_status_code_without_message(api, mocker):
    mock_response = mocker.MagicMock()
    headers = CaseInsensitiveDict()
    headers["X-Runtime"] = "0.008495"
    mock_response.headers = headers
    data = {}
    mock_response.json.return_value = data
    mock_response.status_code = 404

    with pytest.raises(GyazoError):
        api._parse_and_check(mock_response)
