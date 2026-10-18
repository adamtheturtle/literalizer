module Fixture_native_record_mixed_field_type_refinement_Crystal_heterogeneous_strategy_record
extend self
record Record2, value : Int32
record Record1, items : Array(Int32 | Record2)
record Record4, value : String
record Record3, items : Array(Int32 | Record4)
record Record0, first : Record1, second : Record3
my_data = Record0.new(
    Record1.new(
        [
            1,
            Record2.new(
                2,
            ),
        ],
    ),
    Record3.new(
        [
            1,
            Record4.new(
                "s",
            ),
        ],
    ),
)
end
