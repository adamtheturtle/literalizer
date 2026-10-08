module Fixture_call_ref_cpp_owning_record_Crystal_heterogeneous_strategy_record_call
extend self
record Record0, value : String
def consume(value = nil); 0; end
item = Record0.new(
    "owned",
)
consume(value: item);
end
