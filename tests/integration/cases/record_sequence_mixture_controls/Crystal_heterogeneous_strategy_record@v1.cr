module Fixture_record_sequence_mixture_controls_Crystal_heterogeneous_strategy_record
extend self
record Record0, x : Int32
my_data = [
    [[1], Record0.new(1)],
    [Record0.new(1), Record0.new(2)],
    [[] of Record0, [Record0.new(1)]],
    [[] of Nil, [] of Nil],
]
end
