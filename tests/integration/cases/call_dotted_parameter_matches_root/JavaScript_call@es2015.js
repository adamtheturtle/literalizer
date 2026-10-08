var outer = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
outer.inner({ outer: 1, n: 2 });
