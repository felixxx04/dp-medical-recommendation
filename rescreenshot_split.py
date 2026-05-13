"""
Re-screenshot all pages, splitting long pages into multiple images (max ~20cm doc height each).
Flow: Login first → screenshot all auth pages → logout → screenshot login & forbidden.
Pages to split: patients (2 parts), privacy-config (2 parts), visualization (3 views as 3 images).
Other pages: homepage, recommendation, admin - single image each.
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
        print('Logged in.')

        # --- 1. Homepage (single) ---
        await page.goto('http://localhost:5173/')
        await page.wait_for_timeout(2000)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'final_homepage.png'), full_page=True)
        print('1. Homepage done')

        # --- 2. Recommendation (single) ---
        await page.goto('http://localhost:5173/recommendation')
        await page.wait_for_timeout(3000)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'final_recommendation.png'), full_page=True)
        print('2. Recommendation done')

        # --- 3. Patients (split into 2 parts) ---
        await page.goto('http://localhost:5173/patients')
        await page.wait_for_timeout(3000)
        full_path = os.path.join(SCREENSHOTS_DIR, 'full_patients.png')
        await page.screenshot(path=full_path, full_page=True)

        full_img = Image.open(full_path)
        max_px = calc_max_px_height(full_img.width)
        part1 = full_img.crop((0, 0, full_img.width, min(max_px, full_img.height)))
        part1.save(os.path.join(SCREENSHOTS_DIR, 'final_patients_1.png'))
        if full_img.height > max_px:
            part2 = full_img.crop((0, max_px, full_img.width, min(max_px * 2, full_img.height)))
            part2.save(os.path.join(SCREENSHOTS_DIR, 'final_patients_2.png'))
        print(f'3. Patients done (split into 1-2 parts, original {full_img.height}px, max={max_px}px)')

        # --- 4. Privacy Config (split into 2 parts) ---
        await page.goto('http://localhost:5173/privacy')
        await page.wait_for_timeout(3000)
        full_path = os.path.join(SCREENSHOTS_DIR, 'full_privacy.png')
        await page.screenshot(path=full_path, full_page=True)

        full_img = Image.open(full_path)
        max_px = calc_max_px_height(full_img.width)
        part1 = full_img.crop((0, 0, full_img.width, min(max_px, full_img.height)))
        part1.save(os.path.join(SCREENSHOTS_DIR, 'final_privacy_1.png'))
        if full_img.height > max_px:
            part2 = full_img.crop((0, max_px, full_img.width, min(max_px * 2, full_img.height)))
            part2.save(os.path.join(SCREENSHOTS_DIR, 'final_privacy_2.png'))
        print(f'4. Privacy done (split into 1-2 parts, original {full_img.height}px, max={max_px}px)')

        # --- 5. Visualization (3 separate views as 3 images) ---
        await page.goto('http://localhost:5173/visualization')
        await page.wait_for_timeout(3000)

        # View 1: Overview
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'full_viz_overview.png'), full_page=True)
        img = Image.open(os.path.join(SCREENSHOTS_DIR, 'full_viz_overview.png'))
        max_px = calc_max_px_height(img.width)
        # Crop: remove nav bar (~60px)
        crop = img.crop((0, 60, img.width, min(60 + max_px, img.height)))
        crop.save(os.path.join(SCREENSHOTS_DIR, 'final_viz_overview.png'))
        print('5a. Visualization overview done')

        # View 2: Comparison
        await page.click('button:has-text("对比分析")')
        await page.wait_for_timeout(3000)
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'full_viz_comparison.png'), full_page=True)
        img = Image.open(os.path.join(SCREENSHOTS_DIR, 'full_viz_comparison.png'))
        max_px = calc_max_px_height(img.width)
        crop = img.crop((0, 60, img.width, min(60 + max_px, img.height)))
        crop.save(os.path.join(SCREENSHOTS_DIR, 'final_viz_comparison.png'))
        print('5b. Visualization comparison done')

        # View 3: Analysis
        await page.click('button:has-text("深度分析")')
        await page.wait_for_timeout(3000)
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'full_viz_analysis.png'), full_page=True)
        img = Image.open(os.path.join(SCREENSHOTS_DIR, 'full_viz_analysis.png'))
        max_px = calc_max_px_height(img.width)
        crop = img.crop((0, 60, img.width, min(60 + max_px, img.height)))
        crop.save(os.path.join(SCREENSHOTS_DIR, 'final_viz_analysis.png'))
        print('5c. Visualization analysis done')

        # --- 6. Admin Dashboard (check if needs split) ---
        await page.goto('http://localhost:5173/admin')
        await page.wait_for_timeout(3000)
        full_path = os.path.join(SCREENSHOTS_DIR, 'full_admin.png')
        await page.screenshot(path=full_path, full_page=True)

        full_img = Image.open(full_path)
        max_px = calc_max_px_height(full_img.width)
        part1 = full_img.crop((0, 0, full_img.width, min(max_px, full_img.height)))
        part1.save(os.path.join(SCREENSHOTS_DIR, 'final_admin_1.png'))
        if full_img.height > max_px:
            part2 = full_img.crop((0, max_px, full_img.width, min(max_px * 2, full_img.height)))
            part2.save(os.path.join(SCREENSHOTS_DIR, 'final_admin_2.png'))
            print(f'6. Admin done (split into 2 parts, original {full_img.height}px, max={max_px}px)')
        else:
            part1.save(os.path.join(SCREENSHOTS_DIR, 'final_admin_1.png'))
            print(f'6. Admin done (single, {full_img.height}px <= {max_px}px)')

        # --- 7. Login page (logout first) ---
        await page.evaluate("localStorage.removeItem('token'); localStorage.removeItem('user');")
        await page.goto('http://localhost:5173/login')
        await page.wait_for_timeout(2000)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'final_login.png'), full_page=True)
        print('7. Login done')

        # --- 8. Forbidden page ---
        await page.goto('http://localhost:5173/forbidden')
        await page.wait_for_timeout(2000)
        await page.screenshot(path=os.path.join(SCREENSHOTS_DIR, 'final_forbidden.png'), full_page=True)
        print('8. Forbidden done')

        await browser.close()
        print('\nAll screenshots taken!')

asyncio.run(take_screenshots())
