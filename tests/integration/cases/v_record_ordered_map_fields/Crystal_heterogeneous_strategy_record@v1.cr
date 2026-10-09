module Fixture_v_record_ordered_map_fields_Crystal_heterogeneous_strategy_record
extend self
record Record0, numbers : Hash(String, Int32), words : Hash(String, String), nested : Hash(String, Array(Int32)), empty : Hash(String, String), flag : Bool, nested_maps : Hash(String, Hash(String, Int32)), empty_nested_maps : Hash(String, Hash(String, String))
my_data = Record0.new(
    {
        "first" => 1,
    },
    {
        "first" => "s",
    },
    {
        "first" => [
            1,
            2,
        ],
    },
    {} of String => String,
    true,
    {
        "first" => {
            "nested" => 1,
        },
    },
    {
        "first" => {} of String => String,
    },
)
end
