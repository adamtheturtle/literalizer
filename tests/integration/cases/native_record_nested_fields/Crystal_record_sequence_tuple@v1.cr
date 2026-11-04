module Fixture_native_record_nested_fields_Crystal_record_sequence_tuple
extend self
record Record1, name : String, active : Bool
record Record2, name : String, score : Float64
record Record0, owner : Record1, members : Tuple(Record2, Record2)
my_data = Record0.new(
    Record1.new(
        "Ada",
        false,
    ),
    {
        Record2.new(
            "Ada",
            1.5,
        ),
        Record2.new(
            "Bob",
            2.5,
        ),
    },
)
end
