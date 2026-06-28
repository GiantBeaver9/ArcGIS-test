/**
 * Public entry point for the maps toolkit.
 *
 * Re-exports the SDK-free config helpers plus the `createMapView` factory.
 * If you only need the pure helpers (e.g. in Node), import from
 * `@arcgis-test/maps-toolkit/pure` to avoid pulling in `@arcgis/core`.
 */
export * from "./pure/index";
export { createMapView } from "./createMapView";
export type { CreateMapViewOptions, CreatedMap } from "./createMapView";
