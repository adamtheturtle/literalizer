require "json"
module Fixture_utf8_string_sibling_lines_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    "中中中中中中中中中中中中中中中中中中中中",
    "é'é'é'é'é'é'é'é'é'é'",
    "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"
]))
end
