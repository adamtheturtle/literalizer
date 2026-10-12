var obj = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
obj.class({ a: 42 });
