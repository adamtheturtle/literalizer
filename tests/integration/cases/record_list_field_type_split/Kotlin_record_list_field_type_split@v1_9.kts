data class Record1(val kind: String, val urgent: Boolean)
data class Record0(val entries: List<Record1>)
data class Record3(val error: String)
data class Record2(val entries: List<Record3>)
val my_data = linkedMapOf<String, Any?>(
    "left" to Record0(entries = listOf<Record1>(Record1(kind = "add", urgent = true))),
    "right" to Record2(entries = listOf<Record3>(Record3(error = "not_found"))),
)
