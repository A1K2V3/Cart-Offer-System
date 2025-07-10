import logging
import json
import requests

logger = logging.getLogger(__name__)


class MockServer:

    def __init__(self, url: str) -> None:
        self.url = url
        logger.info(f"MockServer initialized at {url}")

    def set_user_segment_mock(self, user_id: int, segment: str):

        expectation_payload = {
            "httpRequest": {
                "method": "GET",
                "path": "/api/v1/user_segment",
                "queryStringParameters": {
                    "user_id": [str(user_id)]
                }
            },
            "httpResponse": {
                "statusCode": 200,
                "headers": [
                    {"name": "Content-Type", "values": ["application/json"]}
                ],
                "body": json.dumps({"segment": segment})
            }
        }
        logger.info(f"Setting mock for user_id={user_id}, segment={segment}")
        response = requests.put(
            f"{self.url}/mockserver/expectation",
            json=expectation_payload
        )

        if response.status_code not in [201, 200]:
            logger.error(
                f"Failed to set mock: {response.status_code} {response.text}")
            raise Exception(
                f"Failed to set mock for user_id={user_id}: {response.text}")
        else:
            logger.info("Mock expectation set successfully.")
