const obj: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
obj.BEGIN({ a: 42 });
export {};
