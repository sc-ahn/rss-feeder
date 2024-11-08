import asyncio

from scripts import get_rss_feed, google_chat


async def main():
    _, new_keys = await get_rss_feed.run()
    for new_key in new_keys:
        await google_chat.send_message(new_key)
        await asyncio.sleep(1) # Sleep for 1 second to avoid rate limiting


if __name__ == "__main__":
    asyncio.run(main())
