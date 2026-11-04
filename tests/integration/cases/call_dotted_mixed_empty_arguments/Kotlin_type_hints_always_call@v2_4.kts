class _ThingType { fun go(before: Any? = null, populated: Any? = null, after: Any? = null): Any? = listOf<Any?>(before, populated, after) }
val thing = _ThingType()
thing.go(before = arrayOf<Any?>(), populated = intArrayOf(1), after = arrayOf<Any?>())
thing.go(before = arrayOf("text"), populated = intArrayOf(2), after = arrayOf<Any?>())
thing.go(before = arrayOf<Any?>(), populated = arrayOf("text"), after = arrayOf<Any?>())
thing.go(before = arrayOf("text"), populated = intArrayOf(2), after = intArrayOf(3))
