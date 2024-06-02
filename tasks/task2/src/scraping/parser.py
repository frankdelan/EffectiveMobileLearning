import asyncio
import datetime
from typing import Optional

from bs4 import BeautifulSoup
from aiohttp import ClientSession, ClientPayloadError, ClientConnectorError
from xlrd import open_workbook

from models import SpimexTradingResults
from config import BXAJAXID

BASE_URL: str = f'https://spimex.com/markets/oil_products/trades/results/?bxajaxid={BXAJAXID}'


class QueryManager:
    @staticmethod
    async def get_html(uri: str) -> str:
        """Метод для получения html страницы"""
        async with ClientSession() as session:
            async with session.get(url=uri) as response:
                data: str = await response.text()
                if response.status == 200:
                    return data

    @staticmethod
    async def get_file_data(uri: str, semaphore: asyncio.Semaphore) -> list[Optional[SpimexTradingResults]]:
        """Метод для получения данных xls файла"""
        async with semaphore:
            try:
                async with ClientSession() as session:
                    retries = 3
                    for attempt in range(retries):
                        try:
                            async with session.get(url=uri, params={"downloadformat": "xls"}) as response:
                                data: bytes = await response.read()
                                if response.status == 200:
                                    return await ParseManager.parse_xlsx(data)
                        except ClientPayloadError as e:
                            if attempt < retries - 1:
                                await asyncio.sleep(1)
                                continue
                            else:
                                raise e
            except ClientConnectorError:
                return []

    @staticmethod
    async def get_page(uri: str) -> list[str]:
        """Метод для получения ссылок на скачивание xls файлов"""
        data: str = await QueryManager.get_html(uri)
        return await ParseManager.parse_download_links(data)


class ParseManager:
    @staticmethod
    async def get_pages_count() -> int:
        """Метод для получения количества страниц"""
        html: str = await QueryManager.get_html(BASE_URL)
        soup = BeautifulSoup(html, 'html.parser')
        last_page: int = int((soup.find("div", {"class": 'bx-pagination-container'}).
                              find_all("li", {'class': ''}))[-1].find("a").find('span').text)
        return last_page

    @staticmethod
    async def parse_download_links(text: str) -> list[str]:
        """Метод, которые возвращает генератор с ссылками на xls файлы"""
        soup = BeautifulSoup(text, 'html.parser')
        elements = soup.find_all("a", {'class': 'accordeon-inner__item-title link xls'})
        return ['https://spimex.com' + link.get('href') for link in elements]

    @staticmethod
    async def parse_xlsx(data: bytes) -> list[SpimexTradingResults]:
        """Метод для парсинга xls файла"""
        workbook = open_workbook(file_contents=data)
        sheet = workbook.sheet_by_index(0)
        return [SpimexTradingResults(
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
            if sheet.row_values(idx)[14].isnumeric() and int(sheet.row_values(idx)[14]) > 0 and sheet.row_values(idx)[2]]


class AsyncController:
    async def _get_files_links(self) -> list[list[str]]:
        """Метод для асинхронного прохода по всем страницам и сбора ссылок на файлы"""
        pages_count: int = await ParseManager.get_pages_count()
        pages_uris: list[str] = [BASE_URL + f'?page=page-{page_number}&bxajaxid={BXAJAXID}'
                                      for page_number in range(201, pages_count + 1)]
        tasks: list = []
        for uri in pages_uris:
            tasks.append(asyncio.create_task(QueryManager.get_page(uri)))
        result: list[list[str]] = await asyncio.gather(*tasks)
        print(result)
        return result

    async def get_objects(self) -> list[list[SpimexTradingResults]]:
        """Метод для асинхронного получения данных из xls файлов"""
        plain_links_list: list[str] = [item for sublist in await self._get_files_links() for item in sublist]
        tasks: list = []
        semaphore = asyncio.Semaphore(10)
        for link in plain_links_list:
            tasks.append(asyncio.create_task(QueryManager.get_file_data(link, semaphore)))
        result: list[list[SpimexTradingResults]] = await asyncio.gather(*tasks)
        return result
