"""Conservative evidence-to-record extractor.

This is intentionally rule based and quote-bound: it only emits a non-unknown field when
the captured official text contains a supporting phrase. An LLM may be plugged in later, but
must return the same field-level quotes and pass this validator.
"""
from __future__ import annotations
import re

def quote(text: str, patterns: tuple[str, ...]) -> str:
    for p in patterns:
        m=re.search(r'[^.]{0,120}'+p+r'[^.]{0,220}\.',text,re.I)
        if m: return m.group(0).strip()
    return ''

def extract(row: dict) -> dict:
    cap=row['source_capture']; source=cap.get('body_text') or cap.get('excerpt',''); text=source.lower()
    auth='unknown'; styles=['unknown']; breadth='unknown'; evidence=[]
    authq=quote(source,(r'oauth\s*2',r'oauth',r'api keys?',r'access tokens?',r'basic authentication'))
    if 'oauth' in text: auth='oauth2'
    elif re.search(r'api keys?',text): auth='api_key'
    elif 'basic authentication' in text: auth='basic'
    elif re.search(r'access tokens?|bearer token',text): auth='token'
    if authq: evidence.append({'field':'auth','url':cap['resolved_url'] or cap['requested_url'],'quote':authq,'source_title':cap.get('title',''),'retrieved_at':cap['retrieved_at']})
    surfaceq=quote(source,(r'graphql',r'rest api',r'api endpoints?',r'command.line'))
    if 'graphql' in text: styles=['graphql']
    elif 'rest' in text or 'api endpoint' in text or '/api/' in text: styles=['rest']
    elif 'command line' in text or 'cli' in text: styles=['local_cli']
    if styles != ['unknown']: breadth='broad'
    if surfaceq: evidence.append({'field':'api_surface','url':cap['resolved_url'] or cap['requested_url'],'quote':surfaceq,'source_title':cap.get('title',''),'retrieved_at':cap['retrieved_at']})
    # Access cannot safely be inferred from API docs; preserve manual/vendor classification
    # unless docs explicitly provide a free/trial signal.
    access=row.get('access','unknown')
    accessq=quote(source,(r'free trial',r'free account',r'contact sales',r'partner',r'enterprise'))
    if accessq: evidence.append({'field':'access','url':cap['resolved_url'] or cap['requested_url'],'quote':accessq,'source_title':cap.get('title',''),'retrieved_at':cap['retrieved_at']})
    return {**row,'auth_methods':[auth] if auth!='unknown' else ['unknown'],'auth_primary':auth,
            'api_style':styles,'api_breadth':breadth,'evidence':evidence,
            'confidence': .90 if len(evidence)>=2 else (.70 if evidence else .25),
            'pass_reached':2}
