fun process(value: Any? = null): Any? = null
class _LogType { fun emit(_arg: Any? = null): Any? = null }
val log = _LogType()
log.emit(process(value = "hello"))
log.emit(process(value = 42))
log.emit(process(value = true))
