module Fixture_call_ref_cpp_trivial_record_Crystal_heterogeneous_strategy_record_call
extend self
record Record0, value : Int32
def consume(value = nil); 0; end
item = Record0.new(
    1,
)
consume(value: item);
end
