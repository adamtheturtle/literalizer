const process: any = () => {};
const my_int = 1;
const my_bool = true;
const my_float = 3.14;
const my_list = [
  1,
  2,
  3,
];
process({ value: my_int, count: 42 });
process({ value: my_bool, count: 7 });
process({ value: my_float, count: 9 });
process({ value: my_list, count: 1 });
export {};
