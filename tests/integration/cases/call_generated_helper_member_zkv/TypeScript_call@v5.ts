const obj: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
obj.ZKV({ value: 1 });
export {};
