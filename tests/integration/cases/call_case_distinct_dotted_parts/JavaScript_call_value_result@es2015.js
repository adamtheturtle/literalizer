var a = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
const my_data = a.foo.Foo.bar({ x: [1] });
