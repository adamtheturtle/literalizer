var foo = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
foo.class({ value: 1 });
