module Fixture_tuple_record_seq_sibling_Crystal_record_sequence_tuple
extend self
record Record0, scores : Tuple(Int32, Int32, Int32), args : Tuple(Int32, String, String, Int32)
my_data = Record0.new(
    {
        10,
        20,
        30,
    },
    {
        1,
        "email",
        "a@gmail.com",
        100,
    },
)
end
