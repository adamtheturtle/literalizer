module Fixture_call_negative_int_Crystal_call
extend self
class ReceiverEvents
  @@index = 0
  def self.observe(actual : Int)
    expected = [1, -1, 1, -2, 1, -3]
    raise "receiver event changed" unless @@index < 6 && actual == expected[@@index]
    @@index += 1
  end
  def self.verify
    raise "missing receiver events" unless @@index == 6
  end
end
def process(value : Int)
  ReceiverEvents.observe(1); ReceiverEvents.observe(value)
  value + 100
end
def verify_events
  ReceiverEvents.verify
end
process(value: -1);
process(value: -2);
process(value: -3);
verify_events();
end
