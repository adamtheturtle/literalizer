module Fixture_cpp_record_scalar_array_value_initialization_Crystal_record_array_sequence
extend self
record Record0, numbers : Array(Int32), nested_numbers : Array(Array(Int32)), words : Array(String), flag : Bool
my_data = Record0.new(
    [
        1,
        2,
    ],
    [
        [
            3,
            4,
        ],
        [
            5,
            6,
        ],
    ],
    [
        "s",
    ],
    true,
)
end
