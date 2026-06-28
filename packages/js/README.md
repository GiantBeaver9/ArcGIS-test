# @arcgis-test/maps-toolkit

Reusable helpers for building web maps with the **ArcGIS Maps SDK for
JavaScript**, plus a small sample app.

The library is split in two so you can reuse the config logic anywhere:

- **`./pure`** — SDK-free builders (basemaps, popup templates, renderers,
  feature-layer configs). Pure JSON in, pure JSON out. Tested headlessly.
- **`createMapView`** — a thin factory over `@arcgis/core` that consumes those
  configs to spin up a `MapView`. Runs in the browser.

## Install

```bash
cd packages/js
npm install                 # dev deps (vite, vitest, typescript)
npm install @arcgis/core    # the SDK (peer dependency) — for the demo/app
```

`@arcgis/core` is an **optional peer dependency**: the pure helpers and the
test suite don't need it, so a plain `npm install` stays light.

## Run the demo

```bash
npm install @arcgis/core
npm run dev      # vite dev server with a live map of a sample layer
```

## Use the helpers

```ts
import { createMapView } from "@arcgis-test/maps-toolkit";

createMapView({
  container: "viewDiv",
  basemap: "topo-vector",
  center: [-118.24, 34.05],
  zoom: 10,
  layers: [
    {
      url: ".../FeatureServer/0",
      title: "Trees",
      popup: { title: "{Common_Name}", fields: ["Common_Name", "Height"] },
      marker: { color: [34, 139, 34], size: 6 },
    },
  ],
});
```

Need just the config objects (no SDK)?

```ts
import { buildPopupTemplate, simpleMarkerRenderer } from "@arcgis-test/maps-toolkit/pure";
```

## Test

```bash
npm test     # vitest, runs fully headless (node env, no SDK/WebGL)
```
