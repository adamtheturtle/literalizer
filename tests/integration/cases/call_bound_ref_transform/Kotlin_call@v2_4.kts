fun f(a: Any? = null): Any? = listOf<Any?>(a)
fun repr(_arg: Any? = null): Any? = listOf<Any?>(_arg)
val ref_data = 1
repr(f(a = ref_data))
