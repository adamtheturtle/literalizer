fun f(a: Any? = null, b: Any? = null): Any? = listOf<Any?>(a, b)
// calls heading
// before call one
// first argument
f(a = 1, b = 2)  // after call one
// second argument
f(a = 3, b = 4)
// after all calls
