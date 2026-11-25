const process: any = () => {};
const emit: any = () => {};
emit(process({ value: "hello" }), true);
emit(process({ value: 42 }), false);
export {};
