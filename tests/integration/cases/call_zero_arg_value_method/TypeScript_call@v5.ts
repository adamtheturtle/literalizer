const thing: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
thing.go({  });
export {};
