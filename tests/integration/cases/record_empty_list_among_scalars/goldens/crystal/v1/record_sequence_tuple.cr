module Fixture_record_empty_list_among_scalars_Crystal_record_sequence_tuple
extend self
record Record0, a : Tuple(Int32, Tuple())
my_data = Record0.new(
    {
        1,
        Tuple.new,
    },
)
end
