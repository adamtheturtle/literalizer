module Fixture_call_binding_existing_seeded_Crystal_call
extend self
class ReceiverEvents
  @@index = 0
  def self.observe(actual : Int)
    expected = [1, 42, 1, 42, 1, 142]
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
def verify_events
  ReceiverEvents.verify
end
my_data = 42
make_widget(count: my_data);
my_data = make_widget(count: my_data)
make_widget(count: my_data);
verify_events();
end
