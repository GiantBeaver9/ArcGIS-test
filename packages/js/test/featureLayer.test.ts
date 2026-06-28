import { describe, expect, it } from "vitest";
import { featureLayerConfig } from "../src/pure/featureLayer";

describe("featureLayerConfig", () => {
  it("defaults outFields to all", () => {
    const cfg = featureLayerConfig({ url: "https://x/FeatureServer/0" });
    expect(cfg.url).toBe("https://x/FeatureServer/0");
    expect(cfg.outFields).toEqual(["*"]);
    expect(cfg.popupTemplate).toBeUndefined();
    expect(cfg.renderer).toBeUndefined();
  });

  it("wires up popup and renderer when requested", () => {
    const cfg = featureLayerConfig({
      url: "https://x/FeatureServer/0",
      title: "Cities",
      outFields: ["NAME", "POP"],
      popup: { title: "{NAME}", fields: ["NAME", "POP"] },
      marker: { color: [255, 0, 0] },
    });

    expect(cfg.title).toBe("Cities");
    expect(cfg.outFields).toEqual(["NAME", "POP"]);
    expect(cfg.popupTemplate?.title).toBe("{NAME}");
    expect(cfg.renderer?.symbol.color).toEqual([255, 0, 0]);
  });
});
