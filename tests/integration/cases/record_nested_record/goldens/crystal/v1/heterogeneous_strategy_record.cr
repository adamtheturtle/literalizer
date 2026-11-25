module Fixture_record_nested_record_Crystal_heterogeneous_strategy_record
extend self
record Record1, name : String, age : Int32
record Record0, id : Int32, owner : Record1
my_data = Record0.new(
    1,
    Record1.new(
        "Alice",
        30,
    ),
)
end
