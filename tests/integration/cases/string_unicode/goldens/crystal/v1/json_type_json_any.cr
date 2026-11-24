require "json"
module Fixture_string_unicode_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    "café",
    "中文",
    "😀"
]))
end
