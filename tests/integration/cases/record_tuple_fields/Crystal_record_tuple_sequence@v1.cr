module Fixture_record_tuple_fields_Crystal_record_tuple_sequence
extend self
record Record0, pair : Tuple(Int32, Int32), mixed : Tuple(Int32, String), triple : Tuple(Int32, String, Bool), nested : Tuple(Tuple(Int32, String), Tuple(Int32, Bool, Float64)), empty : Tuple(), single : Tuple(Int32), long : Tuple(Int32, Int32, Int32, Int32)
my_data = Record0.new(
    {
        1,
        2,
    },
    {
        1,
        "text",
    },
    {
        1,
        "text",
        true,
    },
    {
         {
            1,
            "text",
        },
         {
            2,
            false,
            3.5,
        },
    },
    Tuple.new,
    {
        1,
    },
    {
        1,
        2,
        3,
        4,
    },
)
end
