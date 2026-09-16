import httpx
from datetime import datetime, timezone

def verify_url(url: str) -> dict:
    """Independent second fetch for flagged rows; a browser can replace it for JS-only docs."""
    try:
        r=httpx.get(url,headers={'User-Agent':'Composio-readiness-verifier/1.0'},timeout=25,follow_redirects=True)
        return {'url':str(r.url),'status':r.status_code,'content_type':r.headers.get('content-type',''),'checked_at':datetime.now(timezone.utc).isoformat()}
    except Exception as e:
        return {'url':url,'status':0,'error':type(e).__name__,'checked_at':datetime.now(timezone.utc).isoformat()}
