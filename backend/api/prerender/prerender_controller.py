from urllib.parse import urljoin, urlparse
from pyppeteer import launch
from backend import config
from backend.db import session
from backend.db.models.prerender import Prerender


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
        print(f'Prerendering URL {full_url}')
        await page.goto(full_url)
        html = await page.evaluate('() => document.documentElement.outerHTML')

        prerender = Prerender()
        prerender.url = full_url
        prerender.path = path
        prerender.html = html

        session.add(prerender)
        session.commit()
    except Exception as ex:
        print(ex)
    finally:
        await browser.close()

    return html or ''
