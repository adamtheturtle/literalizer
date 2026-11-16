module Fixture_call_bound_literal_followup_new_Crystal_call
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
def make_widget(value : Int)
  ReceiverEvents.observe(1); ReceiverEvents.observe(value)
  value + 100
end
def consume(value : Int)
  ReceiverEvents.observe(2); ReceiverEvents.observe(value)
end
def verify_events
  ReceiverEvents.verify
end
my_data = make_widget(value: 42)
consume(value: my_data);
verify_events();
end
