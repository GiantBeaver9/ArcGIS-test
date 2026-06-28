/**
 * Basemap helpers — plain data, no SDK import, so they are trivially testable.
 */

/** Well-known Esri basemap ids usable with the Maps SDK out of the box. */
export const BASEMAPS = [
  "topo-vector",
  "streets-vector",
  "satellite",
  "hybrid",
  "gray-vector",
  "dark-gray-vector",
  "oceans",
  "osm",
  "national-geographic",
] as const;

export type BasemapId = (typeof BASEMAPS)[number];

export const DEFAULT_BASEMAP: BasemapId = "topo-vector";

/** Whether `id` is one of the known basemap ids. */
export function isValidBasemap(id: string): id is BasemapId {
  return (BASEMAPS as readonly string[]).includes(id);
}

/**
 * Resolve a basemap id, falling back to a default when missing/invalid.
 */
export function resolveBasemap(
  id?: string,
  fallback: BasemapId = DEFAULT_BASEMAP,
): BasemapId {
  return id && isValidBasemap(id) ? id : fallback;
}
