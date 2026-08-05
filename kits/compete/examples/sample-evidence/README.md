# Sample evidence — OpenSpec (hermetic test set)

A minimal, self-contained retained-evidence set used by the kit's examples and
CI. It mirrors the project-side layout the kit expects under `competitive/`:

```
evidence/index.tsv        # canonical EVD ledger: EVD-358 … EVD-364 + EVD-141 … EVD-144
evidence/extracts/…       # one bundle extract (seven sources) + four single-page ai-sdlc extracts
companies/COMP-073-openspec/facts.tsv   # 12-column fact ledger citing those EVD ids
request.txt               # the natural-language research request (Flow 1 input)
```

Every `EVD-###` cited by the fact ledger and by the shipped artifact examples
resolves in `evidence/index.tsv`, so the reference checks run hermetically:

```bash
python3 scripts/check_evidence.py \
  --evidence-dir examples/sample-evidence/evidence \
  --companies-dir examples/sample-evidence/companies
```

The extract and fact ledger are verbatim copies of the competitive-research
flow-example fixtures (flow 02, OpenSpec); the index is authored here — the
fixtures reference `competitive/evidence/index.tsv` but do not ship it, so
this file is its first concrete instance.
