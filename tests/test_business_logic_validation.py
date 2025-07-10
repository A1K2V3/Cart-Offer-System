import pytest
import allure
from library.services.cart_offer_services import CartOfferServices
from library.mockserver import MockServer


@allure.feature("Cart Offer - Business Rule Validation")
@pytest.mark.validation
@pytest.mark.parametrize(
    "title, cart_value, user_id, restaurant_id, segment, offer_type, offer_value, allowed_segments, expected_cart_value, expected_status, xfail_reason",
    [
        ("TC_001: Invalid data type for cart_value", "abc", 1, 1, None, None, None, None, None, 400, None),
        ("TC_002: Negative cart value", -100, 1, 1, None, None, None, None, None, 400, None),
        ("TC_003: Ineligible user segment", 200, 1, 1, "unknown", "FLATX", 10, ["p1"], 200, 200, "Segment mismatch — no offer applied"),
    ]
)
def test_cart_offer_business_rules(
    cart_offer: CartOfferServices,
    mockserver: MockServer,
    title: str,
    cart_value,
    user_id,
    restaurant_id,
    segment,
    offer_type,
    offer_value,
    allowed_segments,
    expected_cart_value,
    expected_status,
    xfail_reason: str,
):
    allure.dynamic.title(title)

    if xfail_reason:
        pytest.xfail(reason=xfail_reason)

    if segment:
        mockserver.set_user_segment_mock(user_id=user_id, segment=segment)

    if offer_type and allowed_segments:
        cart_offer.create_offer(
            restaurant_id=restaurant_id,
            offer_type=offer_type,
            offer_value=offer_value,
            customer_segment=allowed_segments,
        )

    response = cart_offer.apply_offer(
        cart_value=cart_value,
        user_id=user_id,
        restaurant_id=restaurant_id,
    )

    assert response.status_code in (expected_status, 422)

    if expected_status == 200 and expected_cart_value is not None:
        actual = response.json()["cart_value"]
        if isinstance(expected_cart_value, float):
            assert round(actual, 2) == round(expected_cart_value, 2)
        else:
            assert actual == expected_cart_value


@allure.feature("Cart Offer - Business Rule Validation")
@pytest.mark.validation
@allure.title("TC_004: Multiple offers for same segment — best offer applied")
def test_multiple_offers_best_selected(cart_offer: CartOfferServices, mockserver: MockServer):
    mockserver.set_user_segment_mock(user_id=1, segment="p1")
    cart_offer.create_offer(restaurant_id=1, offer_type="FLATX", offer_value=10, customer_segment=["p1"])
    cart_offer.create_offer(restaurant_id=1, offer_type="FLATX", offer_value=20, customer_segment=["p1"])

    response = cart_offer.apply_offer(cart_value=200, user_id=1, restaurant_id=1)

    assert response.status_code == 200
    assert response.json()["cart_value"] == 180
