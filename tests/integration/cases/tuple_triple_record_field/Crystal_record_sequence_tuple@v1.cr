module Fixture_tuple_triple_record_field_Crystal_record_sequence_tuple
extend self
record Record0, call : String, args : Tuple(Int32, String, Bool)
my_data = Record0.new(
    "send",
    {
        1,
        "email",
        true,
    },
)
end
