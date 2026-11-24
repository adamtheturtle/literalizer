const process: any = () => {};
process({ value: null });
process({ value: [1, 2] as const });
export {};
