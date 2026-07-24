function process() {}
function emit() {}
emit(process({ value: "hello" }), "one");
emit(process({ value: 42 }), "zero");
