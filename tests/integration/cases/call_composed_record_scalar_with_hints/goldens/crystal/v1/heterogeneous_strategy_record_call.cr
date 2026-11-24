module Fixture_call_composed_record_scalar_with_hints_Crystal_heterogeneous_strategy_record_call
extend self
record Record0, a : Int32
def consume(value = nil); 0; end
item = Record0.new(
    1,
)
consume(value: item);
end
