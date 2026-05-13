"""
Final screenshot script: Take meaningful partial screenshots of each page.
- For short pages (< 20cm): full_page screenshot
- For long pages: scroll to different sections and take viewport screenshots
- Patients: top section (header+table with a few rows), then scroll down for more content
"""
import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
import os

SCREENSHOTS_DIR = 'grad_doc/screenshots'
DOC_WIDTH_CM = 18.25
MAX_DOC_HEIGHT_CM = 20.0

def calc_max_px_height(img_width):
    scale = DOC_WIDTH_CM / img_width
    return int(MAX_DOC_HEIGHT_CM / scale)

def split_full_page(img_path, output_prefix):
    """Split a full_page screenshot into segments each ≤ MAX_DOC_HEIGHT_CM."""
    full_img = Image.open(img_path)
    w, h = full_img.width, full_img.height
    max_px = calc_max_px_height(w)
    if h <= max_px:
        full_img.save(os.path.join(SCREENSHOTS_DIR, f'{output_prefix}_1.png'))
        return 1
    segments = []
    start = 0
    while start < h:
        end = min(start + max_px, h)
        segment = full_img.crop((0, start, w, end))
        segments.append(segment)
        start = end
    for i, seg in enumerate(segments):
        seg.save(os.path.join(SCREENSHOTS_DIR, f'{output_prefix}_{i+1}.png'))
    return len(segments)

async def login(page):
    await page.goto('http://localhost:5173/login')
    await page.wait_for_timeout(2000)
    await page.fill('input[placeholder="请输入账号"]', 'admin')
    await page.fill('input[placeholder="请输入密码"]', 'admin123')
    await page.click('button:has-text("登录系统")')
    await page.wait_for_timeout(3000)

async def main():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # === Auth context ===
        auth_ctx = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await auth_ctx.new_page()
        await login(page)
        print('Logged in.')

        # --- 1. Homepage (full_page, split) ---
        await page.goto('http://localhost:5173/')
        await page.wait_for_timeout(2000)
        fp = os.path.join(SCREENSHOTS_DIR, 'full_homepage.png')
        await page.screenshot(path=fp, full_page=True)
        n = split_full_page(fp, 'final_homepage')
        print(f'1. Homepage → {n} parts')

        # --- 2. Recommendation (full_page, split) ---
        await page.goto('http://localhost:5173/recommendation')
        await page.wait_for_timeout(3000)
        fp = os.path.join(SCREENSHOTS_DIR, 'full_recommendation.png')
        await page.screenshot(path=fp, full_page=True)
        n = split_full_page(fp, 'final_recommendation')
        print(f'2. Recommendation → {n} parts')

        # --- 3. Patients (viewport shots at different scroll positions) ---
        await page.goto('http://localhost:5173/patients')
        await page.wait_for_timeout(3000)

        # Part 1: top of page (header + search + first few table rows)
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'final_patients_1.png'))
        print('3a. Patients top section')

        # Part 2: scroll down to show more table content
        await page.evaluate('window.scrollTo(0, 450)')
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'final_patients_2.png'))
        print('3b. Patients scrolled section')

        # --- 4. Privacy Config (full_page, split) ---
        await page.goto('http://localhost:5173/privacy')
        await page.wait_for_timeout(3000)
        fp = os.path.join(SCREENSHOTS_DIR, 'full_privacy.png')
        await page.screenshot(path=fp, full_page=True)
        n = split_full_page(fp, 'final_privacy')
        print(f'4. Privacy → {n} parts')

        # --- 5. Visualization (3 views, each cropped nav+split) ---
        await page.goto('http://localhost:5173/visualization')
        await page.wait_for_timeout(3000)

        nav = 60
        for view_name, button_text in [('overview', None), ('comparison', '对比分析'), ('analysis', '深度分析')]:
            if button_text:
                await page.click(f'button:has-text("{button_text}")')
                await page.wait_for_timeout(3000)
            await page.evaluate('window.scrollTo(0, 0)')
            await page.wait_for_timeout(1000)
            fp = os.path.join(SCREENSHOTS_DIR, f'full_viz_{view_name}.png')
            await page.screenshot(path=fp, full_page=True)
            img = Image.open(fp)
            max_px = calc_max_px_height(img.width)
            segments = []
            start = nav
            while start < img.height:
                end = min(start + max_px, img.height)
                seg = img.crop((0, start, img.width, end))
                segments.append(seg)
                start = end
            for i, seg in enumerate(segments):
                seg.save(os.path.join(SCREENSHOTS_DIR, f'final_viz_{view_name}_{i+1}.png'))
            print(f'5. Viz {view_name} → {len(segments)} parts')

        # --- 6. Admin (viewport shots at different positions) ---
        await page.goto('http://localhost:5173/admin')
        await page.wait_for_timeout(3000)

        # Part 1: top (dashboard stats + navigation)
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'final_admin_1.png'))
        print('6a. Admin top section')

        # Part 2: scroll down to show user management table
        await page.evaluate('window.scrollTo(0, 600)')
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'final_admin_2.png'))
        print('6b. Admin scrolled section')

        await auth_ctx.close()

        # === Unauth context ===
        unauth_ctx = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page2 = await unauth_ctx.new_page()

        # --- 7. Login page ---
        await page2.goto('http://localhost:5173/login')
        await page2.wait_for_timeout(2000)
        fp = os.path.join(SCREENSHOTS_DIR, 'full_login.png')
        await page2.screenshot(path=fp, full_page=True)
        n = split_full_page(fp, 'final_login')
        print(f'7. Login → {n} parts')

        # --- 8. Forbidden page ---
        await page2.goto('http://localhost:5173/forbidden')
        await page2.wait_for_timeout(2000)
        fp = os.path.join(SCREENSHOTS_DIR, 'full_forbidden.png')
        await page2.screenshot(path=fp, full_page=True)
        n = split_full_page(fp, 'final_forbidden')
        print(f'8. Forbidden → {n} parts')

        await unauth_ctx.close()
        await browser.close()
        print('\nAll screenshots taken!')

asyncio.run(main())