module Fixture_special_float_std_binding_mapping_Crystal_heterogeneous_strategy_record
extend self
record Record0, nan : Float64, positive : Float64, negative : Float64
std = Record0.new(
    Float64::NAN,
    Float64::INFINITY,
    -Float64::INFINITY,
)
end
