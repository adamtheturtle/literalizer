module Fixture_call_per_element_false_Crystal_call
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
def process(data : Int)
  ReceiverEvents.observe(1); ReceiverEvents.observe(data)
  data + 100
end
def verify_events
  ReceiverEvents.verify
end
process(data: 1);
verify_events();
end
