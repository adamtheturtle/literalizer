const process: any = () => {};
const emit: any = () => {};
emit(process({ value: "hello" }), 1);
emit(process({ value: 42 }), 0);
export {};
