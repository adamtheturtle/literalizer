require "json"
module Fixture_literalize_ref_value_type_nested_object_Crystal_json_type_json_any_ref
extend self
shared = JSON.parse(%([
    1,
    2
]))
build = JSON.parse(%([
    1,
    2
]))
json_object = JSON.parse(%([
    1,
    2
]))
json_allocator = JSON.parse(%([
    1,
    2
]))
json_entries = JSON.parse(%([
    1,
    2
]))
json_entry = JSON.parse(%([
    1,
    2
]))
my_data = JSON.parse(%({
    "field": #{shared.to_json},
    "nested": [#{shared.to_json}, {}],
    "build": #{build.to_json},
    "json_object": #{json_object.to_json},
    "json_allocator": #{json_allocator.to_json},
    "json_entries": #{json_entries.to_json},
    "json_entry": #{json_entry.to_json}
}))
end
