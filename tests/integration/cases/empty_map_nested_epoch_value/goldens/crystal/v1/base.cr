module Fixture_empty_map_nested_epoch_value_Crystal
extend self
my_data = [
    {"nested" => {"times" => ["1900-01-01T00:00:00+00:00"]}},
    {} of String => String,
]
end
