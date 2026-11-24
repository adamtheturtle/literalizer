module Fixture_shared_checked_counter_result_wrapper_Crystal_shared_checked
  extend self

  class Counter
    getter calls = 0
    def accept(user : String, timestamp : Float64) : Bool
      raise "receiver arguments changed" unless user == (@calls == 0 ? "user_1" : "user_2") && timestamp == 100.0 + @calls
      @calls += 1
      user == "user_1"
    end
  end
  class CheckStats
    class_property count = 0
  end
  def checkResult(actual : Bool, expected : Array(Bool | String))
    raise "paired result changed" unless actual == expected[0] && expected[1] == (CheckStats.count == 0 ? "first" : "second")
    CheckStats.count += 1
  end
  counter = Counter.new
    checkResult(counter.accept("user_1", 100.0), [true, "first"]);
  raise "calls skipped" unless counter.calls == 1 && CheckStats.count == 1
end
