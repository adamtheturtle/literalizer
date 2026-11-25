module Fixture_record_empty_nested_list_Crystal_record_sequence_tuple
extend self
record Record0, a : Tuple(Tuple(Int32, Int32), Tuple(Int32)), b : Tuple(Tuple(), Tuple(Int32))
my_data = Record0.new(
    {
         {
            1,
            2,
        },
         {
            3,
        },
    },
    {
        Tuple.new,
         {
            1,
        },
    },
)
end
