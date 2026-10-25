module Fixture_tuple_record_field_Crystal_record_sequence_tuple
extend self
record Record0, call : String, args : Tuple(Int32, String, String, Int32)
my_data = Record0.new(
    "send",
    {
        1,
        "email",
        "a@gmail.com",
        100,
    },
)
end
