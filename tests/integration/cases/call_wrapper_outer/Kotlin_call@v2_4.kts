fun process(value: Any? = null): Any? = listOf<Any?>(value)
fun emit(_arg: Any? = null): Any? = listOf<Any?>(_arg)
emit(process(value = 42))
