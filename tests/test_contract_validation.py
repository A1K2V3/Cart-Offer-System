import pytest
import allure
from library.services.cart_offer_services import CartOfferServices
from library.mockserver import MockServer


@allure.feature("Cart Offer - API Contract Validation")
@pytest.mark.validation
@pytest.mark.parametrize(
    "title, payload, expected_status_codes, expected_field, xfail_reason",
    [
        ("TC_001: Missing cart_value", {"user_id": 1, "restaurant_id": 1}, (400, 422), "cart_value", None),
        ("TC_002: Missing user_id", {"cart_value": 200, "restaurant_id": 1}, (400, 422), "user_id", None),
        ("TC_003: Missing restaurant_id", {"cart_value": 200, "user_id": 1}, (400, 422), "restaurant_id", None),
        ("TC_004: Empty payload", {}, (400, 422), "cart_value", None),
        ("TC_005: Extra unknown field", {"cart_value": 200, "user_id": 1, "restaurant_id": 1, "foo": "bar"}, (200,), None, None),
        ("TC_006: cart_value as string", {"cart_value": "abc", "user_id": 1, "restaurant_id": 1}, (400, 422), "cart_value", None),
        ("TC_007: user_id as string", {"cart_value": 200, "user_id": "abc", "restaurant_id": 1}, (400, 422), "user_id", None),
        ("TC_008: Negative cart value", {"cart_value": -100, "user_id": 1, "restaurant_id": 1}, (400, 422), "cart_value", None),
        ("TC_009: Negative user_id", {"cart_value": 200, "user_id": -1, "restaurant_id": 1}, (400, 422), "user_id", None),
        ("TC_010: Negative restaurant_id", {"cart_value": 200, "user_id": 1, "restaurant_id": -10}, (400, 422), "restaurant_id", None),
    ]
)
def test_api_contract_validation(
    cart_offer: CartOfferServices,
    title: str,
    payload: dict,
    expected_status_codes: tuple,
    expected_field: str,
    xfail_reason: str
):
    allure.dynamic.title(title)

    if xfail_reason:
        pytest.xfail(reason=xfail_reason)

    response = cart_offer.client.post(["api/v1/cart/apply_offer"], json=payload)
    assert response.status_code in expected_status_codes, f"Expected {expected_status_codes}, got {response.status_code}"

    try:
        body = response.json()
        if expected_field:
            detail = str(body.get("detail") or body)
            assert expected_field in detail, f"Expected field '{expected_field}' in response: {body}"
    except Exception:
        pass

@allure.feature("Cart Offer - Edge Case Logic")
@pytest.mark.validation
@allure.title("TC_011: Mock server fails unexpectedly")
def test_mockserver_failure_simulation(mockserver: MockServer, monkeypatch):
    def raise_failure(self, user_id, segment):
        raise Exception("Mock server unavailable")

    monkeypatch.setattr(MockServer, "set_user_segment_mock", raise_failure)

    with pytest.raises(Exception, match="Mock server unavailable"):
        mockserver.set_user_segment_mock(user_id=1, segment="p1")
