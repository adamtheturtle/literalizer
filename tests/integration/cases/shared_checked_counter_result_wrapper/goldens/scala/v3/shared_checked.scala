
object Fixture_shared_checked_counter_result_wrapper_Scala_shared_checked {
    class Counter {
        var calls = 0
        def accept(user: String, timestamp: Double): Boolean = {
            assert(user == (if (calls == 0) "user_1" else "user_2"))
            assert(timestamp == 100.0 + calls)
            calls += 1
            user == "user_1"
        }
    }
    var checks = 0
    def checkResult(actual: Boolean, expected: List[Any]): Unit = {
        assert(actual == expected(0))
        assert(expected(1) == (if (checks == 0) "first" else "second"))
        checks += 1
    }
    private val counter = new Counter
    checkResult(counter.accept("user_1", 100.0), List(true, "first"))
    assert(counter.calls == 1 && checks == 1)
}
