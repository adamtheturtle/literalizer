fun process(data: Any? = null): Any? = null
val my_var = 42
val my_other = 7
process(data = listOf<Any?>(mapOf<String, String>("ref" to "my_var"), 42, "static"))
process(data = listOf<Any?>(mapOf<String, String>("ref" to "my_other"), 7, "label"))
