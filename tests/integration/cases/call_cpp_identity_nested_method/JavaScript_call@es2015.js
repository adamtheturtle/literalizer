var outer = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
outer.thing.go({  });
