import json

import aiohttp
import logging

from wb.services.tools import get_date


LOGGER = logging.getLogger(__name__)


class StandardApiClient:
    """Get Marketplace Statistics."""

    def __init__(self, new_api_key: str):
        self.token = new_api_key
        self.base = "https://suppliers-api.wildberries.ru/"

    def build_headers(self):
        return {
            "Authorization": self.token,
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def update_discount(self, wb_id, new_discount):
        with aiohttp.ClientSession() as session:
            url = self.base + "public/api/v1/updateDiscounts"
            data = [{"discount": int(new_discount), "nm": int(wb_id)}]

            response = session.post(
                url, data=json.dumps(data), headers=self.build_headers()
            )
            LOGGER.info(f"{response.status_code}, message: {response.json()}")
            if response.status_code == 200:
                return True, "Success"
            errors = response.json().get("errors")
            error = errors[0] if errors else "Неизвестная ошибка"
            return False, error

    def get_prices(self):
        with aiohttp.ClientSession() as session:
            url = self.base + "public/api/v1/info"

            response = session.get(url, headers=self.build_headers())

            if response.status_code == 200:
                return response.json()
            return []

    def get_stock(self):
        url = self.base + "api/v2/stocks"

        offset = 200

        def get_page(skip=0):
            with aiohttp.ClientSession() as session:

                get_params = {
                    "skip": skip,
                    "take": offset,
                }
                try:
                    response = session.get(
                        url, get_params,
                        headers=self.build_headers()
                    )
                except ConnectionError as e:
                    LOGGER.info(f"ConnectionError {e}")
                    return None
                return response

        response = get_page()
        if not response:
            return []
        if response.status_code != 200:
            LOGGER.info(f"{response.status_code}, {response.text}")
            return []

        stock = []
        batch = response.json()
        total = int(batch.get("total", 0))
        if total == 0:
            return []
        LOGGER.info(f"Total {total} products")
        attempt = 1

        stock += batch.get("stocks", 0)
        while total > offset * attempt:
            stock += get_page(offset * attempt).json().get("stocks", 0)
            attempt += 1
        LOGGER.info(f"Got stocks from marketplace {len(stock)} pcs.")
        return stock

    def get_orders(self, days):
        url = self.base + "api/v2/orders"

        offset = 200

        def get_page(skip=0):
            with aiohttp.ClientSession() as session:
                get_params = {
                    "skip": skip,
                    "take": offset,
                    "date_start": await get_date(days=14),
                }
                return session.get(
                    url,
                    get_params,
                    headers=self.build_headers()
                )

        response = get_page()
        if response.status_code != 200:
            LOGGER.info(f"{response.status_code}, {response.text}")
            return []

        orders = []
        batch = response.json()
        total = int(batch.get("total"))
        LOGGER.info(f"Total {total} products")
        attempt = 1

        orders += batch["orders"]
        while total > offset * attempt:
            orders += get_page(offset * attempt).json()["orders"]
            attempt += 1
        LOGGER.info(f"Got orders from marketplace {len(orders)} pcs.")
        return orders

    def get_content(self):
        """Get all content to obtain tricky images' urls.
        Must be cached properly, heavy request."""
        with aiohttp.ClientSession() as session:
            LOGGER.info("Getting content...")
            url = self.base + "content/v1/cards/cursor/list"

            first_payload = {
                "sort": {
                    "cursor": {
                        "limit": 1000
                    },
                    "filter": {
                        "withPhoto": -1,
                        "allowedCategoriesOnly": True
                    },
                    "sort": {
                        "sortColumn": "updateAt",
                        "ascending": False
                    }
                }
            }
            content = dict()
            total = 1000  # Any number above 1000 will do
            limit = 1000
            while total >= limit:
                response = session.post(
                    url,
                    headers=self.build_headers(),
                    data=json.dumps(first_payload)
                )
                LOGGER.info("Entering loop")
                if response.status_code == 200:

                    data = response.json()["data"]
                    total = int(data["cursor"]["total"])
                    LOGGER.info(f"Total cards: {data['cursor']}")

                    first_payload[
                        "sort"
                        ][
                            "cursor"
                            ][
                                "updatedAt"
                                ] = data["cursor"]["updatedAt"]
                    first_payload[
                        "sort"
                        ][
                            "cursor"
                            ][
                                "nmID"
                                ] = data["cursor"]["nmID"]
                    LOGGER.info(first_payload)
                    cards = data["cards"]

                    for card in cards:
                        content[card["nmID"]] = {
                            "image": card["mediaFiles"][0],
                            "object": card["object"]
                        }
                else:
                    LOGGER.info(response.text)
                    break
            LOGGER.info("Exit loop")
            return content
