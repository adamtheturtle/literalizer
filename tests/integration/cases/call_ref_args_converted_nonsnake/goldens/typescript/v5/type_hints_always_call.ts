const process: any = () => {};
const myVar: number[] = [
  1,
  2,
  3,
];
const myOther: number[] = [
  4,
  5,
  6,
];
process({ data: myVar, count: 42 });
process({ data: myOther, count: 7 });
export {};
