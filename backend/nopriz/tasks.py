import logging
import math
import os
import time

import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.conf import settings
from django.core.management import call_command
from django.db.models import Q
from django.db.models.functions import Length
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from nopriz.models import NoprizFiz, NoprizYr

from .models import NoprizFiz, NoprizYr
from .utils import (
    NoprizFizExcelGenerator,
    NoprizYrExcelGenerator,
    extract_text_from_image,
    fiz_get_type_of_work,
    generate_combinations_of_replacements,
)

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


def fiz_check_id_number(img_url, id_number):
    r = requests.get(url=f"https://nrs.nopriz.ru/?s.registrationNumber={id_number}")
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find("table")
    for row in table.find("tbody").find_all("tr")[1:2]:
        columns = row.find_all("td")
        id_number_img = columns[0].find("img")["src"]
        id_number_img = BASE_URL + id_number_img[3:]
        if id_number_img == img_url:
            return True
        return False
    return False


def fiz_get_verify_id(img_url, id_number):
    obj_id_number = id_number
    if fiz_check_id_number(img_url, id_number):
        logger.info(f"{id_number} Прошел верификацию.")
        return id_number
    else:
        id_number_list = generate_combinations_of_replacements(id_number)
        for id_number in id_number_list:
            res = fiz_check_id_number(img_url, id_number)
            logger.info(f"Делаю замену {obj_id_number} на {id_number}, результат {res}")
            if res:
                logger.info(f"{obj_id_number} Верифицирован.")
                return id_number
        logger.info(f"{obj_id_number} Не верифицирован.")
        return None


@shared_task
def fiz_parse_main_data():
    total_objects_in_db = NoprizFiz.objects.count()
    objects_per_page = 20
    start_page = math.floor(total_objects_in_db / objects_per_page) + 1

    r = requests.get(BASE_URL)
    time.sleep(0.5)
    soup = BeautifulSoup(r.content, "html.parser")
    pages = int(
        float(soup.find("div", {"class": "tatal-count-wrapper"}).text.split(" ")[-1])
        / objects_per_page
    )
    for page in range(start_page, pages + 1):
        r = requests.get(f"{BASE_URL}?sort=s.id&direction=ASC&page={page}")
        time.sleep(0.09)
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")

        for row in table.find("tbody").find_all("tr")[1:]:
            columns = row.find_all("td")
            try:
                id_number_img = columns[0].find("img")["src"]
                full_name_img = columns[1].find("img")["src"]
                date_of_inclusion_protocol_img = columns[2].find("img")["src"]

                full_name_img = BASE_URL + full_name_img[3:]
                id_number_img = BASE_URL + id_number_img[3:]
                date_of_inclusion_protocol_img = (
                    BASE_URL + date_of_inclusion_protocol_img[3:]
                )

                id_number = extract_text_from_image(id_number_img)
                full_name = extract_text_from_image(full_name_img)
                date_of_inclusion_protocol = extract_text_from_image(
                    date_of_inclusion_protocol_img
                )
                obj = NoprizFiz.objects.get_or_create(
                    id_number_img=id_number_img,
                    full_name_img=full_name_img,
                    id_number=id_number,
                    full_name=full_name,
                    date_of_inclusion_protocol=date_of_inclusion_protocol,
                    type_of_work=fiz_get_type_of_work(columns),
                    status_worker=STATUS_MAP[columns[-1].text],
                )
                logger.info(f"Был создан новый объект {obj}")
            except Exception as e:
                pass


@shared_task
def fiz_verify_id_number():
    for object in NoprizFiz.objects.filter(verified_id_number=False).order_by(
        "id_number_verification_attempts"
    ):
        id_number = object.id_number
        new_id_number = fiz_get_verify_id(
            img_url=object.id_number_img, id_number=id_number
        )
        if new_id_number:
            object.id_number = new_id_number
            object.verified_id_number = True
            object.save()
        else:
            object.id_number_verification_attempts += 1
            object.save()


