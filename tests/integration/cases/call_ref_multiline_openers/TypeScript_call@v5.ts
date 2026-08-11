const consume: any = () => {};
const foo = 42;
consume({ items: [
  {
    "other": 1,
  },
  foo,
], mapping: {
  "left": foo,
  "other": 1,
} });
export {};
