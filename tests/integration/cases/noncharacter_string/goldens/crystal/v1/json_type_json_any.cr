require "json"
module Fixture_noncharacter_string_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%({
    "fffe": "￾",
    "ffff": "￿"
}))
end
