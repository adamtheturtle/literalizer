require "json"
module Fixture_bom_string_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "x": "﻿"
}))
end
