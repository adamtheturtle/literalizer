fun f(ops: Any? = null): Any? = listOf<Any?>(ops)
f(ops = arrayOf(arrayOf("DEL", "b", "10"), arrayOf("ADD", "a", "x")))  // note
// next call
f(ops = arrayOf(arrayOf("ADD", "c", "y")))
