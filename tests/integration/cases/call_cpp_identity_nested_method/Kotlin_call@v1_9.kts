class _ThingType { fun go(): Any? = null }
class _OuterType { val thing = _ThingType() }
val outer = _OuterType()
outer.thing.go()
