module Fixture_unwrapped_record_argument_Crystal_heterogeneous_strategy_record_ref_default
extend self
record Record0, a : Int32, b : String
def consume_widget(arg_value = nil); 0; end
consume_widget(arg_value: Record0.new(
    1,
    "x",
));
end
