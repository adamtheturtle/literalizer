module Fixture_v_empty_record_sequence_root_Crystal_heterogeneous_strategy_record
extend self
record Record0, x : Int32
my_data = [
    [] of Hash(String, Int32),
    [Record0.new(1)],
]
end
