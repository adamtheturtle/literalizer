class _ThingType { fun go(value: Any? = null): Any? = listOf<Any?>(value) }
val thing = _ThingType()
val item = intArrayOf(
    1,
    2,
)
thing.go(value = item)
