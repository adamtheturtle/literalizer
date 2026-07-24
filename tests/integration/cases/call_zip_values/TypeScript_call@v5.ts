const process: any = () => {};
const emit: any = () => {};
emit(process({ value: "hello" }), "one");
emit(process({ value: 42 }), "zero");
export {};
