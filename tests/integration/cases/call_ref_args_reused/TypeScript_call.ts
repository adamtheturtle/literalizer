const process: any = () => {};
const shared = 1;
const other = 2;
process({ data: shared, count: 1 });
process({ data: other, count: 0 });
process({ data: shared, count: 8 });
export {};
