class _ThingType { fun go(): Any? = listOf<Any?>() }
class _OuterType { val thing = _ThingType() }
val outer = _OuterType()
outer.thing.go()
