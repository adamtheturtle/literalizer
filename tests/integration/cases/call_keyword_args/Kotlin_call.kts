val throttler = object { fun check(vararg a: Any?): Any? = null }
fun print(vararg a: Any?): Any? = null
print(throttler.check(user_id = "user_1", ts = 1000.0))
print(throttler.check(user_id = "user_2", ts = 2000.5))
