const a: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
a.foo.Foo.bar({ x: [1] });
export {};
