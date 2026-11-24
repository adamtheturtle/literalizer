module Fixture_record_list_field_Crystal_record_sequence_tuple
extend self
record Record1, a : Int32
record Record0, items : Tuple(Record1)
my_data = Record0.new(
    {
        Record1.new(
            1,
        ),
    },
)
end
