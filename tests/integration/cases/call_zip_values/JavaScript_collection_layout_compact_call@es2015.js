function process() {}
function emit() {}
emit(process({ value: "hello" }), true);
emit(process({ value: 42 }), false);
