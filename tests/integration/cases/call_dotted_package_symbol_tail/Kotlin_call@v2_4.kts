class _HelperType { fun list(a: Any? = null): Any? = listOf<Any?>(a) }
val helper = _HelperType()
helper.list(a = 1)
