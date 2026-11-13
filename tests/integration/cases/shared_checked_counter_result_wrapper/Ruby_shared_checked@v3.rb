
class Counter
  attr_reader :calls
  def initialize
    @calls = 0
  end
  def accept(user, timestamp)
    raise "receiver arguments changed" unless user == (@calls == 0 ? "user_1" : "user_2") && timestamp == 100.0 + @calls
    @calls += 1
    user == "user_1"
  end
end
$checks = 0
def checkResult(actual, expected)
  raise "paired result changed" unless actual == expected[0] && expected[1] == ($checks == 0 ? "first" : "second")
  $checks += 1
end
counter = Counter.new
checkResult(counter.accept("user_1", 100.0), [true, "first"])
raise "calls skipped" unless counter.calls == 1 && $checks == 1
