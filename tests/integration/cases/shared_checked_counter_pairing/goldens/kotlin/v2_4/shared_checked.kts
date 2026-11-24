
class Counter {
    var calls = 0
    fun accept(user: String, timestamp: Double): Boolean {
        check(user == if (calls == 0) "user_1" else "user_2")
        check(timestamp == 100.0 + calls)
        calls++
        return user == "user_1"
    }
}
var checks = 0
fun checkResult(actual: Boolean, expected: List<Any?>) {
    check(actual == expected[0])
    check(expected[1] == if (checks == 0) "first" else "second")
    checks++
}
fun main() {
    val counter = Counter()
    checkResult(counter.accept("user_1", 100.0), listOf<Any?>(true, "first"))
    checkResult(counter.accept("user_2", 101.0), listOf<Any?>(false, "second"))
    check(counter.calls == 2 && checks == 2)
}

main()
