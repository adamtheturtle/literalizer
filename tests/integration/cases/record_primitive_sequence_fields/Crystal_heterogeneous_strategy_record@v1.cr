module Fixture_record_primitive_sequence_fields_Crystal_heterogeneous_strategy_record
extend self
record Record0, flags : Array(Bool), values : Array(Float64), ints : Array(Int32), text : Array(String), nested_flags : Array(Array(Bool)), nested_values : Array(Array(Float64))
my_data = Record0.new(
    [
        true,
        false,
    ],
    [
        1.5,
        -2.25,
    ],
    [
        1,
        2,
    ],
    [
        "a",
    ],
    [
        [
            true,
        ],
        [
            false,
        ],
    ],
    [
        [
            1.5,
        ],
        [
            2.25,
        ],
    ],
)
end
