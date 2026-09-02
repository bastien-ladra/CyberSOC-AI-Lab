# Dataset card

Status: **source selected; exact local file not frozen yet**.

## Selected dataset

- **Name:** CIC-IDS2017 (Intrusion Detection Evaluation Dataset).
- **Publisher:** Canadian Institute for Cybersecurity, University of New Brunswick.
- **Official source:** https://www.unb.ca/cic/datasets/ids-2017.html
- **Primary reference:** I. Sharafaldin, A. H. Lashkari and A. A. Ghorbani, "Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization", ICISSP 2018.
- **Availability:** the official dataset page states that labelled flows and machine-learning CSV files are publicly available for researchers and requests citation of the reference paper. The CIC dataset FAQ also states that its datasets may be redistributed, republished and mirrored.
- **Data origin:** controlled/lab network traffic containing benign activity and documented attacks collected over five days in July 2017.

## Benchmark v1 scope

The first benchmark intentionally uses only the subset already mapped explicitly by this repository:

- `BENIGN` -> no expected SSH brute-force alert.
- `SSH-Patator` -> expected `SSH_BRUTE_FORCE` alert.

Other CIC-IDS2017 attack labels are **excluded from benchmark v1 scoring** until the repository has an explicit, reviewed label-to-alert mapping for them. This prevents unsupported labels from being silently treated as benign.

The preferred source is the official **generated labelled flows** representation because benchmark v1 needs timestamp, source/destination IP, source/destination port, protocol and label fields. Raw packet captures are not required for this experiment.

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

## Freeze procedure

No scored result may be interpreted until all of the following are committed:

1. exact downloaded file name;
2. SHA-256 of that local file;
3. row count and label distribution;
4. inclusion/exclusion rule;
5. deterministic evaluation-split or sampling rule;
6. benchmark configuration and model/version information.

`python -m research.cicids2017_validate <local.csv> --output research/results/dataset_manifest.json`

The validator streams metadata from a caller-provided local file and records its SHA-256. Raw CIC-IDS2017 data must **not** be committed to this repository.

## Privacy, ethics and security

CIC-IDS2017 is a public research dataset generated in a controlled environment. The benchmark must not mix it with confidential employer/client logs. Public dataset findings are evidence about this experimental setup only and are not evidence of production SOC performance.

## Known limitations

- The traffic was collected in 2017 and cannot represent all current attack techniques or modern enterprise environments.
- Lab-generated traffic differs from operational SOC telemetry.
- Benchmark v1 covers only benign versus SSH brute-force labels.
- Label quality, class imbalance and source-file ordering can influence measured performance.
- A later benchmark version should add a second, newer dataset or a broader validated label mapping before making general claims.
