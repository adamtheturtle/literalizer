const helper: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
helper.list({ a: 1 });
export {};
