import { describe, expect, it } from "vitest";
import {
  DEFAULT_BASEMAP,
  isValidBasemap,
  resolveBasemap,
} from "../src/pure/basemaps";

describe("basemaps", () => {
  it("validates known ids", () => {
    expect(isValidBasemap("satellite")).toBe(true);
    expect(isValidBasemap("not-a-basemap")).toBe(false);
  });

  it("resolves a valid id unchanged", () => {
    expect(resolveBasemap("hybrid")).toBe("hybrid");
  });

  it("falls back for missing or invalid ids", () => {
    expect(resolveBasemap(undefined)).toBe(DEFAULT_BASEMAP);
    expect(resolveBasemap("bogus")).toBe(DEFAULT_BASEMAP);
    expect(resolveBasemap("bogus", "oceans")).toBe("oceans");
  });
});
