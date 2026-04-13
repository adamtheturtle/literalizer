var process = new Proxy({}, {get: () => () => {}});
process({ value: "hello" });
process({ value: 42 });
process({ value: true });
