module Fixture_crystal_record_empty_nested_list_Crystal_heterogeneous_strategy_record
extend self
record Record0, a : Array(Array(Int32)), b : Array(Array(Int32))
my_data = Record0.new(
    [
        [
            1,
            2,
        ],
        [
            3,
        ],
    ],
    [
        [] of Int32,
        [
            1,
        ],
    ],
)
end
