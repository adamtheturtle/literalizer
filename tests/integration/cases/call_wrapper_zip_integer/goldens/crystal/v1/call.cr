module Fixture_call_wrapper_zip_integer_Crystal_call
extend self
class ReceiverEvents
  @@index = 0
  def self.observe(actual : Int)
    expected = [1, 1, 2, 101, 3, 42]
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
def emit(actual : Int, zipped : Int)
  ReceiverEvents.observe(2); ReceiverEvents.observe(actual)
  ReceiverEvents.observe(3); ReceiverEvents.observe(zipped)
end
def verify_events
  ReceiverEvents.verify
end
emit(process(value: 1), 42);
verify_events();
end
