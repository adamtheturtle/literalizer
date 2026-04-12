dynamic throttler;
print(throttler.check(user_id: "user_1", ts: 1000.0))
print(throttler.check(user_id: "user_2", ts: 2000.5))
