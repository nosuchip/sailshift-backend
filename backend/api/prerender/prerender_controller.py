from flask import g
from urllib.parse import urljoin, urlparse
from pyppeteer import launch
from backend import config
from backend.db.models.prerender import Prerender
from backend.common.logger import logger


async def render_url(url):
    browser = await launch(
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        headless=False
    )

    try:
        full_url = urljoin(config.SITE_URL, url)
        path = urlparse(full_url).path
        page = await browser.newPage()
        logger.info(f'Prerendering URL {full_url}')
        await page.goto(full_url)
        html = await page.evaluate('() => document.documentElement.outerHTML')

        prerender = Prerender()
        prerender.url = full_url
        prerender.path = path
        prerender.html = html

        g.session.add(prerender)
    except Exception as ex:
        logger.exception(f'render_url error: {ex}')
    finally:
        await browser.close()

    return html or ''
