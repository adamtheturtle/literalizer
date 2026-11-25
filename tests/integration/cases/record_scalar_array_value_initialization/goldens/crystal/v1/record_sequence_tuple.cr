module Fixture_record_scalar_array_value_initialization_Crystal_record_sequence_tuple
extend self
record Record0, numbers : Tuple(Int32, Int32), nested_numbers : Tuple(Tuple(Int32, Int32), Tuple(Int32, Int32)), words : Tuple(String), flag : Bool
my_data = Record0.new(
    {
        1,
        2,
    },
    {
         {
            3,
            4,
        },
         {
            5,
            6,
        },
    },
    {
        "s",
    },
    true,
)
end
