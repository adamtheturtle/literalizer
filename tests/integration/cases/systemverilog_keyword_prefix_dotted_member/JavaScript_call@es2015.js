var thing = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
thing.first_value({ value: 1 });
