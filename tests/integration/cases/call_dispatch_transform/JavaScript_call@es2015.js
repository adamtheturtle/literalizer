function record_value() {}
function flush_buffer() {}
function emit() {}
emit(record_value({ value: 42 }));
flush_buffer({ count: 3 });
