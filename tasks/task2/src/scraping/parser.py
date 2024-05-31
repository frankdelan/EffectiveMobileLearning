import asyncio
import datetime
from typing import Generator

from bs4 import BeautifulSoup
from aiohttp import ClientSession
from xlrd import open_workbook

from tasks.task2.src.models import SpimexTradingResults
from tasks.task2.src.config import BXAJAXID

BASE_URL: str = f'https://spimex.com/markets/oil_products/trades/results/?bxajaxid={BXAJAXID}'


class QueryManager:
    @staticmethod
    async def get_html() -> str:
        async with ClientSession() as session:
            async with session.get(url=BASE_URL) as response:
                data: str = await response.text()
        return data

    @staticmethod
    async def get_file_data(uri: str):
        async with ClientSession() as session:
            async with session.get(url=uri, params={"downloadformat": "xls"}) as response:
                data: bytes = await response.read()
        return await ParseManager.parse_xlsx(data)

    @staticmethod
    async def get_page(url: str) -> list[str]:
        async with ClientSession() as session:
            async with session.get(url=url) as response:
                data = await response.text()
        return await ParseManager.parse_download_links(data)


class ParseManager:
    @staticmethod
    async def get_pages_count() -> int:
        html: str = await QueryManager.get_html()
        soup = BeautifulSoup(html, 'html.parser')
        last_page: int = int((soup.find("div", {"class": 'bx-pagination-container'}).
                              find_all("li", {'class': ''}))[-1].find("a").find('span').text)
        return last_page

    @staticmethod
    async def parse_download_links(text) -> list[str]:
        soup = BeautifulSoup(text, 'html.parser')
        elements = soup.find_all("a", {'class': 'accordeon-inner__item-title link xls'})
        return ('https://spimex.com' + link.get('href') for link in elements)

    @staticmethod
    async def parse_xlsx(data: bytes):
        workbook = open_workbook(file_contents=data)
        sheet = workbook.sheet_by_index(0)

        return (SpimexTradingResults(
            exchange_product_id=sheet.row_values(idx)[1],
            exchange_product_name=sheet.row_values(idx)[2],
            oil_id=sheet.row_values(idx)[1][:4],
            delivery_basis_id=sheet.row_values(idx)[1][4:7],
            delivery_basis_name=sheet.row_values(idx)[3],
            delivery_type_id=sheet.row_values(idx)[1][-1],
            volume=int(sheet.row_values(idx)[4]) if sheet.row_values(idx)[4].isnumeric() else 0,
            total=int(sheet.row_values(idx)[5]) if sheet.row_values(idx)[5].isnumeric() else 0,
            count=int(sheet.row_values(idx)[14]),
            trading_date=datetime.date.today(),
            created_on=datetime.datetime.now())
            for idx in range(9, sheet.nrows)
            if sheet.row_values(idx)[14].isnumeric() and int(sheet.row_values(idx)[14]) > 0 and sheet.row_values(idx)[2])


class AsyncController:
    async def _get_files_links(self) -> list[list[str]]:
        pages_count: int = await ParseManager.get_pages_count()
        pages_uris: list[str] = [BASE_URL + f'?page=page-{item}&bxajaxid={BXAJAXID}' for item in range(1, pages_count + 1)]
        tasks: list = []
        for uri in pages_uris:
            tasks.append(asyncio.create_task(QueryManager.get_page(uri)))
        result: list = await asyncio.gather(*tasks)
        return result

    async def get_objects(self):
        plain_links_list: Generator[str] = (item for sublist in await self._get_files_links() for item in sublist)
        tasks: list = []
        for link in plain_links_list:
            tasks.append(asyncio.create_task(QueryManager.get_file_data(link)))
        result = await asyncio.gather(*tasks)
        return result
