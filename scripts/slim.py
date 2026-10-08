#!/usr/bin/env python3
"""Slim Synthea FHIR transaction bundles into a compact static demo dataset."""
import json, os, re, glob

SRC = os.path.expanduser("~/workspace/fhir-build/demo-gen/output/fhir")
DST = os.path.expanduser("~/workspace/fhir-build/demo-data")
os.makedirs(os.path.join(DST, "patients"), exist_ok=True)

def clean_name(s):
    return re.sub(r"\d+$", "", s or "")

def displayable(codeable):
    if not codeable:
        return "Unknown"
    if codeable.get("text"):
        return codeable["text"]
    for c in codeable.get("coding", []):
        if c.get("display"):
            return c["display"]
    return "Unknown"

def obs_value(ob):
    for k in ("valueQuantity", "valueCodeableConcept", "valueString",
              "valueBoolean", "valueInteger", "valueRatio"):
        v = ob.get(k)
        if v is None:
            continue
        if k == "valueQuantity":
            return f"{v.get('value')} {v.get('unit', '')}".strip()
        if k == "valueCodeableConcept":
            return displayable(v)
        if k == "valueRatio":
            n, d = v.get("numerator", {}), v.get("denominator", {})
            return f"{n.get('value')}/{d.get('value')}"
        return str(v)
    for comp in ob.get("component", []):
        return f"{displayable(comp.get('code'))}: {obs_value(comp)}"
    return "—"

index = []
for path in sorted(glob.glob(os.path.join(SRC, "*.json"))):
    try:
        bundle = json.load(open(path))
    except Exception:
        continue
    entries = bundle.get("entry", [])
    by_type = {}
    for e in entries:
        r = e.get("resource", {})
        by_type.setdefault(r.get("resourceType"), []).append(r)
    pats = by_type.get("Patient", [])
    if not pats:
        continue
    p = pats[0]
    names = p.get("name", [{}])[0]
    given = " ".join(clean_name(g) for g in names.get("given", []))
    family = clean_name(names.get("family", ""))
    full = f"{given} {family}".strip() or "Unknown"
    pid = p.get("id", os.path.basename(path).replace(".json", ""))

    def dt(res, *keys):
        for k in keys:
            v = res.get(k)
            if v:
                return v[:10]
        return ""

    conditions = [
        {"name": displayable(c.get("code")), "status": (c.get("clinicalStatus", {}).get("coding", [{}])[0].get("code") or "unknown"),
         "onset": dt(c, "onsetDateTime")}
        for c in by_type.get("Condition", [])[:12]
    ]
    meds = [
        {"name": displayable(m.get("medicationCodeableConcept")), "date": dt(m, "authoredOn")}
        for m in by_type.get("MedicationRequest", [])[:10]
    ]
    observations = [
        {"name": displayable(o.get("code")), "value": obs_value(o), "date": dt(o, "effectiveDateTime", "issued")}
        for o in sorted(by_type.get("Observation", []), key=lambda o: o.get("effectiveDateTime", ""), reverse=True)[:25]
    ]
    encounters = [
        {"type": displayable((e.get("type", [{}])[0])), "date": (e.get("period", {}).get("start", "")[:10])}
        for e in sorted(by_type.get("Encounter", []), key=lambda e: e.get("period", {}).get("start", ""), reverse=True)[:10]
    ]
    immunizations = [
        {"name": displayable(i.get("vaccineCode")), "date": dt(i, "occurrenceDateTime")}
        for i in by_type.get("Immunization", [])[:8]
    ]

    record = {
        "id": pid,
        "name": full,
        "gender": p.get("gender", "unknown"),
        "birthDate": p.get("birthDate", ""),
        "conditions": conditions,
        "medications": meds,
        "observations": observations,
        "encounters": encounters,
        "immunizations": immunizations,
    }
    with open(os.path.join(DST, "patients", f"{pid}.json"), "w") as f:
        json.dump(record, f)
    index.append({"id": pid, "name": full, "gender": record["gender"],
                  "birthDate": record["birthDate"],
                  "conditions": len(conditions), "medications": len(meds),
                  "observations": len(observations)})

with open(os.path.join(DST, "index.json"), "w") as f:
    json.dump(index, f)
print(f"patients: {len(index)}")
