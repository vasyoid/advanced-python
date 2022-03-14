import asyncio
import logging
import os.path

import aiohttp
import click

SITE_URL = "https://picsum.photos/512"

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class FinishedException(Exception):
    pass


async def download_image(session, path, i):
    logger.debug(f"downloading {i}-th image")
    try:
        async with session.get(SITE_URL) as img:
            logger.debug(f"saving {i}-th image")
            with open(os.path.join(path, f"{i}.jpg"), "wb") as output:
                output.write(await img.read())
            logger.debug(f"complete {i}-th image")
    except Exception as e:
        logger.error(e)


async def gather_images(path, n):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(download_image(session, path, i)) for i in range(n)]
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            logger.error(e)
    asyncio.get_running_loop().stop()


@click.command()
@click.option('-p', '--path', default=None)
@click.option('-n', '--num', default=None, type=int)
def main(path, num):
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(gather_images(path, num))
        loop.run_forever()
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    main()
