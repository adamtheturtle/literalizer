var foo = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
foo.Foo.bar({ x: [1] });
