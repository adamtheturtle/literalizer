module Fixture_call_followup_result_last_Crystal_call
extend self
def make_widget(first = nil, second = nil); 0; end
def consume(first = nil, second = nil); 0; end
my_data = make_widget(first: 42, second: 3)
consume(first: 3, second: my_data);
end
