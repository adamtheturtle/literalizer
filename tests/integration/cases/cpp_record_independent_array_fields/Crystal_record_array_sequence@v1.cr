module Fixture_cpp_record_independent_array_fields_Crystal_record_array_sequence
extend self
record Record0, numbers : Array(Int32), words : Array(String)
my_data = Record0.new(
    [
        1,
    ],
    [
        "s",
    ],
)
end
