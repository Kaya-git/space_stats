from typing import List


async def form_links_list(product_links: str) -> List(str):
    return product_links.split(" ")
