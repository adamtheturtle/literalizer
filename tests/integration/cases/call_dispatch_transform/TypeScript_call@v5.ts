const record_value: any = () => {};
const flush_buffer: any = () => {};
const emit: any = () => {};
emit(record_value({ value: 42 }));
flush_buffer({ count: 3 });
export {};
