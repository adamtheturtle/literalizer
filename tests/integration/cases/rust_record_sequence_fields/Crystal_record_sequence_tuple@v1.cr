module Fixture_rust_record_sequence_fields_Crystal_record_sequence_tuple
extend self
record Record0, short : Array(Int32), long : Array(Int32)
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
