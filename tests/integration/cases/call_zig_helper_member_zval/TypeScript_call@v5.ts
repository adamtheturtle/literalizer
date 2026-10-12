const obj: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
obj.ZVal({ value: 1 });
export {};
