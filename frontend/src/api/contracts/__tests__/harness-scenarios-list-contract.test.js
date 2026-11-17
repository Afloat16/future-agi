import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("src/utils/Mixpanel", () => ({
  resetUser: vi.fn(),
}));

import axiosInstance from "src/utils/axios";
import {
  listScenarios,
  serializeScenarioParams,
} from "src/api/simulate-environments/scenarios";
import { resolveScenarioSelection } from "src/api/simulate-environments/scenarioSelection";

const JOB_ID = "7f9d0f16-9d42-48b6-9bb8-44cdb1a9c0ab";

const page = {
  count: 0,
  next: null,
  previous: null,
  total_pages: 1,
  current_page: 1,
  results: [],
  groups: [],
  group_by: "",
  fields: [],
  groupings: [],
  level_labels: {},
};

// The real app axios, with its contract request interceptor, answering from a
// stub adapter so a request that passes the contract is captured, not sent.
describe("harness scenarios list request contract", () => {
  let sent;
  let defaultAdapter;

  beforeEach(() => {
    sent = [];
    defaultAdapter = axiosInstance.defaults.adapter;
    axiosInstance.defaults.adapter = async (config) => {
      sent.push(config);
      return { data: page, status: 200, statusText: "OK", headers: {}, config };
    };
    vi.spyOn(console, "warn").mockImplementation(() => {});
  });

  afterEach(() => {
    axiosInstance.defaults.adapter = defaultAdapter;
    vi.restoreAllMocks();
  });

  it("accepts the list with paging, search, grouping, ordering, filters and readiness", async () => {
    await expect(
      listScenarios(JOB_ID, {
        page: 2,
        limit: 25,
        search: "refund",
        group_by: "accent",
        ordering: "-number",
        "persona.accent": ["Canadian", "Indian"],
        "coverage.task_not": ["cancel_order"],
        sub_goals: ["verify_identity"],
        readiness: true,
      }),
    ).resolves.toMatchObject({ results: [] });

    expect(sent).toHaveLength(1);
    const query = new URLSearchParams(serializeScenarioParams(sent[0].params));
    expect(query.get("page")).toBe("2");
    expect(query.get("group_by")).toBe("accent");
    expect(query.getAll("persona.accent")).toEqual(["Canadian", "Indian"]);
    expect(query.getAll("coverage.task_not")).toEqual(["cancel_order"]);
    expect(query.get("readiness")).toBe("true");
  });

  it("accepts the flat page walk a selection makes with group_by empty", async () => {
    await resolveScenarioSelection(JOB_ID, {
      search: "refund",
      filters: { status: ["failed"] },
      mode: "all",
    });

    expect(sent).toHaveLength(1);
    expect(sent[0].params).toMatchObject({ page: 1, limit: 100, group_by: "" });
  });

  it("refuses a query key the list does not declare", async () => {
    await expect(
      listScenarios(JOB_ID, { page: 1, not_a_param: "x" }),
    ).rejects.toMatchObject({
      message: expect.stringContaining("query contract validation failed"),
    });
    expect(sent).toHaveLength(0);
  });
});
