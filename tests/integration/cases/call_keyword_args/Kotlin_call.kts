val throttler = object { fun check(user_id: Any? = null, ts: Any? = null): Any? = null }
fun print(user_id: Any? = null, ts: Any? = null): Any? = null
print(throttler.check(user_id = "user_1", ts = 1000.0))
print(throttler.check(user_id = "user_2", ts = 2000.5))
