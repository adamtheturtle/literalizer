require "json"
module Fixture_toml_negative_integer_zero_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "value": -0.0
}))
end
