data class Record0(val call: String, val args: List<Any?>)
val my_data = listOf<Any?>(
    Record0(call = "send", args = listOf<Any?>(1, "email", "a@gmail.com", 100)),
    Record0(call = "recv", args = listOf<Any?>(2, "sms", "b@example.com", 200)),
)
