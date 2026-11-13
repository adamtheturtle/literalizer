
class Counter {
    int calls = 0
    boolean accept(String user, double timestamp) {
        assert user == (calls == 0 ? "user_1" : "user_2")
        assert timestamp == 100.0 + calls
        calls++
        return user == "user_1"
    }
}
def counter = new Counter()
int checks = 0
def checkResult = { boolean actual, List expected ->
    assert actual == expected[0]
    assert expected[1] == (checks == 0 ? "first" : "second")
    checks++
}
checkResult(counter.accept("user_1", 100.0), [true, "first"])
assert counter.calls == 1 && checks == 1
