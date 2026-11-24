const process: any = () => {};
const my_var: number[] = [
  1,
  2,
  3,
];
const my_other: number[] = [
  4,
  5,
  6,
];
process({ data: my_var, count: 42 });
process({ data: my_other, count: 7 });
export {};
