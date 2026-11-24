module Fixture_call_followup_result_first_Crystal_call
extend self
def make_widget(first = nil, second = nil); 0; end
def consume(first = nil, second = nil); 0; end
my_data = make_widget(first: 42, second: 3)
consume(first: my_data, second: 3);
end
