import { expect, it } from "vitest";
import { validateDatasetFilter } from "../datasetUtils";

const run = (value, operator = "equal") =>
  validateDatasetFilter([], { dataType: "number", operator, value })[0]?.value;

it.each([[0, 0], [-3, -3], ["0x10", 16], ["1e3", 1000]])(
  "preserves numeric filter value %s",
  (value, expected) => {
    expect(run([value])).toEqual([expected]);
  },
);

it.each([null, true, "", " ", "bad", Infinity])(
  "rejects an invalid numeric value %s",
  (value) => {
    expect(run([value])).toBeUndefined();
  },
);

it.each(["between", "notBetween"])("preserves %s bounds", (operator) => {
  expect(run([0, "10"], operator)).toEqual([0, 10]);
  expect(run([" ", 10], operator)).toBeUndefined();
});
