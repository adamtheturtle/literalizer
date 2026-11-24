// Normalize native collections and record signed zeros before JSON erases them.
export function printRoundtrip(value: unknown, mapExpected: boolean): void {
  const negativeZeroPaths: Record<string, true> = {};

  function normalize(value: unknown, path: (string | number)[]): unknown {
    if (Object.is(value, -0)) {
      negativeZeroPaths[JSON.stringify(path)] = true;
    }
    if (Array.isArray(value)) {
      return value.map((entry: unknown, index) =>
        normalize(entry, [...path, index]),
      );
    }
    if (value === null || typeof value !== "object") {
      return value;
    }
    const isMap = value instanceof Map;
    if (
      mapExpected ? !isMap : Object.getPrototypeOf(value) !== Object.prototype
    ) {
      throw new Error(
        `Unexpected mapping representation at ${JSON.stringify(path)}`,
      );
    }
    const entries: Iterable<[unknown, unknown]> =
      isMap ? value.entries() : Object.entries(value);
    return Object.fromEntries(
      Array.from(entries, ([key, entry]) => {
        if (typeof key !== "string") {
          throw new Error(`Expected a string key at ${JSON.stringify(path)}`);
        }
        return [key, normalize(entry, [...path, key])];
      }),
    );
  }

  console.log(JSON.stringify({ values: normalize(value, []), negativeZeroPaths }));
}
