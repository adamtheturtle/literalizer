require "json"
module Fixture_epoch_boundary_set_Crystal_json_type_json_any
extend self
my_data = JSON.parse(%([
    "1901-12-13T20:45:51",
    "1901-12-13T20:45:52",
    "2038-01-19T03:14:07",
    "2038-01-19T03:14:08"
]))
end
