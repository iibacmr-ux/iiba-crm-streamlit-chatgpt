from .repo import recalc_score

def update_scores_for_all(contact_ids):
    for cid in contact_ids:
        try: recalc_score(cid)
        except: pass
