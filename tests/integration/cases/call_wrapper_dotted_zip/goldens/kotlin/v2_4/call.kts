fun process(value: Any? = null): Any? = listOf<Any?>(value)
class _HelpersType { fun emit(_call: Any? = null, _zip: Any? = null): Any? = listOf<Any?>(_call, _zip) }
val helpers = _HelpersType()
helpers.emit(process(value = 1), 42)
