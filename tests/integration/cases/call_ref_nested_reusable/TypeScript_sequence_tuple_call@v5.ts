const process: any = () => {};
const item = [
  1,
  2,
] as const;
process({ data: [item, item] as const });
export {};
