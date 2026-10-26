module Fixture_call_integer_result_arithmetic_outer_Crystal_call
extend self
def make_widget(count = nil); 0; end
my_data = ((make_widget(count: 42) + # inner
 1)) * 2
end
