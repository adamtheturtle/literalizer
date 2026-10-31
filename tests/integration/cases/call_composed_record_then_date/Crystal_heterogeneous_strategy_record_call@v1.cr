module Fixture_call_composed_record_then_date_Crystal_heterogeneous_strategy_record_call
extend self
record Record0, a : Int32
def consume(stamp = nil, value = nil); 0; end
item = Record0.new(
    1,
)
stamp = Time.utc(2001, 2, 3)
consume(stamp: stamp, value: item);
end
