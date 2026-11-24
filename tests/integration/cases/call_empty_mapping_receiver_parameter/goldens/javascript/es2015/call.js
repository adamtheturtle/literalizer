var api = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
api.process({ self: {} });
