module Fixture_call_seeded_integer_result_binding_Crystal_collection_layout_compact_call
extend self
class ReceiverEvents
  @@index = 0
  def self.observe(actual : Int)
    expected = [2, 42, 1, 42, 2, 142]
    raise "receiver event changed" unless @@index < 6 && actual == expected[@@index]
    @@index += 1
  end
  def self.verify
    raise "missing receiver events" unless @@index == 6
  end
end
def make_widget(count : Int)
  ReceiverEvents.observe(1); ReceiverEvents.observe(count)
  count + 100
end
def consume(count : Int)
  ReceiverEvents.observe(2); ReceiverEvents.observe(count)
end
def verify_events
  ReceiverEvents.verify
end
my_data = 42
consume(count: my_data);
my_data = make_widget(count: 42)
consume(count: my_data);
verify_events();
end
