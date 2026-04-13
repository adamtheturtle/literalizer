var throttler = new Proxy({}, {get: () => () => {}});
var emit = new Proxy({}, {get: () => () => {}});
emit(throttler.check({ user_id: "user_1", ts: 1000.0 }));
emit(throttler.check({ user_id: "user_2", ts: 2000.5 }));
