import { describe, expect, it } from "vitest";
import { simpleMarkerRenderer } from "../src/pure/renderer";

describe("simpleMarkerRenderer", () => {
  it("applies sensible defaults", () => {
    const r = simpleMarkerRenderer();
    expect(r.type).toBe("simple");
    expect(r.symbol.type).toBe("simple-marker");
    expect(r.symbol.size).toBe(8);
    expect(r.symbol.outline.width).toBe(1);
  });

  it("overrides only provided options", () => {
    const r = simpleMarkerRenderer({ color: [255, 0, 0], size: 12 });
    expect(r.symbol.color).toEqual([255, 0, 0]);
    expect(r.symbol.size).toBe(12);
    // untouched default
    expect(r.symbol.outline.color).toEqual([255, 255, 255]);
  });
});
