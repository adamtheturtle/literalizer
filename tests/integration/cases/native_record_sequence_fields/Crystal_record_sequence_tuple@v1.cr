module Fixture_native_record_sequence_fields_Crystal_record_sequence_tuple
extend self
record Record0, short : Tuple(Int32), long : Tuple(Int32, Int32)
my_data = Record0.new(
    {
        1,
    },
    {
        1,
        2,
    },
)
end
