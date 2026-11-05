const my_data = new Map([
  // About the first dotted key.
  // About the second dotted key.
  ["dotted", new Map([["first", 1], ["second", 2]])],
  ["plain", 3],  // About the plain key.
  // Before the first entry.
  // Before the second entry.
  ["entries", [new Map([["name", "one"]]), new Map([["name", "two"]])]],
  // Inside the table.
  ["table", new Map([["inner", 4]])],
]);
