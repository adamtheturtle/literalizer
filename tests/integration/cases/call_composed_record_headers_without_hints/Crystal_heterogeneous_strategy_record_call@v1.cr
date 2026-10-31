module Fixture_call_composed_record_headers_without_hints_Crystal_heterogeneous_strategy_record_call
extend self
record Record0, name : String, values : Array(Int32)
def consume(value = nil); 0; end
item = Record0.new(
    "first",
    [
        1,
        2,
    ],
)
consume(value: item);
end
