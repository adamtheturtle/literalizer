fun process(value: Any? = null): Any? = null
class _TracerType { fun emit(_arg: Any? = null): Any? = null }
val tracer = _TracerType()
tracer.emit(process(value = "hello"))
tracer.emit(process(value = 42))
tracer.emit(process(value = true))
