/**
 * Build simple renderer config objects (autocastable JSON) for point layers.
 */

export type RGBA = [number, number, number] | [number, number, number, number];

export interface SimpleMarkerOptions {
  color?: RGBA;
  size?: number;
  outlineColor?: RGBA;
  outlineWidth?: number;
}

export interface SimpleRendererConfig {
  type: "simple";
  symbol: {
    type: "simple-marker";
    color: RGBA;
    size: number;
    outline: { color: RGBA; width: number };
  };
}

const DEFAULTS: Required<SimpleMarkerOptions> = {
  color: [0, 122, 194],
  size: 8,
  outlineColor: [255, 255, 255],
  outlineWidth: 1,
};

/** Build a `simple` renderer with a `simple-marker` symbol. */
export function simpleMarkerRenderer(
  options: SimpleMarkerOptions = {},
): SimpleRendererConfig {
  const opts = { ...DEFAULTS, ...options };
  return {
    type: "simple",
    symbol: {
      type: "simple-marker",
      color: opts.color,
      size: opts.size,
      outline: { color: opts.outlineColor, width: opts.outlineWidth },
    },
  };
}