@shared_task
def fiz_parse_type_of_work():
    objects = NoprizFiz.objects.annotate(work_length=Length("type_of_work")).filter(
        Q(work_length__lt=53)
        | Q(type_of_work__isnull=True)
        | Q(type_of_work__exact="")
        | Q(type_of_work__regex=r"^\s*$"),
        verified_id_number=True,
    )
    for obj in objects:
        try:
            r = requests.get(
                url=f"https://nrs.nopriz.ru/?s.registrationNumber={obj.id_number}"
            )
            r.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Ошибка запроса для {obj.id_number}: {e}")
            continue

        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        if table:
            try:
                row = table.find("tbody").find_all("tr")[1]
                columns = row.find_all("td")
                obj.type_of_work = fiz_get_type_of_work(columns)
                logger.info(f"Обновил тип работ для {obj.id_number}")
                obj.save()

            except (IndexError, AttributeError) as e:
                logger.error(f"Ошибка парсинга для {obj.id_number}: {e}")
        else:
            logger.error(f"Таблица не найдена для {obj.id_number}")


@shared_task
def fiz_parse_status_worker():
    objects = NoprizFiz.objects.exclude(
        status_worker__in=["ACTIVE", "EXCLUDED"], verified_id_number=True
    )
    for obj in objects:
        try:
            r = requests.get(
                url=f"https://nrs.nopriz.ru/?s.registrationNumber={obj.id_number}"
            )
            r.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Ошибка запроса для {obj.id_number}: {e}")
            continue

        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        if table:
            try:
                row = table.find("tbody").find_all("tr")[1]
                columns = row.find_all("td")
                obj.status_worker = STATUS_MAP[columns[-1].text.strip()]
                obj.save()
                logger.info(f"Обновлен статус {obj.id_number}")

            except (IndexError, AttributeError) as e:
                logger.error(f"Ошибка парсинга для {obj.id_number}: {e}")
        else:
            logger.error(f"Таблица не найдена для {obj.id_number}")


@shared_task
def fiz_verify_parsed_data():
    objects = NoprizFiz.objects.filter(
        verified_id_number=True,
        is_parsed=False,
        status_worker__in=["ACTIVE", "EXCLUDED"],
        type_of_work__isnull=False,
    )
    for obj in objects:
        obj.is_parsed = True
        obj.save()


@shared_task
def yr_parse_data():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.nopriz.ru/nreesters/elektronnyy-reestr/")
    driver.maximize_window()
    time.sleep(1)
    WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "reestr_iframe"))
    )

    for page in range(1, 20000):
        WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table__list"))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"class": "table__list"})
        rows = table.find_all("tr")[1:]
        for row in rows:
            columns = row.find_all("td")
            try:
                NoprizYr.objects.get_or_create(
                    id_number=columns[0].text,
                    name_cpo=columns[1].text,
                    status=STATUS_MAP[columns[2].text.strip()],
                    name_of_the_member_cpo=columns[3].text,
                    inn=columns[4].text,
                    ogrn=columns[5].text,
                    date_of_registration=columns[6].text,
                    date_of_termination=columns[7].text,
                    director=columns[8].text,
                )
            except KeyError as e:
                logger.info(f"{e} {columns[0].text}")
            time.sleep(0.2)
        driver.find_elements(By.CLASS_NAME, "v-pagination__navigation")[-1].click()


@shared_task
def generate_excel_nopriz_fiz():
    generator = NoprizFizExcelGenerator()
    return generator.generate_excel()


@shared_task
def generate_excel_nopriz_yr():
    generator = NoprizYrExcelGenerator()
    return generator.generate_excel()


@shared_task
def dumpdata_and_send_to_telegram():
    try:
        date = timezone.now().date()
        output_file = f"nopriz-{date}.json"
        with open(output_file, "w") as f:
            call_command("dumpdata", "nopriz", stdout=f)
        with open(output_file, "rb") as f:
            settings.BOT.send_document(
                chat_id=settings.DUMP_CHAT_ID, document=f, caption="Дамп nopriz"
            )
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)
        return f"Dump sent successfully."
