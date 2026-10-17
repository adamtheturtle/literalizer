require "json"
module Fixture_odin_bom_string_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "v": "a﻿b"
}))
end
