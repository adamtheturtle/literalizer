module Fixture_record_ordered_map_nested_nominal_lists_Crystal_record_sequence_tuple
extend self
record Record1, x : Int32
record Record0, values : Hash(String, Tuple(Hash(String, Record1), Hash(String, Record1))), flag : Bool
my_data = Record0.new(
    {
        "entries" => {
             {
                "inner" => Record1.new(
                    1,
                ),
            },
             {
                "inner" => Record1.new(
                    2,
                ),
            },
        },
    },
    true,
)
end
