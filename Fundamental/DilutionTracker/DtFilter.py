from bs4 import BeautifulSoup as bs
from playwright.async_api import async_playwright
from models.login import login
from models.data import data
from models.rs import ReSplit

async def getDilutionData():
    # --- testing retrieve dilutiontracker data with beautifulsoup & playwright for web manuipulation
    # playwright is originally not compatible with jupyter on Window due to asyncio window policy
    # problem later solved by removing such policy in python ipykernel
    # Reference: https://github.com/microsoft/playwright-python/issues/178#issuecomment-1302895391
    # modified file: C:\Users\RONCHIBULU\AppData\Roaming\Python\Python311\site-packages\ipykernel
    async with async_playwright() as p:
        pw = await async_playwright().start()
        browser = await pw.chromium.launch_persistent_context(user_data_dir="./Fundamental/DilutionTracker/chrome-usr", headless=False, slow_mo=50)
        page = await browser.new_page()
        login_page = login(page)
        await login_page.login()
        data_page = data(page, 'IMPP')
        await data_page.getData()
        rs_page = ReSplit(page, "IMPP")
        await rs_page.getData()