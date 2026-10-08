class _OuterType { fun inner(outer: Any? = null, n: Any? = null): Any? = null }
val outer = _OuterType()
outer.inner(outer = 1, n = 2)
