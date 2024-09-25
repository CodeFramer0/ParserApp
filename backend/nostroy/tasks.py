import asyncio
import bz2
import logging
import math
import os
import time

import requests
from aiogram.types.input_file import InputFile
from bs4 import BeautifulSoup
from celery import shared_task
from core.settings import bot
from django.conf import settings
from django.core.management import call_command
from django.db.models import Q
from django.db.models.functions import Length
from django.db.utils import DataError
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .models import NostroySmet

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")


logger = logging.getLogger(__name__)
BASE_URL = "https://nrs.nopriz.ru/"
STATUS_MAP = {
    "Действует": "ACTIVE",
    "Исключен": "EXCLUDED",
    "Является членом": "ACTIVE",
}


@shared_task()
def smet_parse():
    try:
        r = requests.get(BASE_URL)
        time.sleep(0.5)
        soup = BeautifulSoup(r.content, "html.parser")

        r = requests.get(
            f"https://nostroy.ru/actual/reestr-spetsialistov-stoimostnogo-inzhiniringa/"
        )
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table", {"class": "m-dept-phone"})

        for row in table.find("tbody").find_all("tr")[1:]:
            columns = row.find_all("td")
            try:
                obj, created = NostroySmet.objects.get_or_create(
                    id_number=columns[0].text.strip(),
                    defaults={
                        "full_name": columns[1].text.strip(),
                        "date_of_inclusion_protocol": columns[2].text.strip(),
                        "date_of_exclusion": columns[3].text.strip(),
                        "type_of_work": columns[4].text.strip(),
                        "status_worker": STATUS_MAP[
                            columns[5].text.strip().split("\n")[-1]
                        ],
                    },
                )
            except DataError as e:
                logger.error(
                    f"DataError occurred for id_number {columns[0].text.strip()}: {e}"
                )
                logger.error(f"Full name: {columns[1].text.strip()}")
                logger.error(f"Date of inclusion protocol: {columns[2].text.strip()}")
                logger.error(f"Date of exclusion: {columns[3].text.strip()}")
                logger.error(f"Type of work: {columns[4].text.strip()}")
                logger.error(f"Status worker: {columns[5].text.strip()[-1]}")
                raise
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
