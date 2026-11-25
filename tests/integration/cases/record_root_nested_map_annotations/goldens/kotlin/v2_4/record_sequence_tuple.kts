data class Record0(val x: Int)
val my_data = linkedMapOf<String, Any?>(
    "outer" to Pair(linkedMapOf<String, Any?>("inner" to Record0(x = 1)), linkedMapOf<String, Any?>("inner" to Record0(x = 2))),
)
