module Fixture_record_nested_empty_lists_Crystal_heterogeneous_strategy_record
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
