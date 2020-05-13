import asyncio
import pytest
import voila.app
from pyprojroot import here
from pyppeteer import launch


class VoilaTest(voila.app.Voila):
    def listen(self):
        pass


@pytest.fixture
def calh_app():
    calh_notebook = here() / 'calh.ipynb'
    voila_args = [str(calh_notebook), '--no-browser']
    voila_app = VoilaTest.instance()
    voila_app.initialize(voila_args)
    voila_app.start()
    yield voila_app
    voila_app.stop()
    voila_app.clear_instance()


@pytest.fixture
def app(calh_app):
    return calh_app.app


@pytest.mark.gen_test
def test_app(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.code == 200


@pytest.mark.gen_test
async def test_show_example(http_client, base_url):
    browser = await launch(headless=True)
    try:
        page = await browser.newPage()
        await page.goto(base_url, {"waitUntil": ["networkidle0"]})
        await asyncio.sleep(5)
        show_example_btn_array = await page.xpath('//button[span[contains(text(), "Show example")]]')
        show_example_btn = show_example_btn_array[0]
        await show_example_btn.click()
        await asyncio.sleep(5)
        example_heatmap = await page.xpath('//div[@class="v-image__image v-image__image--cover"]')
        assert len(example_heatmap) == 1
    finally:
        await browser.close()
