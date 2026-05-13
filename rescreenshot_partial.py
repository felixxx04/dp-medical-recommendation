"""
Re-screenshot patients page: viewport only (not full_page), showing just a portion of the table.
Also re-screenshot admin page: viewport only (was split unnecessarily).
"""
import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
import os

SCREENSHOTS_DIR = 'grad_doc/screenshots'
MAX_DOC_HEIGHT_CM = 20.0
DOC_WIDTH_CM = 18.25

def calc_max_px_height(img_width):
    scale = DOC_WIDTH_CM / img_width
    return int(MAX_DOC_HEIGHT_CM / scale)

async def take_screenshots():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        # Login
        await page.goto('http://localhost:5173/login')
        await page.wait_for_timeout(2000)
        await page.fill('input[placeholder="请输入账号"]', 'admin')
        await page.fill('input[placeholder="请输入密码"]', 'admin123')
        await page.click('button:has-text("登录系统")')
        await page.wait_for_timeout(3000)

        # Patients - viewport only (shows header + a few table rows)
        await page.goto('http://localhost:5173/patients')
        await page.wait_for_timeout(3000)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'final_patients.png'))
        print('Patients viewport screenshot done')

        # Admin - viewport only
        await page.goto('http://localhost:5173/admin')
        await page.wait_for_timeout(3000)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'final_admin.png'))
        print('Admin viewport screenshot done')

        await browser.close()

asyncio.run(take_screenshots())
