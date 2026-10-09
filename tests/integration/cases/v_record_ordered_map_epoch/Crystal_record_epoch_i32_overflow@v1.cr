module Fixture_v_record_ordered_map_epoch_Crystal_record_epoch_i32_overflow
extend self
record Record0, values : Hash(String, Int64), flag : Bool, nested_values : Hash(String, Hash(String, Int64)), list_values : Hash(String, Array(Int64))
my_data = Record0.new(
    {
        "first" => 2208988800,
    },
    true,
    {
        "first" => {
            "nested" => 2208988800,
        },
    },
    {
        "first" => [
            2208988800,
        ],
    },
)
end
