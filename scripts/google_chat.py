import asyncio
import logging
import os
import sys

from scripts.common import aio_wrpper

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# get environment variables from os
KEY = os.getenv("GOOGLE_CHAT_KEY")
TOKEN = os.getenv("GOOGLE_CHAT_TOKEN")
SPACE = os.getenv("GOOGLE_CHAT_SPACE")
TARGET_ENDPOINT = f"https://chat.googleapis.com/v1/spaces/{SPACE}/messages"


@aio_wrpper
async def send_message(session, message):
    async with session.post(
        TARGET_ENDPOINT,
        params={"key": KEY, "token": TOKEN},
        json={"text": message},
    ) as response:
        response = await response.json()
        logging.info("%s", response)
        return response


async def main():
    if not sys.argv[1:]:
        return None
    message = " ".join(sys.argv[1:])
    if not message:
        raise ValueError(f'메시지를 입력해주세요: python {sys.argv[0]} "메시지"')
    logging.info(await send_message(message))


if __name__ == "__main__":
    asyncio.run(main())
