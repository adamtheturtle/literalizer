var throttler = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
function emit() {}
emit(throttler.check({ user_id: "user_1", ts: 1000.0 }));
emit(throttler.check({ user_id: "user_2", ts: 2000.5 }));
