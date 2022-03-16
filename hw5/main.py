import argparse
import asyncio
import os

import aiofiles as aiofiles
import aiohttp as aiohttp

URL = 'https://picsum.photos/200/300'


async def download_image(url, session, filename):
    async with session.get(url) as response:
        async with aiofiles.open(filename, mode='wb') as f:
            await f.write(await response.read())


async def download_all(n, dir_path):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(n):
            tasks.append(asyncio.create_task(download_image(URL, session, f'{dir_path}/image_{i}.jpg')))

        return await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int)
    parser.add_argument('dir_path')
    args = parser.parse_args()
    if not os.path.exists(args.dir_path):
        os.makedirs(args.dir_path)
    asyncio.run(download_all(args.n, args.dir_path))
