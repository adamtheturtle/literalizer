module Fixture_call_comment_trailing_backslash_Crystal_call_zipped_integer_results
extend self
class ReceiverEvents
  @@index = 0
  def self.observe(actual : Int)
    expected = [1, 1, 2, 101, 3, 41, 1, 2, 2, 102, 3, 42]
    raise "receiver event changed" unless @@index < 12 && actual == expected[@@index]
    @@index += 1
  end
  def self.verify
    raise "missing receiver events" unless @@index == 12
  end
end
def process(value : Int)
  ReceiverEvents.observe(1); ReceiverEvents.observe(value)
  value + 100
end
def emit(actual : Int, zipped : Int)
  ReceiverEvents.observe(2); ReceiverEvents.observe(actual)
  ReceiverEvents.observe(3); ReceiverEvents.observe(zipped)
end
def verify_events
  ReceiverEvents.verify
end
emit(process(value: 1), 41);
emit(process(value: 2), 42);
verify_events();
end
