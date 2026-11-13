from std.utils.variant import Variant
comptime Value = Variant[String, Float64, Bool]
struct Counter:
    var calls: Int
    def __init__(out self):
        self.calls = 0
    def accept(mut self, user: String, timestamp: Float64) raises -> Bool:
        assert_true(user == ("user_1" if self.calls == 0 else "user_2"))
        assert_equal(timestamp, 100.0 + Float64(self.calls))
        self.calls += 1
        return user == "user_1"
from testing import assert_true, assert_equal
struct Checker:
    var calls: Int
    def __init__(out self):
        self.calls = 0
    def check_result(mut self, actual: Bool, expected: List[Value]) raises:
        assert_equal(actual, expected[0][Bool])
        assert_equal(expected[1][String], String("first" if self.calls == 0 else "second"))
        self.calls += 1
def main() raises:
    var counter = Counter()
    var checker = Checker()
    checker.check_result(counter.accept("user_1", 100.0), List([Value(True), Value(String("first"))]))
    checker.check_result(counter.accept("user_2", 101.0), List([Value(False), Value(String("second"))]))
    assert_equal(counter.calls, 2)
    assert_equal(checker.calls, 2)
