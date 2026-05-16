module Fixture_record_list_of_records_Crystal_heterogeneous_strategy_record
extend self
record Record1, id : Int32, label : String
record Record0, name : String, items : Array(Record1)
my_data = Record0.new(
    "box",
    [
        Record1.new(
            1,
            "first",
        ),
        Record1.new(
            2,
            "second",
        ),
    ],
)
end
