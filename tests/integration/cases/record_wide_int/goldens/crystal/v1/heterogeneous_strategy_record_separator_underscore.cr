module Fixture_record_wide_int_Crystal_heterogeneous_strategy_record_separator_underscore
extend self
record Record0, quantity : Int32, big : Int128, ratio : Float64, label : String, ok : Bool
my_data = Record0.new(
    1_000_000,
    18446744073709551615_i128,
    2.5,
    "tag",
    true,
)
end
