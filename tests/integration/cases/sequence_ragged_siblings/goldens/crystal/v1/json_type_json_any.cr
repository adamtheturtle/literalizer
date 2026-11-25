require "json"
module Fixture_sequence_ragged_siblings_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    ["set_task", "web", "lint_web"],
    ["merge_pipelines"]
]))
end
