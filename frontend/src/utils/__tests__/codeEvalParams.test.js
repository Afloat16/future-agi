import { expect, it } from "vitest";
import { extractCodeEvaluateParams } from "../codeEvalParams";

const cases = ["python", "javascript"].flatMap((language) =>
  ["'a,b'", "'[a,b'", "'{a},b'", String.raw`"a\",b"`].map((literal) => [
    language, literal,
  ]),
);

it.each(cases)("keeps %s default %s inside one param", (language, literal) => {
  const params = `output = ${literal}, expected = 0, context = 0`;
  const code =
    language === "python"
      ? `def evaluate(${params}): pass`
      : `function evaluate({${params}}) { return true; }`;
  expect(extractCodeEvaluateParams(code, language)).toEqual(["output", "expected"]);
});

it("keeps nested generic annotations and JavaScript template defaults", () => {
  const py = "def evaluate(output: Dict[str, int], expected): pass";
  const js = "function evaluate({output = `a,b`, expected}) {}";
  expect(extractCodeEvaluateParams(py, "python")).toEqual(["output", "expected"]);
  expect(extractCodeEvaluateParams(js, "javascript")).toEqual(["output", "expected"]);
});
