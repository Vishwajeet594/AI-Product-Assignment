def critique(row: dict) -> dict:
    c=row.get('source_capture',{}); text=(c.get('excerpt') or '').lower(); auth=row['auth_primary'].replace('_',' ')
    auth_ok=auth in text or (auth=='oauth2' and 'oauth' in text) or (auth=='api key' and 'key' in text)
    surface_ok=any(x in text for x in ('api','rest','graphql','endpoint','token')); source_ok=c.get('status',0) in range(200,400)
    score=round((.45 if source_ok else 0)+(.35 if auth_ok else 0)+(.20 if surface_ok else 0),2)
    return {'id':row['id'],'source_reachable':source_ok,'auth_evidence_supported':auth_ok,'surface_evidence_supported':surface_ok,'score':score,'needs_verification':score<.80 or row['access'] in {'partner_gated','paid_plan_required','enterprise_only','no_public_api'}}

def needs_browser_verification(row: dict) -> bool:
    return critique(row)['needs_verification']
