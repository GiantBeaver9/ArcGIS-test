/**
 * Build ArcGIS popup template config objects.
 *
 * Returns plain JSON that the Maps SDK accepts wherever a `PopupTemplate`
 * (or its autocast form) is expected — so this stays SDK-free and testable.
 */

export interface FieldSpec {
  fieldName: string;
  label?: string;
}

export interface PopupTemplateConfig {
  title: string;
  content: Array<{
    type: "fields";
    fieldInfos: Array<{ fieldName: string; label: string; visible: boolean }>;
  }>;
}

function normalizeField(field: string | FieldSpec): FieldSpec {
  return typeof field === "string" ? { fieldName: field } : field;
}

/**
 * Build a popup template that shows a title and a table of fields.
 *
 * @param title   popup title — may include `{FIELD}` placeholders.
 * @param fields  field names or `{ fieldName, label }` specs.
 */
export function buildPopupTemplate(
  title: string,
  fields: Array<string | FieldSpec>,
): PopupTemplateConfig {
  return {
    title,
    content: [
      {
        type: "fields",
        fieldInfos: fields.map(normalizeField).map((f) => ({
          fieldName: f.fieldName,
          label: f.label ?? f.fieldName,
          visible: true,
        })),
      },
    ],
  };
}
