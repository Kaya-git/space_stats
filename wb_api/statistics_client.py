import aiohttp
import logging

from services.tools import get_date

LOGGER = logging.getLogger(__name__)

RETRY_DELAY = 0.1
URL = "https://statistics-api.wildberries.ru/api/v1/supplier/"


class StatisticsApiClient:
    """Get WB stock statistics."""

    def __init__(self, token):
        self.token = token

        self.base_url = URL

    def connect(self, params, server):
        # redis_client.get_date
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": self.token,
            }
            response = session.get(url=server, params=params, headers=headers)
            LOGGER.info(f"URL WAS: {response.url}")
            return response

    def get_stock(self):
        LOGGER.info("Preparing url params for stocks...")
        params = {
            "dateFrom": await get_date(days=15),
            "key": self.token,
        }
        return self.connect(params, self.base_url + "stocks")

    def get_ordered(self, url, week=False, flag=1, days=None):
        params = {
            "dateFrom": await get_date(week, days),
            "key": self.token,
            "flag": flag,
        }
        return self.connect(params, self.base_url + url)

    def get_report(self, url, week=False):
        params = {
            "dateFrom": await get_date(week),
            "dateto": await get_date(),
            "key": self.token,
        }
        return self.connect(params, self.base_url + url)
