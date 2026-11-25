module Fixture_call_wrapper_outer_Crystal_call
extend self
class ReceiverEvents
  @@index = 0
  def self.observe(actual : Int)
    expected = [1, 42, 2, 142]
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
def emit(value : Int)
  ReceiverEvents.observe(2); ReceiverEvents.observe(value)
end
def verify_events
  ReceiverEvents.verify
end
emit(process(value: 42));
verify_events();
end
