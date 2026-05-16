module Fixture_dict_all_scalar_types_Crystal_heterogeneous_strategy_record_datetime_epoch
extend self
record Record0, s : String, i : Int32, f : Float64, b : Bool, n : Nil, d : String, dt : Int32, by : String
my_data = Record0.new(
    "string",
    1,
    1.5,
    true,
    nil,
    "2024-01-15",
    1705320000,
    "48656c6c6f",
)
end
