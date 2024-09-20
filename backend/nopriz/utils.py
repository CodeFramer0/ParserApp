import itertools
import logging
import re
import time
from io import BytesIO

import pytesseract
import requests
from PIL import Image


def generate_combinations_of_replacements(
    s,
    targets=["5", "6", "Б", "А", "О", "4", "У"],
    replacements=["6", "5", "6", "4", "0", "3", "9"],
):

    if len(targets) != len(replacements):
        raise ValueError(
            "Количество элементов в 'targets' и 'replacements' должно совпадать"
        )

    all_combinations = set([s])

    for target, replacement in zip(targets, replacements):
        temp_results = set()
        for variant in all_combinations:
            indices = [i for i, char in enumerate(variant) if char == target]
            if indices:
                for r in range(1, len(indices) + 1):
                    for combination in itertools.combinations(indices, r):
                        temp_list = list(variant)
                        for idx in combination:
                            temp_list[idx] = replacement
                        temp_results.add("".join(temp_list))
        all_combinations.update(temp_results)

    final_results = set()
    for variant in all_combinations:
        if "-" in variant:
            dash_index = variant.index("-")
            part_before_dash = variant[: dash_index + 1]
            part_after_dash = variant[dash_index + 1 :]
            part_after_dash = re.sub(r"\D", "", part_after_dash)
            final_results.add(part_before_dash + part_after_dash)
        else:
            final_results.add(variant)

    return sorted(final_results)


def extract_text_from_image(img_url, max_retries=6, retry_delay=5):
    if not img_url:
        return None
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.get(img_url, timeout=5)
            response.raise_for_status()
            if not response.content:
                logging.error(f"Empty content received for image {img_url}.")
                return None
            with Image.open(BytesIO(response.content)) as img:
                text = pytesseract.image_to_string(
                    img, config="--psm 6 --oem 3", lang="rus"
                )
                return text.strip()

        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error for image {img_url}: {req_err}")
        except IOError as io_err:
            logging.error(f"IO error processing image {img_url}: {io_err}")
        except Exception as e:
            logging.error(f"General error processing image {img_url}: {e}")

        attempt += 1
        logging.info(f"Retrying ({attempt}/{max_retries}) after {retry_delay} seconds.")
        time.sleep(retry_delay)

    logging.error(
        f"Failed to extract text from image {img_url} after {max_retries} attempts."
    )
    return None


def get_type_of_work(columns):
    type_of_work = columns[5].text.strip()
    if len(type_of_work) > 12:
        return type_of_work
    else:
        type_of_work = columns[7].text.strip()
        if len(type_of_work) > 12:
            return type_of_work
