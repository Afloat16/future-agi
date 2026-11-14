import { describe, it, expect } from "vitest";
import { fireEvent, render, screen } from "src/utils/test-utils";
import WorkerBoundaries from "../WorkerBoundaries";
import { workerHeldBackReason } from "../readinessView";

const tool = (name, action, boundary) => ({ tool: name, action, boundary });

const WORKERS = [
  {
    worker_id: "order_lookup",
    name: "Order-lookup worker",
    binding: "separate",
    status: "partial",
    reason_code: "held_at_world_cooperative",
    reason: "Held at the world on its own channel.",
    tools: [
      tool("get_order", "POST orders.get", "allowed"),
      tool("update_order_status", "POST orders.update_status", "blocked"),
    ],
    bypassed: [],
    fix: null,
    checked_at: null,
  },
  {
    worker_id: "refund",
    name: "Refund worker",
    binding: "shared",
    status: "unavailable",
    reason_code: "shared_binding",
    reason:
      "Its calls reach the world without its name, so no limit is held for it.",
    tools: [tool("issue_refund", null, "not_enforced")],
    bypassed: [{ run_id: "r1", call_execution_id: "c1", tool: null }],
    fix: null,
    checked_at: null,
  },
];

describe("WorkerBoundaries", () => {
  it("shows one row per worker, cooperative for a held worker, and the three boundary words", () => {
    const { container } = render(<WorkerBoundaries workers={WORKERS} />);
    expect(screen.getByText("Participants and tools")).toBeInTheDocument();
    expect(screen.getAllByTestId("worker-boundary")).toHaveLength(2);
    expect(
      screen.getByText("Held at the world (cooperative)"),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        "Reached the world without its own channel in 1 recent call",
      ),
    ).toBeInTheDocument();
    fireEvent.click(
      screen.getByRole("button", { name: "Show Order-lookup worker's tools" }),
    );
    fireEvent.click(
      screen.getByRole("button", { name: "Show Refund worker's tools" }),
    );
    expect(screen.getByText("Allowed")).toBeInTheDocument();
    expect(screen.getByText("Blocked")).toBeInTheDocument();
    expect(screen.getByText("Not enforced")).toBeInTheDocument();
    expect(screen.getByText("No route")).toBeInTheDocument();
    // No false enforcement badge anywhere in what renders.
    expect(container.textContent).not.toMatch(/Enforced(?!\))/);
    expect(container.textContent.replace(/Not enforced/g, "")).not.toMatch(
      /enforced/i,
    );
  });

  it("is hidden when the contract declares no worker", () => {
    const { container } = render(<WorkerBoundaries workers={[]} />);
    expect(container.textContent).toBe("");
  });

  it("names a case held back by a worker's limits", () => {
    expect(workerHeldBackReason("worker:refund", WORKERS)).toBe(
      "Refund worker's limits are not held",
    );
    expect(workerHeldBackReason("tool_routing", WORKERS)).toBeNull();
  });
});
