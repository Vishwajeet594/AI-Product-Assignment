"""Evidence collector used by `python run.py --live`.

Retrieval is intentionally separated from classification: source text/title/status is saved
before any rule or model can make a claim, making every row re-reviewable.
"""
from __future__ import annotations
import re, time
from datetime import datetime, timezone
from html import unescape
import httpx

UA = 'Composio-readiness-research/1.0 (+documentation review)'

def clean_html(html: str) -> str:
    html=re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>',' ',html,flags=re.I|re.S)
    return re.sub(r'\s+',' ',unescape(re.sub(r'<[^>]+>',' ',html))).strip()

def _excerpt(text: str) -> str:
    m=re.search(r'[^.]{0,160}(oauth|api key|access token|authentication|authorization|REST API|GraphQL)[^.]{0,240}\.',text,re.I)
    return (m.group(0) if m else text[:420]).strip()

def fetch_evidence(url: str, client: httpx.Client) -> dict:
    try:
        r=client.get(url,follow_redirects=True); text=clean_html(r.text) if 'html' in r.headers.get('content-type','') else r.text[:20000]
        title=re.search(r'<title[^>]*>(.*?)</title>',r.text,re.I|re.S)
        return {'requested_url':url,'resolved_url':str(r.url),'status':r.status_code,
                'title':clean_html(title.group(1)) if title else '', 'excerpt':_excerpt(text),
                'retrieved_at':datetime.now(timezone.utc).isoformat()}
    except Exception as e:
        return {'requested_url':url,'resolved_url':None,'status':0,'title':'','excerpt':'',
                'error':type(e).__name__,'retrieved_at':datetime.now(timezone.utc).isoformat()}

def collect(rows: list[dict], pause: float=.15) -> list[dict]:
    out=[]
    with httpx.Client(headers={'User-Agent':UA},timeout=25) as client:
        for row in rows:
            out.append({**row,'source_capture':fetch_evidence(row['evidence_url'],client)})
            time.sleep(pause)
    return out
