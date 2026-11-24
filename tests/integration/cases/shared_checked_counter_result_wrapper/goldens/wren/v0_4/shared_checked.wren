
class Counter {
  construct new() { _calls = 0 }
  calls { _calls }
  accept(user, timestamp) {
    if (user != (_calls == 0 ? "user_1" : "user_2") || timestamp != 100 + _calls) Fiber.abort("receiver arguments changed")
    _calls = _calls + 1
    return user == "user_1"
  }
}
var counter = Counter.new()
var checks = 0
var checkResult = Fn.new { |actual, expected|
  if (actual != expected[0] || expected[1] != (checks == 0 ? "first" : "second")) Fiber.abort("paired result changed")
  checks = checks + 1
}
checkResult.call(counter.accept("user_1", 100.0), [true, "first"])
if (counter.calls != 1 || checks != 1) Fiber.abort("calls skipped")
