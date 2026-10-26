require "json"
module Fixture_subnormal_floats_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    5.0e-324,
    -5.0e-324,
    1.0e-310
]))
end
