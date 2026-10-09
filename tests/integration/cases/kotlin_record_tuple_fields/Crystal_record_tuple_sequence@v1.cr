module Fixture_kotlin_record_tuple_fields_Crystal_record_tuple_sequence
extend self
record Record0, pair : Array(Int32), mixed : Array(Int32 | String), triple : Array(Bool | Int32 | String), nested : Array(Array(Bool | Float64 | Int32) | Array(Int32 | String)), empty : Array(Nil), single : Array(Int32), long : Array(Int32)
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
