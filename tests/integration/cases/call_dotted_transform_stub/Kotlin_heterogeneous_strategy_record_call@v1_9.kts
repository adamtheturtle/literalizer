fun process(value: Any? = null): Any? = listOf<Any?>(value)
class _TracerType { fun emit(_arg: Any? = null): Any? = listOf<Any?>(_arg) }
val tracer = _TracerType()
tracer.emit(process(value = "hello"))
tracer.emit(process(value = 42))
tracer.emit(process(value = true))
