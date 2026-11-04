module Fixture_record_list_of_records_Crystal_record_sequence_tuple
extend self
record Record1, id : Int32, label : String
record Record0, name : String, items : Tuple(Record1, Record1)
my_data = Record0.new(
    "box",
    {
        Record1.new(
            1,
            "first",
        ),
        Record1.new(
            2,
            "second",
        ),
    },
)
end
