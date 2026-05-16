require "set"
module Fixture_record_container_fields_Crystal
extend self
my_data = [
    {"id" => 1, "empty_map" => {} of String => String, "int_map" => {1 => "a"}, "full_set" => Set{"x", "y"}, "empty_set" => Set(String).new},
    {"id" => 2, "empty_map" => {} of String => String, "int_map" => {1 => "b"}, "full_set" => Set{"x"}, "empty_set" => Set(String).new},
]
end
