function process() {}
function emit() {}
emit(process({ value: "hello" }), {"a": 1, "b": 2});
emit(process({ value: 42 }), {"c": 3, "d": 4});
