const process: any = () => {};
const untypedValue: readonly [] = [] as const;
process({ data: [untypedValue, untypedValue] as const });
export {};
