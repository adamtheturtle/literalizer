function process() {}
const my_ints = [
  1,
  2,
  3,
];
const my_strings = [
  "a",
  "b",
];
const my_empty = [];
process({ data: my_ints, count: 42 });
process({ data: my_strings, count: 7 });
process({ data: my_empty, count: 99 });
