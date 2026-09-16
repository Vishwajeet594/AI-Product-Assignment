def score(audit, pass1, final, fields=('auth_primary','access','api_style','buildable')):
    p1={r['id']:r for r in pass1}; fin={r['id']:r for r in final}; result={}
    for label, rows in [('baseline',p1),('final',fin)]:
        right=total=0; per={}
        for f in fields:
            tested=[a for a in audit if f in a and a['id'] in rows]; hits=sum(a[f]==rows[a['id']][f] for a in tested)
            per[f]={'hits':hits,'total':len(tested)}; right+=hits; total+=len(tested)
        result[label]={'hits':right,'total':total,'pct':round(100*right/total,1) if total else None,'by_field':per}
    return result
