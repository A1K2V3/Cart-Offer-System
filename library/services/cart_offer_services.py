# library/services/cart_offer_services.py

import logging
from typing import Any

from library.api_client import APIClient
from library.util import SENTINEL

logger = logging.getLogger(__name__)


class CartOfferServices:
    def __init__(self, client: APIClient):
        self.client = client
        logger.info("CartOfferServices initialized")

    def create_offer(
        self,
        *,
        restaurant_id: Any = SENTINEL,
        offer_type: Any = SENTINEL,
        offer_value: Any = SENTINEL,
        customer_segment: Any = SENTINEL,
    ):
        payload = {}
        if restaurant_id is not SENTINEL:
            payload["restaurant_id"] = restaurant_id
        if offer_type is not SENTINEL:
            payload["offer_type"] = offer_type
        if offer_value is not SENTINEL:
            payload["offer_value"] = offer_value
        if customer_segment is not SENTINEL:
            payload["customer_segment"] = customer_segment

        logger.info(f"Creating offer: {payload}")
        return self.client.post("api/v1/offer", json=payload)

    def apply_offer(
        self,
        *,
        cart_value: Any = SENTINEL,
        user_id: Any = SENTINEL,
        restaurant_id: Any = SENTINEL,
    ):
        payload = {}
        if cart_value is not SENTINEL:
            payload["cart_value"] = cart_value
        if user_id is not SENTINEL:
            payload["user_id"] = user_id
        if restaurant_id is not SENTINEL:
            payload["restaurant_id"] = restaurant_id

        logger.info(f"Applying offer: {payload}")
        return self.client.post(["api/v1/cart/apply_offer"], json=payload)
