module Fixture_record_sequence_empty_sibling_Crystal_heterogeneous_strategy_record
extend self
record Record0, x : Int32
my_data = [
    [] of Record0,
    [Record0.new(1)],
]
end
