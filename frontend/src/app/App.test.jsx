import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { fetchHealth } from "../api/health.js";
import App from "./App.jsx";

vi.mock("../api/health.js", () => ({
  fetchHealth: vi.fn(),
}));

describe("App", () => {
  beforeEach(() => {
    fetchHealth.mockReset();
  });

  it("renders the frontend foundation", () => {
    render(<App />);

    expect(
      screen.getByRole("heading", { name: "Pathwise" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Frontend foundation is running."),
    ).toBeInTheDocument();
  });

  it("displays a successful Backend health result", async () => {
    fetchHealth.mockResolvedValue({ status: "ok" });
    render(<App />);

    fireEvent.click(
      screen.getByRole("button", { name: "Check backend health" }),
    );

    expect(await screen.findByText("Backend health: ok")).toBeInTheDocument();
  });

  it("displays an error when the health request fails", async () => {
    fetchHealth.mockRejectedValue(new Error("Backend unavailable"));
    render(<App />);

    fireEvent.click(
      screen.getByRole("button", { name: "Check backend health" }),
    );

    expect(
      await screen.findByText("Backend health: error"),
    ).toBeInTheDocument();
  });
});
