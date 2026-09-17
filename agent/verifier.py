"""Rendered-browser verifier for pages the HTTP collector cannot establish."""
from datetime import datetime, timezone

def verify_url(url: str) -> dict:
    """Use Playwright Chromium and report rendered title/text; never pretend a fetch is a browser."""
    checked=datetime.now(timezone.utc).isoformat()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {'url':url,'browser_verified':False,'status':None,'checked_at':checked,
                'error':'playwright_not_installed','next_action':'python -m playwright install chromium'}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            page=browser.new_page(); response=page.goto(url,wait_until='domcontentloaded',timeout=30000)
            result={'url':page.url,'browser_verified':True,'status':response.status if response else None,
                    'title':page.title(),'rendered_excerpt':page.locator('body').inner_text()[:600], 'checked_at':checked}
            browser.close(); return result
    except Exception as e:
        return {'url':url,'browser_verified':False,'status':None,'checked_at':checked,
                'error':type(e).__name__,'detail':str(e)[:500]}
