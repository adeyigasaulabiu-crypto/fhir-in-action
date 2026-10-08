# FHIR in Action: A Working Interoperability Pipeline

**Live demo:** https://adeyigasaulabiu.com/fhir/

A hands-on FHIR R4 project by **Adeyiga Saulabiu** (M.S. Healthcare Informatics, Houston, Texas).

Most healthcare informatics candidates can talk about interoperability. This project shows it: a synthetic patient population generated with Synthea, expressed as FHIR R4 resources with US Core profiles, and explored in a live viewer that runs entirely in the browser.

## What this demonstrates

- **FHIR R4 resources in practice:** Patient, Encounter, Condition, Observation, MedicationRequest, Immunization, Procedure, DiagnosticReport
- **US Core profiles and USCDI data classes**, the same ones EHR vendors certify against under the 21st Century Cures Act
- **SMART on FHIR launch flows:** standalone and EHR launch, exercised against the public HAPI FHIR test server (the same launch sequence Epic uses for third-party apps)
- **Population-scale synthetic data** with Synthea, and static-site delivery of a clinical data viewer at zero hosting cost

## The pipeline

```
Synthea  →  FHIR R4 bundles  →  FHIR REST queries  →  Static viewer
(2,325       (US Core              (Patient · Condition ·
 synthetic    profiles)             Observation · Meds)
 patients)
```

1. **Generate:** Synthea creates a realistic synthetic population with full longitudinal histories: conditions, medications, labs, encounters, immunizations.
2. **Express:** Everything is exported as FHIR R4 transaction bundles with US Core profiles applied.
3. **Query:** Resources are read the way any FHIR client would read them (`Patient`, `Condition`, `MedicationRequest`, `Observation`, `Encounter`, `Immunization`).
4. **Present:** `scripts/slim.py` compacts the bundles into a browser-friendly dataset, and `index.html` renders a searchable population viewer. Each section of a patient record maps to the FHIR REST query behind it.

## Repository structure

```
├── index.html          # The population viewer (search + patient records + case study)
├── data/
│   ├── index.json      # 334-patient searchable index
│   └── patients/       # One compact JSON record per patient
├── scripts/
│   └── slim.py         # Bundle → viewer dataset pipeline
└── README.md
```

## Run it locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

No build step, no dependencies, no server. The viewer is a single static page.

## Honest scope

This is an educational build on synthetic data. It is not connected to any real EHR and contains no real patient information. What it demonstrates is genuine: generating, querying, and presenting interoperable clinical data using the standards U.S. healthcare actually runs on.

## Author

**Adeyiga Saulabiu** — Healthcare Operations & Informatics, Houston, Texas
Portfolio: https://adeyigasaulabiu.com · LinkedIn: https://www.linkedin.com/in/adeyigasaulabiu

## License

MIT — the viewer code is free to use and adapt. Synthetic patient data was generated with [Synthea](https://github.com/synthetichealth/synthea) (Apache 2.0).
