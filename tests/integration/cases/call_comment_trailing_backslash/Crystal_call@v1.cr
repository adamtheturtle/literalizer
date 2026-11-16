module Fixture_call_comment_trailing_backslash_Crystal_call
extend self
class ReceiverEvents
  @@index = 0
  def self.observe(actual : Int)
    expected = [1, 1, 1, 2]
    raise "receiver event changed" unless @@index < 4 && actual == expected[@@index]
    @@index += 1
  end
  def self.verify
    raise "missing receiver events" unless @@index == 4
  end
end
def process(value : Int)
  ReceiverEvents.observe(1); ReceiverEvents.observe(value)
  value + 100
end
def verify_events
  ReceiverEvents.verify
end
process(value: 1);  # trail \ .
process(value: 2);  # second
verify_events();
end
