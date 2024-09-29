from io import BytesIO
import logging
import time
from PIL import Image

import pytesseract
import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.db.utils import DataError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .models import NostroySmet, NostroyFiz

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")


logger = logging.getLogger(__name__)
BASE_URL = "https://nrs.nostroy.ru/"
STATUS_MAP = {
    "Действует": "ACTIVE",
    "Исключен": "EXCLUDED",
}


@shared_task()
def smet_parse():
    try:
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


def get_image_selenium(img_url):
    r = requests.get(img_url, verify=False)
    with Image.open(BytesIO(r.content)) as img:
        text = pytesseract.image_to_string(img, config="--psm 6 --oem 3", lang="rus")
        return text


@shared_task()
def fiz_parse():
    total_objects = NostroyFiz.objects.count()
    objects_per_page = 20 
    last_parsed_page = total_objects // objects_per_page + 1


    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    for page in range(last_parsed_page, 20000):
        driver.get(f"https://nrs.nostroy.ru/?sort=s.id&direction=ASC&page={page}")
        time.sleep(2)
        WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table"))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"class": "table"})
        rows = table.find_all("tr")[1:]

        for row in rows:
            columns = row.find_all("td")
            id_number_img = columns[0].find("img")
            id_number_img = BASE_URL + id_number_img["src"][3:] if id_number_img else ""
            if not id_number_img or len(id_number_img) < 10:
                continue
            full_name_img = columns[1].find("img")
            date_of_inclusion_protocol_img = columns[2].find("img")
            date_of_modification_img = columns[3].find("img")
            date_of_issue_certificate_img = columns[4].find("img")

            
            full_name_img = BASE_URL + full_name_img["src"][3:] if full_name_img else ""
            date_of_inclusion_protocol_img = (
                BASE_URL + date_of_inclusion_protocol_img["src"][3:]
                if date_of_inclusion_protocol_img
                else ""
            )
            date_of_modification_img = (
                BASE_URL + date_of_modification_img["src"][3:]
                if date_of_modification_img
                else ""
            )
            date_of_issue_certificate_img = (
                BASE_URL + date_of_issue_certificate_img["src"][3:]
                if date_of_issue_certificate_img
                else ""
            )

            id_number = get_image_selenium(id_number_img) if id_number_img else ""
            full_name = get_image_selenium(full_name_img) if full_name_img else ""
            date_of_inclusion_protocol = (
                get_image_selenium(date_of_inclusion_protocol_img)
                if date_of_inclusion_protocol_img
                else ""
            )
            date_of_modification = (
                get_image_selenium(date_of_modification_img)
                if date_of_modification_img
                else ""
            )
            date_of_issue_certificate = (
                get_image_selenium(date_of_issue_certificate_img)
                if date_of_issue_certificate_img
                else ""
            )

            logger.info(f"id_number: {id_number}, full_name: {full_name}")

            type_of_work = columns[-2].text.strip()
            status = columns[-1].text.split("\n")[-2].strip()
            if len(status) > 4:
                status = STATUS_MAP.get(status, status)
            try:
                obj, created = NostroyFiz.objects.get_or_create(
                    id_number_img=id_number_img,
                    defaults={
                        "date_of_inclusion_protocol_img": date_of_inclusion_protocol_img,
                        "date_of_modification_img": date_of_modification_img,
                        "date_of_issue_certificate_img": date_of_issue_certificate_img,
                        "full_name_img": full_name_img,
                        "id_number": id_number,
                        "full_name": full_name,
                        "date_of_inclusion_protocol": date_of_inclusion_protocol,
                        "date_of_modification": date_of_modification,
                        "date_of_issue_certificate": date_of_issue_certificate,
                        "type_of_work": type_of_work,
                        "status_worker": status,
                    },
                )
            except Exception as e:
                logger.error(f"Unexpected error: {e}")

            time.sleep(0.2)

        # next_page_button = driver.find_elements(By.CLASS_NAME, "v-pagination__navigation")[-1]
        # next_page_button.click()
