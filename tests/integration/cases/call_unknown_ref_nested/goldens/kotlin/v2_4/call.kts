fun process(known_value: Any? = null, nested_missing: Any? = null): Any? = listOf<Any?>(known_value, nested_missing)
val known_value = true
val unknown_value = true
process(known_value = known_value, nested_missing = unknown_value)
