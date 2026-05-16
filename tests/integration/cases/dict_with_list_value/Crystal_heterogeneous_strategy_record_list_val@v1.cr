module Fixture_dict_with_list_value_Crystal_heterogeneous_strategy_record_list_val
extend self
record Record0, name : String, scores : Array(Int32)
my_data = Record0.new(
    "Alice",
    [
        10,
        20,
        30,
    ],
)
end
