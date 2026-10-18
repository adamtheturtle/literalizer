module Fixture_record_ordered_map_nested_nominal_parent_types_Crystal_record_nested_map_fallback
extend self
record Record2, x : Int32
record Record1, values : Hash(String, Hash(String, Record2)), flag : Bool
record Record4, y : String
record Record3, values : Hash(String, Hash(String, Record4)), flag : Bool
record Record0, first : Record1, second : Record3
my_data = Record0.new(
    Record1.new(
        {
            "outer" => {
                "inner" => Record2.new(
                    1,
                ),
            },
        },
        true,
    ),
    Record3.new(
        {
            "outer" => {
                "inner" => Record4.new(
                    "s",
                ),
            },
        },
        false,
    ),
)
end
