module Fixture_call_seeded_integer_result_binding_Crystal_call
extend self
def make_widget(count = nil); 0; end
def consume(count = nil); 0; end
my_data = make_widget(count: 42)
consume(count: my_data);
my_data = make_widget(count: 42)
consume(count: my_data);
end
