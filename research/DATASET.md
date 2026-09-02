# Dataset card

Status: **planned — no benchmark dataset is frozen yet**.

## Requirements before first scored run

Document all of the following before interpreting results:

- Dataset name and version.
- Source/provenance.
- License or permission to use and redistribute.
- Whether records are synthetic, public, lab-generated or otherwise non-sensitive.
- Schema and field definitions.
- Label definition and who/what assigned labels.
- Inclusion and exclusion criteria.
- Class distribution.
- Train/tuning/evaluation split policy, if applicable.
- Deduplication and leakage controls.
- Privacy, ethics and security considerations.
- Known biases and limitations.

## Minimum record schema

The benchmark should expose only fields necessary for reproducible alert prioritization. Candidate fields may include a stable record identifier, alert type/category, timestamp or relative ordering, observable features, ground-truth priority/label, and provenance metadata.

The final schema must be documented here after the dataset is selected; this file intentionally does **not** invent fields that are not present in the source data.

## Versioning rule

Freeze and commit the dataset version or an immutable retrieval manifest before publishing benchmark results. Any later dataset change requires a new version and a new result set.