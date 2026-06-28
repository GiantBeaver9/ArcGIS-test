/**
 * Thin factory around the ArcGIS Maps SDK for JavaScript.
 *
 * This module imports `@arcgis/core` (a peer dependency), so it only runs in
 * an app/browser context. The pure config builders it uses live in `./pure`
 * and are tested independently without the SDK.
 */

import Map from "@arcgis/core/Map";
import MapView from "@arcgis/core/views/MapView";
import FeatureLayer from "@arcgis/core/layers/FeatureLayer";

import { resolveBasemap } from "./pure/basemaps";
import { featureLayerConfig, type FeatureLayerOptions } from "./pure/featureLayer";

export interface CreateMapViewOptions {
  /** DOM node (or its id) that hosts the view. */
  container: string | HTMLDivElement;
  basemap?: string;
  center?: [number, number];
  zoom?: number;
  /** Feature layers to add, described with the pure config helpers. */
  layers?: FeatureLayerOptions[];
}

export interface CreatedMap {
  map: Map;
  view: MapView;
  layers: FeatureLayer[];
}

/**
 * Create a `MapView` with an optional set of feature layers.
 *
 * Returns the `map`, `view`, and created `layers` so callers can wire up
 * further interaction.
 */
export function createMapView(options: CreateMapViewOptions): CreatedMap {
  const layers = (options.layers ?? []).map(
    (opt) => new FeatureLayer(featureLayerConfig(opt) as never),
  );

  const map = new Map({
    basemap: resolveBasemap(options.basemap),
    layers,
  });

  const view = new MapView({
    container: options.container,
    map,
    center: options.center ?? [0, 0],
    zoom: options.zoom ?? 2,
  });

  return { map, view, layers };
}
