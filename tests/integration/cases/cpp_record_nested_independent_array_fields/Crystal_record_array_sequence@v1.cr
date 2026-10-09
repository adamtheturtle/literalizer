module Fixture_cpp_record_nested_independent_array_fields_Crystal_record_array_sequence
extend self
record Record0, numbers : Array(Array(Int32)), words : Array(Array(String))
my_data = Record0.new(
    [
        [
            1,
        ],
        [
            2,
        ],
    ],
    [
        [
            "s",
        ],
        [
            "t",
        ],
    ],
)
end
