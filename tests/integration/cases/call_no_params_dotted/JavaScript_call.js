var throttler = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
throttler.check({  });
throttler.check({  });
