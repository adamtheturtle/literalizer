module Fixture_crystal_record_empty_list_among_scalars_Crystal_heterogeneous_strategy_record
extend self
record Record0, a : Array(Array(Nil) | Int32)
my_data = Record0.new(
    [
        1,
        [] of Nil,
    ],
)
end
