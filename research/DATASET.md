# Dataset card

Status: **source and target day/file selected; exact local bytes and SHA-256 not frozen yet**.

## Selected dataset

- **Name:** CIC-IDS2017 (Intrusion Detection Evaluation Dataset).
- **Publisher:** Canadian Institute for Cybersecurity, University of New Brunswick.
- **Official source:** https://www.unb.ca/cic/datasets/ids-2017.html
- **Primary reference:** I. Sharafaldin, A. H. Lashkari and A. A. Ghorbani, "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization", ICISSP 2018.
- **Availability:** the official dataset page states that labelled flows and machine-learning CSV files are publicly available for researchers and requests citation of the reference paper.
- **Data origin:** controlled/lab network traffic containing benign activity and documented attacks collected over five days in July 2017.

## Benchmark v1 target file

Benchmark v1 is preregistered against the **Tuesday generated-labelled-flows CSV**, expected as:

`Tuesday-WorkingHours.pcap_ISCX.csv`

inside `GeneratedLabelledFlows.zip`.

The official CICIDS2017 description places the SSH brute-force attack (`SSH-Patator`) on Tuesday from 14:00 to 15:00 and also includes normal activity on that day. This makes Tuesday the narrowest day-level file that contains both classes required by benchmark v1.

The exact local file is not considered frozen until its SHA-256 is recorded by the validator. If the downloaded archive exposes a materially different Tuesday filename or schema, stop and update this card before any result is interpreted.

## Benchmark v1 scope

The first benchmark intentionally uses only the subset already mapped explicitly by this repository:

- `BENIGN` -> no expected SSH brute-force alert.
- `SSH-Patator` -> expected `SSH_BRUTE_FORCE` alert.

Other CIC-IDS2017 attack labels are **excluded from benchmark v1 scoring** until the repository has an explicit, reviewed label-to-alert mapping for them. This prevents unsupported labels from being silently treated as benign.

The selected representation is the **generated labelled flows** CSV because benchmark v1 needs timestamp, source/destination IP, source/destination port, protocol and label fields. Raw packet captures are not required for this experiment.

## Required fields

The validation harness requires the following normalized fields:

- timestamp;
- source IP;
- destination IP;
- source port;
- destination port;
- protocol;
- label.

Column spelling and separators may vary; the existing CIC-IDS2017 normalization helpers are reused.

## Frozen evaluation rule

The evaluation set is fixed before results:

- exactly 100 `BENIGN` rows;
- exactly 100 `SSH-Patator` rows;
- within each class, select the 100 canonical rows with the lexicographically smallest SHA-256 values;
- evaluate the resulting 200 selected row numbers in original source order;
- bind the selection manifest to the exact dataset SHA-256.

Generate the manifest with:

```bash
python -m research.cicids2017_selection /path/to/Tuesday-WorkingHours.pcap_ISCX.csv \
  --rows-per-class 100 \
  --output research/results/evaluation_selection.json
```

## Freeze procedure

No scored result may be interpreted until all of the following are committed:

1. exact downloaded Tuesday file name;
2. SHA-256 of that local file;
3. row count and label distribution;
4. generated 200-row selection manifest;
5. exact Ollama model identifier/version or digest where available;
6. supported generation/runtime configuration used for the scored AI run.

Validate the dataset with:

```bash
python -m research.cicids2017_validate /path/to/Tuesday-WorkingHours.pcap_ISCX.csv \
  --output research/results/dataset_manifest.json
```

The validator streams metadata from a caller-provided local file and records its SHA-256. Raw CIC-IDS2017 data must **not** be committed to this repository.

## Privacy, ethics and security

CIC-IDS2017 is a public research dataset generated in a controlled environment. The benchmark must not mix it with confidential employer/client logs. Public dataset findings are evidence about this experimental setup only and are not evidence of production SOC performance.

## Known limitations

- The traffic was collected in 2017 and cannot represent all current attack techniques or modern enterprise environments.
- Lab-generated traffic differs from operational SOC telemetry.
- Benchmark v1 covers only benign versus SSH brute-force labels.
- The balanced 100/100 evaluation set is useful for method comparison but does not preserve real-world class prevalence.
- Model/version drift and local hardware can affect AI latency and outputs.
- A later benchmark version should add a second, newer dataset or a broader validated label mapping before making general claims.
