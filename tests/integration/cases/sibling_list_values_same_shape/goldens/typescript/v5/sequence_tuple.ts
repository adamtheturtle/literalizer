const my_data: Record<string, readonly [number, readonly [string, string]]> = {
  "test": [5, ["compile", "test"] as const] as const,
  "package": [7, ["link", "test"] as const] as const,
};
export {};
