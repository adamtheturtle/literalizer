module Fixture_call_seeded_result_consumption_Crystal_call
extend self
def make_widget(count = nil); 0; end
def consume_widget(count = nil); 0; end
my_data = make_widget(count: 0)
consume_widget(count: my_data);
my_data = make_widget(count: 1)
consume_widget(count: my_data);
end
