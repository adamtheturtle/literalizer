module Fixture_swift_record_ordered_map_parent_shapes_Crystal_record_nested_map_fallback
extend self
record Record2, x : Int32
record Record1, values : Hash(String, Nil), flag : Bool
record Record3, y : Int32
record Record0, first : Record1, second : Record1
my_data = Record0.new(
    Record1.new(
        {
            "item" => Record2.new(
                1,
            ),
        },
        true,
    ),
    Record1.new(
        {
            "item" => Record3.new(
                2,
            ),
        },
        false,
    ),
)
end
