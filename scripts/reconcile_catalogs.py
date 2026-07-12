#!/usr/bin/env python3
"""Reconcile a DistroKid catalog with a SoundCloud public track export."""

from __future__ import annotations
import argparse, csv, json, re, unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

VERSION_WORDS = {"live","remix","edit","version","instrumental","demo","acoustic","radio","mix","remaster","remastered"}

def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(c for c in value if not unicodedata.combining(c)).casefold()
    value = re.sub(r"&", " and ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())

def base_title(value: str) -> str:
    words = normalize(value).split()
    return " ".join(w for w in words if w not in VERSION_WORDS)

def load_distrokid(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out=[]
    for release in data["releases"]:
        for i, track in enumerate(release["tracks"], 1):
            out.append({"release":release["release"],"track_number":i,"title":track["title"],"artist":release.get("artist","Iyari Gomez")})
    return out

def load_soundcloud(path: Path) -> list[dict]:
    data=json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for key in ("tracks","collection","items"):
            if isinstance(data.get(key), list):
                data=data[key]; break
        else:
            data=[data]
    out=[]
    for row in data:
        title=row.get("title") or row.get("name")
        if not title: continue
        out.append({"title":title,"url":row.get("permalink_url") or row.get("url") or row.get("href",""),"id":row.get("id",""),"plays":row.get("playback_count") or row.get("plays","")})
    return out

def load_aliases(path: Path | None) -> dict[str,str]:
    aliases={}
    if path and path.exists():
        with path.open(encoding="utf-8",newline="") as f:
            for row in csv.DictReader(f):
                aliases[normalize(row["soundcloud_title"])]=normalize(row["distrokid_title"])
    return aliases

def reconcile(dk, sc, aliases, threshold=.88, gap=.04):
    by_norm=defaultdict(list)
    by_base=defaultdict(list)
    for i,row in enumerate(dk):
        by_norm[normalize(row["title"])].append(i)
        by_base[base_title(row["title"])].append(i)

    matched_dk=set(); matched_sc=set(); matches=[]; review=[]
    for si,srow in enumerate(sc):
        sn=normalize(srow["title"]); target=aliases.get(sn,sn)
        candidates=by_norm.get(target,[])
        method="alias" if sn in aliases else "exact"
        score=1.0
        if not candidates:
            candidates=by_base.get(base_title(srow["title"]),[])
            method="base_title"; score=.96
        available=[i for i in candidates if i not in matched_dk]
        if len(available)==1:
            di=available[0]
        elif len(available)>1:
            review.append({"soundcloud_title":srow["title"],"reason":"multiple exact candidates","candidates":" | ".join(dk[i]["title"] for i in available)})
            continue
        else:
            scored=sorted(((SequenceMatcher(None,target,normalize(d["title"])).ratio(),i) for i,d in enumerate(dk) if i not in matched_dk),reverse=True)
            if not scored: continue
            best,di=scored[0]; second=scored[1][0] if len(scored)>1 else 0
            if best < threshold or best-second < gap:
                if best >= threshold-.08:
                    review.append({"soundcloud_title":srow["title"],"reason":"ambiguous fuzzy match","candidates":" | ".join(f'{dk[i]["title"]} ({s:.3f})' for s,i in scored[:3])})
                continue
            method="fuzzy"; score=best
        matched_dk.add(di); matched_sc.add(si)
        matches.append({**dk[di],"soundcloud_title":srow["title"],"soundcloud_url":srow["url"],"soundcloud_plays":srow["plays"],"method":method,"score":round(score,4)})
    return matches,[sc[i] for i in range(len(sc)) if i not in matched_sc],[dk[i] for i in range(len(dk)) if i not in matched_dk],review

def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore"); w.writeheader(); w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--distrokid",default="catalog/distrokid_catalog.json")
    p.add_argument("--soundcloud",default="sources/soundcloud_tracks_public.json")
    p.add_argument("--aliases",default="config/title_aliases.csv")
    p.add_argument("--output",default="reports")
    p.add_argument("--threshold",type=float,default=.88)
    args=p.parse_args()
    dk=load_distrokid(Path(args.distrokid)); sc=load_soundcloud(Path(args.soundcloud))
    matches,only_sc,only_dk,review=reconcile(dk,sc,load_aliases(Path(args.aliases)),args.threshold)
    out=Path(args.output)
    write_csv(out/"matched.csv",matches,["release","track_number","title","artist","soundcloud_title","soundcloud_url","soundcloud_plays","method","score"])
    write_csv(out/"soundcloud_only.csv",only_sc,["title","url","id","plays"])
    write_csv(out/"distrokid_only.csv",only_dk,["release","track_number","title","artist"])
    write_csv(out/"needs_review.csv",review,["soundcloud_title","reason","candidates"])
    summary={"distrokid_tracks":len(dk),"soundcloud_tracks":len(sc),"matched":len(matches),"soundcloud_only":len(only_sc),"distrokid_only":len(only_dk),"needs_review":len(review),"match_rate_distrokid":round(len(matches)/len(dk),4) if dk else 0}
    (out/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=="__main__": main()
