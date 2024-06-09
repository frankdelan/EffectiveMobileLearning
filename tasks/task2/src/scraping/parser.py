import asyncio
import datetime
import io
from typing import Optional

import fake_useragent
import pandas as pd
from bs4 import BeautifulSoup
from aiohttp import ClientSession
from pandas import DataFrame

from decorators import handle_client_exception
from models import SpimexTradingResults
from config import BXAJAXID

BASE_URL: str = f'https://spimex.com/markets/oil_products/trades/results/?bxajaxid={BXAJAXID}'


class QueryManager:
    @staticmethod
    async def get_header_data() -> dict[str, str]:
        user = fake_useragent.UserAgent()
        header = {
            'user-agent': user.random,
        }
        return header

    @staticmethod
    async def get_html(uri: str) -> str:
        """Метод для получения html страницы"""
        async with ClientSession(headers=await QueryManager.get_header_data()) as session:
            async with session.get(url=uri) as response:
                if response.status == 200:
                    data: str = await response.text()
                    return data

    @staticmethod
    @handle_client_exception(default_return=[])
    async def get_file_data(uri: str) -> list[Optional[SpimexTradingResults]]:
        """Метод для получения данных xls файла"""
        async with ClientSession(headers=await QueryManager.get_header_data()) as session:
            async with session.get(url=uri, params={"downloadformat": "xls"}) as response:
                data = pd.read_excel(io.BytesIO(await response.read()), usecols='B:O', skiprows=3)
                if not data.empty:
                    return await ParseManager.parse_xlsx(data.dropna())

    @staticmethod
    async def get_page(uri: str) -> list[Optional[str]]:
        """Метод для получения ссылок на скачивание xls файлов"""
        data: str = await QueryManager.get_html(uri)
        if data is None:
            return []
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
    async def parse_xlsx(data: DataFrame) -> list[SpimexTradingResults]:
        """Метод для парсинга xls файла"""
        trading_date = data.columns[0].replace('Дата торгов: ', '')
        return [SpimexTradingResults(
            exchange_product_id=item[1],
            exchange_product_name=item[2],
            oil_id=item[1][:4],
            delivery_basis_id=item[1][4:7],
            delivery_basis_name=item[3],
            delivery_type_id=item[1][-1],
            volume=0 if item[4] == '-' else int(item[4]),
            total=0 if item[5] == '-' else float(item[5]),
            count=int(item[14]),
            trading_date=datetime.datetime.strptime(f'{trading_date}', '%d.%m.%Y').date(),
            created_on=datetime.datetime.now())
            for item in data.itertuples()
            if item[2] and item[14] != '-']


class AsyncController:
    async def _get_files_links(self) -> list[list[str]]:
        """Метод для асинхронного прохода по всем страницам и сбора ссылок на файлы"""
        pages_count: int = await ParseManager.get_pages_count()
        pages_uris: list[str] = [BASE_URL + f'&page=page-{page_number}'
                                 for page_number in range(1, pages_count + 1)]
        tasks: list = []
        for uri in pages_uris:
            tasks.append(asyncio.create_task(QueryManager.get_page(uri)))
        result: list[list[str]] = await asyncio.gather(*tasks)
        return result

    async def get_objects(self) -> list[list[SpimexTradingResults]]:
        """Метод для асинхронного получения данных из xls файлов"""
        plain_links_list: list[str] = [item for sublist in await self._get_files_links() for item in sublist]
        tasks: list = []
        for link in plain_links_list:
            tasks.append(asyncio.create_task(QueryManager.get_file_data(link)))
        result: list[list[SpimexTradingResults]] = await asyncio.gather(*tasks)
        return result
