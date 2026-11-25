const my_data = new Map<string, unknown>([
  // About the first dotted key.
  // About the second dotted key.
  ["dotted", new Map<string, unknown>([["first", 1], ["second", 2]])],
  ["plain", 3],  // About the plain key.
  // Before the first entry.
  // Before the second entry.
  ["entries", [new Map<string, unknown>([["name", "one"]]), new Map<string, unknown>([["name", "two"]])]],
  // Inside the table.
  ["table", new Map<string, unknown>([["inner", 4]])],
]);
export {};
