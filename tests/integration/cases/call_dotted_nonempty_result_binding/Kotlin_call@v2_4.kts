class _ThingType { fun go(value: Any? = null): Any? = listOf<Any?>(value) }
val thing = _ThingType()
val my_data = thing.go(value = intArrayOf(1))
