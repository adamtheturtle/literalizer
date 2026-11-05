const process: any = () => {};
const single_var: number[] = [
  4,
  5,
  6,
];
const repeated_var: number = 1;
process({ data: repeated_var, count: 1 });
process({ data: single_var, count: 0 });
process({ data: repeated_var, count: 8 });
export {};
