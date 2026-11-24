const my_data: Record<string, Record<string, readonly [number, Record<string, number>]>> = {
  "first": {"items": [1, {"value": 2}] as const},
  "second": {"items": [1, {"value": 3}] as const},
};
export {};
