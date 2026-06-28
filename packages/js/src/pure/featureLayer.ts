/**
 * Build a FeatureLayer config object from a small options bag.
 *
 * The returned JSON can be passed to `new FeatureLayer(config)` — keeping the
 * config-building logic SDK-free and unit-testable.
 */

import { buildPopupTemplate, type FieldSpec, type PopupTemplateConfig } from "./popupTemplate";
import { simpleMarkerRenderer, type SimpleMarkerOptions, type SimpleRendererConfig } from "./renderer";

export interface FeatureLayerOptions {
  url: string;
  title?: string;
  outFields?: string[];
  /** Popup spec: a title plus the fields to show. Omit to disable popups. */
  popup?: { title: string; fields: Array<string | FieldSpec> };
  /** Simple-marker renderer options. Omit to use the SDK default renderer. */
  marker?: SimpleMarkerOptions;
}

export interface FeatureLayerConfig {
  url: string;
  title?: string;
  outFields: string[];
  popupTemplate?: PopupTemplateConfig;
  renderer?: SimpleRendererConfig;
}

export function featureLayerConfig(options: FeatureLayerOptions): FeatureLayerConfig {
  const config: FeatureLayerConfig = {
    url: options.url,
    outFields: options.outFields ?? ["*"],
  };
  if (options.title) config.title = options.title;
  if (options.popup) {
    config.popupTemplate = buildPopupTemplate(options.popup.title, options.popup.fields);
  }
  if (options.marker) {
    config.renderer = simpleMarkerRenderer(options.marker);
  }
  return config;
}
