module Fixture_special_float_std_binding_mapping_Crystal
extend self
std = {
    "nan" => Float64::NAN,
    "positive" => Float64::INFINITY,
    "negative" => -Float64::INFINITY,
}
end
