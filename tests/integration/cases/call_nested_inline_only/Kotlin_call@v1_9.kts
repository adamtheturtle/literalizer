fun f(@Suppress("UNUSED_PARAMETER") a: Any? = null, @Suppress("UNUSED_PARAMETER") b: Any? = null): Any? = null
f(a = 2, b = "hello")  // trailing note
f(a = 3, b = "world")  // another note
