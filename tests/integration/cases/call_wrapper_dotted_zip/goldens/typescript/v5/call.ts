const process: any = () => {};
const helpers: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
helpers.emit(process({ value: 1 }), 42);
export {};
