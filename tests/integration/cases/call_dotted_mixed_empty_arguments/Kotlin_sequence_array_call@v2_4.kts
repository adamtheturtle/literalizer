class _ThingType { fun go(before: Any? = null, populated: Any? = null, after: Any? = null): Any? = listOf<Any?>(before, populated, after) }
val thing = _ThingType()
thing.go(before = arrayOf<Any?>(), populated = arrayOf<Any?>(1), after = arrayOf<Any?>())
thing.go(before = arrayOf<Any?>("text"), populated = arrayOf<Any?>(2), after = arrayOf<Any?>())
thing.go(before = arrayOf<Any?>(), populated = arrayOf<Any?>("text"), after = arrayOf<Any?>())
thing.go(before = arrayOf<Any?>("text"), populated = arrayOf<Any?>(2), after = arrayOf<Any?>(3))
