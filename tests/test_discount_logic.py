import pytest
import allure
from library.services.cart_offer_services import CartOfferServices
from library.mockserver import MockServer


@allure.feature("Cart Offer - Flat Discount Logic (FLATX and FLAT%)")
@pytest.mark.cart
@pytest.mark.parametrize(
    "title, user_id, segment, offer_type, offer_value, cart_value, expected_cart_value, xfail_reason",
    [
        ("TC_001: FLATX offer applied correctly", 1, "p1", "FLATX", 10, 200, 190, None),
        ("TC_002: FLATX offer with high discount (but valid)", 1, "p1", "FLATX", 40, 200, 160, None),
        ("TC_003: FLAT% offer applied correctly", 2, "p2", "FLAT%", 10, 200, 180, None),
        ("TC_004: FLATX equals cart value", 1, "p1", "FLATX", 100, 100, 0, None),
        ("TC_005: FLATX exceeds cart value", 1, "p1", "FLATX", 200, 50, 0, None),
        ("TC_006: FLAT% with 100% discount", 3, "p3", "FLAT%", 100, 200, 0, None),
        ("TC_007: FLAT% with >100% discount", 3, "p3", "FLAT%", 150, 200, 0, None),
        ("TC_008: Zero cart value with FLATX", 2, "p2", "FLATX", 10, 0, 0, None),
        ("TC_009: Decimal cart value with FLATX", 1, "p1", "FLATX", 10, 199.99, 189.99, None),
        ("TC_010: High cart value with FLAT% offer", 1, "p1", "FLAT%", 50, 9999, 4999.5, None),
    ]
)
def test_cart_offer_flat_cases(
    cart_offer: CartOfferServices,
    mockserver: MockServer,
    title: str,
    user_id: int,
    segment: str,
    offer_type: str,
    offer_value: float,
    cart_value: float,
    expected_cart_value: float,
    xfail_reason: str
):
    allure.dynamic.title(title)

    if xfail_reason:
        pytest.xfail(reason=xfail_reason)

    mockserver.set_user_segment_mock(user_id=user_id, segment=segment)

    cart_offer.create_offer(
        restaurant_id=1,
        offer_type=offer_type,
        offer_value=offer_value,
        customer_segment=[segment]
    )

    response = cart_offer.apply_offer(
        cart_value=cart_value,
        user_id=user_id,
        restaurant_id=1
    )

    actual_cart_value = response.json()["cart_value"]

    if isinstance(expected_cart_value, float):
        assert round(actual_cart_value, 2) == round(expected_cart_value, 2), f"Expected {expected_cart_value}, got {actual_cart_value}"
    else:
        assert actual_cart_value == expected_cart_value, f"Expected {expected_cart_value}, got {actual_cart_value}"
