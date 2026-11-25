const my_data: Record<string, readonly [Record<string, readonly [number]>]> = {
  "a": [{"item": [1] as const}] as const,
  "b": [{"item": [2] as const}] as const,
};
export {};
