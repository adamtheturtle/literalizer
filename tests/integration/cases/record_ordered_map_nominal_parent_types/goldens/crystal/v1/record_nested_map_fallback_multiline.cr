module Fixture_record_ordered_map_nominal_parent_types_Crystal_record_nested_map_fallback_multiline
extend self
record Record2, x : Int32
record Record1, values : Hash(String, Record2), flag : Bool
record Record4, y : String
record Record3, values : Hash(String, Record4), flag : Bool
record Record0, first : Record1, second : Record3
my_data = Record0.new(
    Record1.new(
        {
            "item" => Record2.new(
                1,
            ),
        },
        true,
    ),
    Record3.new(
        {
            "item" => Record4.new(
                "s",
            ),
        },
        false,
    ),
)
end
