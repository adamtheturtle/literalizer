data class Record0(val call: String, val args: Array<Any?>)
val my_data = listOf<Record0>(
    Record0(call = "send", args = arrayOf<Any?>(1, "email", "a@gmail.com", 100)),
    Record0(call = "recv", args = arrayOf<Any?>(2, "sms", "b@example.com", 200)),
)
