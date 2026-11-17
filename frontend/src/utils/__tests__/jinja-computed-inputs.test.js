import { expect, it } from "vitest";
import { extractJinjaVariables } from "../jinjaVariables";

// Expected names also match jinja2.meta.find_undeclared_variables.
it.each([
  ["{{ records[key] }}", ["key", "records"]],
  ["{{ records[indices[selected]].name }}", ["indices", "records", "selected"]],
  ["{{ matrix[row][column] }}", ["column", "matrix", "row"]],
  ["{{ values[index + offset] }}", ["index", "offset", "values"]],
  ["{% for item in items %}{{ lookup[item.id] }}{% endfor %}", ["items", "lookup"]],
  ["{{ records['fixed'] }}", ["records"]],
])("finds all external inputs in %s", (template, expected) => {
  expect(extractJinjaVariables(template)).toEqual(expected);
});
