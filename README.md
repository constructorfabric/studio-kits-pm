# Constructor Studio Kits for Product Managers

A collection of installable [Constructor Studio](https://github.com/constructorfabric/studio)
kits for product-management work. Each kit is a self-contained package —
artifact templates, PDSL rules, checklists, workflows, deterministic
checker scripts, and a constraints contract — that lives in its own
directory under `kits/` and installs independently.

## Kits

| Kit | Directory | What it does |
|-----|-----------|--------------|
| Competitive Analysis (`compete`) | [`kits/compete/`](kits/compete/) | Evidence-first competitive research: research requests, candidate registers, company profiles and dossiers, feature taxonomies, single-frame comparison matrices with deck exports, watch reports, and a quality-loop review — every claim carrying an evidence locator, an observation date, and an explicit boundary. |
| Product Spec (`product-spec`) | [`kits/product-spec/`](kits/product-spec/) | The pre-PRD product layer: evidence-backed opportunities that frame a problem before any solution exists, use cases that specify one user goal end to end with pass/fail acceptance criteria, and a conformance-and-traceability audit — every requirement downstream traceable to a dated source. |

## Install a kit

From your Constructor Studio project, straight from GitHub:

```bash
cfs kit install constructorfabric/studio-kits-pm --kit <kit>
cfs generate-agents
```

Pin a release with `--version <tag-or-sha>`. `--kit` accepts one slug,
a comma-separated list, or `all`. For local development, install from a
clone instead:

```bash
cfs kit install --path <path-to-this-clone> --kit <kit> --install-mode copy
```

See each kit's own `README.md` and `guides/QUICKSTART.md` for usage.

## Repository conventions

- One kit per directory under `kits/<slug>/`; the repository-root
  `.cf-studio-kit.toml` is the single canonical manifest — one `[[kits]]`
  entry per kit, resource `source` paths repo-relative
  (`kits/<slug>/...`), `install_path` project-relative. `cfs` reads it to
  offer the kit selector on install.
- Every kit is self-contained: no cross-kit imports, no shared code, and
  stdlib-only scripts, so a kit can be installed without the rest of the
  repository.
- Every kit must pass `cfs validate-kits .`, `cfs kit normalize
  --dry-run . --json`, and
  `cfs pdsl validate kits/<slug>/workflows/*.md kits/<slug>/artifacts/*/rules.md`.
- CI validates all kits generically on every PR and runs each kit's own
  deterministic checks in a per-kit job.

## Contributing

Changes go through pull requests to `main`; CI must be green. When adding
a kit, add its `[[kits]]` entry to the root `.cf-studio-kit.toml`, its
row to the table above, and a per-kit job to `.github/workflows/ci.yml`
if it ships deterministic checks beyond the generic gate.

## License

Apache-2.0. See `LICENSE`; kits may carry their own `NOTICE`.
