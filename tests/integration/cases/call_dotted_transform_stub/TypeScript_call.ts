const process: any = () => {};
const tracer: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
tracer.emit(process({ value: "hello" }));
tracer.emit(process({ value: 42 }));
tracer.emit(process({ value: true }));
export {};
