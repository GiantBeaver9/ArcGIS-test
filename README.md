# ArcGIS Toolkits Monorepo

A collection of **reusable ArcGIS toolkits**, one per stack, so you can build
more tools on a shared, tested foundation. Each package lives under
`packages/` and is independently installable and testable.

| Package | Stack | Language | What it's for |
| --- | --- | --- | --- |
| [`packages/python`](packages/python) | ArcGIS API for Python | Python | Analysis, scripting & automation against ArcGIS Online / Enterprise |
| [`packages/rest`](packages/rest) | ArcGIS REST API | Python | Thin, dependency-light client for small tools, jobs & Lambdas |
| [`packages/js`](packages/js) | ArcGIS Maps SDK for JavaScript | TypeScript | Reusable web-map helpers + a sample app |

## Repository layout

```
.
├── packages/
│   ├── python/   # `arcgis_project`      — full Python API toolkit + CLI
│   ├── rest/     # `arcgis_rest`         — thin REST API client
│   └── js/       # @arcgis-test/maps-toolkit — JS/TS map helpers + demo
├── .github/workflows/ci.yml   # tests every package (Python 3.9–3.12 + Node 20)
└── LICENSE
```

## Quick start

Each package is self-contained — `cd` into it and follow its README.

```bash
# Python API toolkit
cd packages/python && pip install -e ".[dev]" && pytest

# REST client
cd packages/rest && pip install -e ".[dev]" && pytest

# JS maps toolkit
cd packages/js && npm install && npm test
```

## Design principles

- **Reusable first** — every package is a library you import, not a one-off
  script. Add new tools by composing these helpers.
- **Testable without the heavy bits** — the large/native dependencies
  (`arcgis` SDK, `@arcgis/core`) are optional, and the test suites run fully
  offline with no portal access, browser, or WebGL.
- **One concern per package** — pick the lightest stack that does the job.

## Adding a new tool

1. If it fits an existing stack, add a module + tests inside that package.
2. If it needs a new stack, create `packages/<name>/` mirroring the structure
   of an existing package and add it to the CI matrix in
   `.github/workflows/ci.yml`.

## License

MIT — see [LICENSE](LICENSE).
