require "json"
module Fixture_bom_in_string_value_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "v": "a﻿b"
}))
end
