module Fixture_call_type_alias_reference_Crystal_call_external_integer
extend self
class ReceiverEvents
  @@index = 0
  def self.observe(actual : Int)
    expected = [1, 1]
    raise "receiver event changed" unless @@index < 2 && actual == expected[@@index]
    @@index += 1
  end
  def self.verify
    raise "missing receiver events" unless @@index == 2
  end
end
def process(value : Int)
  ReceiverEvents.observe(1); ReceiverEvents.observe(value)
  value + 100
end
def verify_events
  ReceiverEvents.verify
end
value = 1
process(value: value);
verify_events();
end
