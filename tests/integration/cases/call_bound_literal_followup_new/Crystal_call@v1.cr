module Fixture_call_bound_literal_followup_new_Crystal_call
extend self
def make_widget(value = nil); 0; end
def consume(value = nil); 0; end
my_data = make_widget(value: 42)
consume(value: my_data);
end
