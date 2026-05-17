module Fixture_dict_mixed_int_widths_Crystal_heterogeneous_strategy_record
extend self
record Record0, a : Int32, b : Int64, c : String
my_data = Record0.new(
    1,
    3000000000,
    "x",
)
end
