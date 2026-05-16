module Fixture_record_two_shapes_Crystal_heterogeneous_strategy_record
extend self
record Record1, count : Int32, rate : Int32
record Record2, retries : Int32, timeout : Int32
record Record0, metrics : Record1, flags : Record2
my_data = Record0.new(
    Record1.new(
        100,
        50,
    ),
    Record2.new(
        3,
        30,
    ),
)
end
