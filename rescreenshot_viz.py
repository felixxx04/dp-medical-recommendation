"""
Re-screenshot visualization page: capture all 3 views (overview, comparison, analysis)
"""
import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image
import os

async def screenshot_visualization():
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

        # Navigate to visualization
        await page.goto('http://localhost:5173/visualization')
        await page.wait_for_timeout(3000)

        screenshots_dir = 'grad_doc/screenshots'

        # 1. Screenshot "overview" view (default)
        print('Screenshotting overview view...')
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(2000)
        await page.screenshot(path=os.path.join(screenshots_dir, 'viz_overview.png'), full_page=True)

        # 2. Click "对比分析" button to switch to comparison view
        print('Screenshotting comparison view...')
        await page.click('button:has-text("对比分析")')
        await page.wait_for_timeout(3000)  # Wait for charts to render
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(screenshots_dir, 'viz_comparison.png'), full_page=True)

        # 3. Click "深度分析" button to switch to analysis view
        print('Screenshotting analysis view...')
        await page.click('button:has-text("深度分析")')
        await page.wait_for_timeout(3000)
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(1000)
        await page.screenshot(path=os.path.join(screenshots_dir, 'viz_analysis.png'), full_page=True)

        await browser.close()

        # 4. Stitch all 3 screenshots into one composite image
        overview = Image.open(os.path.join(screenshots_dir, 'viz_overview.png'))
        comparison = Image.open(os.path.join(screenshots_dir, 'viz_comparison.png'))
        analysis = Image.open(os.path.join(screenshots_dir, 'viz_analysis.png'))

        # Crop each to show only the chart content area (skip nav bar)
        # Nav bar is about ~60px at top, so crop from 60px down
        nav_height = 60
        overview_crop = overview.crop((0, nav_height, overview.width, overview.height))
        comparison_crop = comparison.crop((0, nav_height, comparison.width, comparison.height))
        analysis_crop = analysis.crop((0, nav_height, analysis.width, analysis.height))

        # Stitch vertically with a separator
        sep_height = 40
        sep = Image.new('RGB', (overview_crop.width, sep_height), (15, 23, 42))

        total_height = overview_crop.height + sep_height + comparison_crop.height + sep_height + analysis_crop.height
        composite = Image.new('RGB', (overview_crop.width, total_height), (15, 23, 42))

        y = 0
        composite.paste(overview_crop, (0, y))
        y += overview_crop.height + sep_height
        composite.paste(comparison_crop, (0, y))
        y += comparison_crop.height + sep_height
        composite.paste(analysis_crop, (0, y))

        # Limit max height to 4000px to avoid page overflow
        max_height = 4000
        if composite.height > max_height:
            composite = composite.crop((0, 0, composite.width, max_height))

        composite.save(os.path.join(screenshots_dir, 'visualization_cropped.png'))

        for f in ['viz_overview.png', 'viz_comparison.png', 'viz_analysis.png']:
            img = Image.open(os.path.join(screenshots_dir, f))
            print(f'{f}: {img.size}')

        print(f'Composite: {composite.size}')
        print('All done!')

asyncio.run(screenshot_visualization())