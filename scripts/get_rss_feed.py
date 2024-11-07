import asyncio
import json
import logging
from dataclasses import asdict, dataclass
from typing import Annotated

import feedparser

from scripts.common import aio_wrpper, ensure_path

DATA_DIR = "web"
FILE_NAME = "feed.json"
DATA_PATH = f"{DATA_DIR}/{FILE_NAME}"
TARGET_URL = "https://health.chosun.com/site/data/rss/rss.xml"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@dataclass
class Feed:
    title: Annotated[str, "Title of the feed"]
    description: Annotated[str, "Description of the feed"]
    date: Annotated[str, "Date of the feed"]
    category: Annotated[str, "Category of the feed"]

    def model_dump(self) -> dict:
        return asdict(self)


@aio_wrpper
async def get_feed(session):
    async with session.get(TARGET_URL) as response:
        return await response.text()


def load_feed(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_feed(path: str, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def check_diff(previous: dict, current: dict) -> list[str]:
    new_keys = set(previous.keys()) - set(current.keys())
    return list(new_keys)


async def run() -> tuple[bool, list[str]]:
    ensure_path(DATA_DIR)
    raw_feed_txt = await get_feed()
    feed = feedparser.parse(raw_feed_txt)
    previous_response_map = load_feed(DATA_PATH)
    response_map = {}
    for entry in feed.entries:
        response_map[entry.link] = Feed(
            title=entry.title,
            description=entry.description,
            date=entry.date,
            category=entry.category,
        ).model_dump()
    new_keys = check_diff(previous_response_map, response_map)
    if new_keys:
        logging.info("New feed is detected")
        for key in new_keys:
            logging.info(f"New feed: {key}")

    save_feed(DATA_PATH, response_map)
    return bool(new_keys), new_keys


if __name__ == "__main__":
    asyncio.run(run())
