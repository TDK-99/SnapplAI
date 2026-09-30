import pytest
from unittest.mock import MagicMock, patch
from google.genai import errors
import src.llm as llm_module
from src.llm import generate_content_resilient, FALLBACK_MODELS

# def mock api response
def api_error(code):
    """Shorthand to build an APIError with a given HTTP status code."""
    return errors.APIError(code, {"error": {"message": f"error {code}"}})


# autouse: runs before/after every test to reset the global model pointer,
# preventing test-order dependencies.
@pytest.fixture(autouse=True)
def reset_sticky_model_pointer():
    llm_module._current_model_idx = 0
    yield
    llm_module._current_model_idx = 0


@patch("src.llm.time.sleep")  # avoid real delays between retries
def test_rotates_to_next_model_after_exhausting_retries_and_stays_sticky(mock_sleep):
    client = MagicMock()
    # side_effect list: each call consumes the next item in order
    client.models.generate_content.side_effect = [
        api_error(503),
        api_error(503),
        "ok-response",
    ]

    result = generate_content_resilient(client, contents="hi", config={}, max_retries=2)

    assert result == "ok-response"

    calls = client.models.generate_content.call_args_list
    # Calls 1-2: model 0 retried twice (503), call 3: rotated to model 1
    assert [c.kwargs["model"] for c in calls] == [
        FALLBACK_MODELS[0], FALLBACK_MODELS[0], FALLBACK_MODELS[1]
    ]

    # Pointer stays on model 1 (sticky) instead of resetting to 0
    assert llm_module._current_model_idx == 1


def test_non_retryable_error_raises_immediately_without_retry():
    client = MagicMock()
    # 400 is a client error, retrying would send the same bad request
    client.models.generate_content.side_effect = api_error(400)

    with pytest.raises(errors.APIError) as exc_info:
        generate_content_resilient(client, contents="hi", config={}, max_retries=5)

    assert exc_info.value.code == 400
    client.models.generate_content.assert_called_once()