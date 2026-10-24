require "json"
module Fixture_sml_negative_epoch_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    "1960-01-01T00:00:00+00:00"
]))
end
