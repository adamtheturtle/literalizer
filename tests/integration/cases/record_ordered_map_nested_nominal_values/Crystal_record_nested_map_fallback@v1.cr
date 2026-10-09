module Fixture_record_ordered_map_nested_nominal_values_Crystal_record_nested_map_fallback
extend self
record Record1, x : Int32
record Record0, values : Hash(String, Hash(String, Nil)), flag : Bool
my_data = Record0.new(
    {
        "outer" => {
            "inner" => Record1.new(
                1,
            ),
        },
    },
    true,
)
end
