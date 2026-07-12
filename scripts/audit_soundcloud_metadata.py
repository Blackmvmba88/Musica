#!/usr/bin/env python3
"""Audit SoundCloud artwork and metadata completeness."""

from __future__ import annotations
import argparse, csv, json
from pathlib import Path

FIELDS = {
    "artwork": ("artwork_url", "artwork", "cover_url"),
    "genre": ("genre",),
    "description": ("description",),
    "tags": ("tag_list", "tags"),
    "bpm": ("bpm", "tempo"),
    "key": ("key_signature", "key", "musical_key"),
    "url": ("permalink_url", "url", "href"),
}

def first(row, names):
    for name in names:
        value=row.get(name)
        if value not in (None,"",[],{}):
            return value
    return ""

def load_tracks(path: Path):
    data=json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data,dict):
        for key in ("tracks","collection","items"):
            if isinstance(data.get(key),list):
                data=data[key]; break
        else: data=[data]
    return data

def audit(rows):
    gaps=[]
    for row in rows:
        title=row.get("title") or row.get("name") or "(sin título)"
        values={name:first(row,keys) for name,keys in FIELDS.items()}
        missing=[name for name,value in values.items() if not value]
        critical=[name for name in ("artwork","genre","description","url") if name in missing]
        score=max(0,100-len(critical)*18-len([x for x in missing if x not in critical])*7)
        priority="critical" if "artwork" in missing else "high" if len(critical)>=2 else "medium" if missing else "complete"
        gaps.append({
            "id":row.get("id",""),
            "title":title,
            "url":values["url"],
            "artwork_url":values["artwork"],
            "genre":values["genre"],
            "description":values["description"],
            "tags":values["tags"] if isinstance(values["tags"],str) else " ".join(values["tags"]),
            "bpm":values["bpm"],
            "key":values["key"],
            "missing_fields":" | ".join(missing),
            "completeness_score":score,
            "priority":priority,
            "playback_count":row.get("playback_count") or row.get("plays") or 0,
        })
    order={"critical":0,"high":1,"medium":2,"complete":3}
    gaps.sort(key=lambda x:(order[x["priority"]],-int(x["playback_count"] or 0),x["title"].casefold()))
    return gaps

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    fields=["id","title","url","artwork_url","genre","description","tags","bpm","key","missing_fields","completeness_score","priority","playback_count"]
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--soundcloud",default="sources/soundcloud_tracks_public.json")
    p.add_argument("--output",default="reports")
    args=p.parse_args()
    rows=load_tracks(Path(args.soundcloud))
    audited=audit(rows)
    out=Path(args.output)
    write_csv(out/"soundcloud_metadata_audit.csv",audited)
    write_csv(out/"soundcloud_repair_queue.csv",[x for x in audited if x["priority"]!="complete"])
    summary={
        "tracks":len(audited),
        "without_artwork":sum(not x["artwork_url"] for x in audited),
        "without_genre":sum(not x["genre"] for x in audited),
        "without_description":sum(not x["description"] for x in audited),
        "without_tags":sum(not x["tags"] for x in audited),
        "without_bpm":sum(not x["bpm"] for x in audited),
        "without_key":sum(not x["key"] for x in audited),
        "complete":sum(x["priority"]=="complete" for x in audited),
    }
    (out/"soundcloud_metadata_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
