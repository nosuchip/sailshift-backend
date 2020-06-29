import re
from flask import g, request
from urllib.parse import urljoin, urlparse
from pyppeteer import launch
from backend import config
from backend.db.models.prerender import Prerender
from backend.common.logger import logger


def should_prerender(url):
    # Prerender for bots
    user_agent = request.headers.get('user-agent')
    known_bots = re.compile(r'googlebot|adsbot\-google|Feedfetcher\-Google|bingbot|yandex|baiduspider|Facebot|facebookexternalhit|twitterbot|WhatsApp|Applebot|rogerbot|linkedinbot|embedly|quora link preview|showyoubot|outbrain|pinterest|slackbot|vkShare|W3C_Validator|TelegramBot', re.IGNORECASE)
    prerender_urls_rx = [re.compile(r'^document/[A-Fa-f0-9]+$')]

    match_user_agent = known_bots.match(user_agent)
    match_url = any([rx.match(url) for rx in prerender_urls_rx])

    return match_user_agent and match_url


async def render_url(url):
    html = ''
    browser = None

    try:
        print(">> launching browser")
        browser = await launch(handleSIGINT=False,
                               handleSIGTERM=False,
                               handleSIGHUP=False,
                               args=["--no-sandbox", "--disable-dev-shm-usage"]
                               )

        print(">> browser stated")

        full_url = urljoin(config.SITE_URL, url)
        path = urlparse(full_url).path
        print(">> awaiting for new page")
        page = await browser.newPage()
        print(">> opening url")

        logger.info(f'Prerendering URL {full_url}')
        await page.goto(full_url)

        print(">> awaiting for meta-ready tag")
        await page.waitForFunction('document.querySelector(`meta[name="meta-ready"][content="true"]`)')
        print(">> got meta-ready tag:")

        html = await page.evaluate('() => document.documentElement.outerHTML')

        prerender = None
        is_created = False

        try:
            prerender = g.session.query(Prerender).filter_by(path=path).one()
        except Exception:
            prerender = Prerender()
            is_created = True

        prerender.url = full_url
        prerender.path = path
        prerender.html = html

        if is_created:
            g.session.add(prerender)

        g.session.commit()
    except Exception as ex:
        logger.exception(f'render_url error: {ex}')
        logger.exception(ex)
    finally:
        if browser:
            await browser.close()

    return html
