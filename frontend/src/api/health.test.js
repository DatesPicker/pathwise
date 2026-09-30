import { afterEach, describe, expect, it, vi } from "vitest";

import { fetchHealth } from "./health.js";

describe("fetchHealth", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllEnvs();
  });

  it("returns a successful health response", async () => {
    vi.stubEnv("VITE_API_BASE_URL", "http://api.test");
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      status: 200,
      json: vi.fn().mockResolvedValue({ status: "ok" }),
    });

    await expect(fetchHealth()).resolves.toEqual({ status: "ok" });
    expect(fetchMock).toHaveBeenCalledWith(new URL("http://api.test/health"), {
      method: "GET",
    });
  });

  it("rejects a non-success HTTP response", async () => {
    vi.stubEnv("VITE_API_BASE_URL", "http://api.test");
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: false,
      status: 503,
    });

    await expect(fetchHealth()).rejects.toThrow(
      "Health request failed with status 503",
    );
  });

  it("rejects an unexpected health payload", async () => {
    vi.stubEnv("VITE_API_BASE_URL", "http://api.test");
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      status: 200,
      json: vi.fn().mockResolvedValue({ status: "unexpected" }),
    });

    await expect(fetchHealth()).rejects.toThrow(
      "Backend returned an unexpected health status",
    );
  });

  it.each([undefined, "   "])(
    "rejects missing or blank API configuration",
    async (apiBaseUrl) => {
      vi.stubEnv("VITE_API_BASE_URL", apiBaseUrl);

      await expect(fetchHealth()).rejects.toThrow(
        "VITE_API_BASE_URL is required",
      );
    },
  );
});
