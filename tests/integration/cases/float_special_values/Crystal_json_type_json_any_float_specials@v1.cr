require "json"
module Fixture_float_special_values_Crystal_json_type_json_any_float_specials
extend self
my_data = JSON.parse(%([
    Float64::INFINITY,
    -Float64::INFINITY,
    Float64::NAN
]))
end
