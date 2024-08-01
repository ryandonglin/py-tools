import urllib
import asyncio

from urllib import request,parse
from urllib.error import HTTPError,URLError


def baseHttpGet(async_open=False, url='', data=None, headers={}):
    query_str = parse.urljoin(data)
    url = f'{url}?{query_str}'
    if async_open:
        response = asyncio.run(asyncHttpGet(url, headers))
        return response
    else:
        response = coreHttpGet(url, headers)
        return response

def baseHttpPost(async_open=False, url='', data=None, content_type="application/json", headers={}):
    return


async def asyncHttpGet(url, headers):
    try:
        process = await asyncio.create_subprocess_exec(
            coreHttpGet(url, headers),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            return stdout.decode()
        else:
            return f'Error: {stderr.decode()}'
    except Exception as e:
        # Handle exceptions
        return f'Exception: {e}'

def coreHttpGet(url, headers):
    try:
        response = urllib.request.urlopen(url)
        response_data = response.read().decode('utf-8')
        return response_data
    except HTTPError as e:
        error_message = f'HTTPError: {e.code} - {e.reason}\nResponse: {e.read().decode()}'
        return error_message
    except URLError as e:
        # Handle URL errors (e.g., network problems)
        return f'URLError: {e.reason}'
    except Exception as e:
        # Handle other exceptions
        return f'Exception: {e}'

