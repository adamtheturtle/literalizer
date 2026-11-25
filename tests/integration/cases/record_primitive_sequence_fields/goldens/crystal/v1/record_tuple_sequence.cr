module Fixture_record_primitive_sequence_fields_Crystal_record_tuple_sequence
extend self
record Record0, flags : Tuple(Bool, Bool), values : Tuple(Float64, Float64), ints : Tuple(Int32, Int32), text : Tuple(String), nested_flags : Tuple(Tuple(Bool), Tuple(Bool)), nested_values : Tuple(Tuple(Float64), Tuple(Float64))
my_data = Record0.new(
    {
        true,
        false,
    },
    {
        1.5,
        -2.25,
    },
    {
        1,
        2,
    },
    {
        "a",
    },
    {
         {
            true,
        },
         {
            false,
        },
    },
    {
         {
            1.5,
        },
         {
            2.25,
        },
    },
)
end
