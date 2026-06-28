import { describe, expect, it } from "vitest";
import { buildPopupTemplate } from "../src/pure/popupTemplate";

describe("buildPopupTemplate", () => {
  it("creates a fields content block with labels defaulting to field name", () => {
    const tpl = buildPopupTemplate("{NAME}", ["NAME", { fieldName: "POP", label: "Population" }]);

    expect(tpl.title).toBe("{NAME}");
    expect(tpl.content).toHaveLength(1);

    const infos = tpl.content[0].fieldInfos;
    expect(infos).toEqual([
      { fieldName: "NAME", label: "NAME", visible: true },
      { fieldName: "POP", label: "Population", visible: true },
    ]);
  });

  it("handles an empty field list", () => {
    const tpl = buildPopupTemplate("Title", []);
    expect(tpl.content[0].fieldInfos).toEqual([]);
  });
});
