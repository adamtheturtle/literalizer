require 'set'
my_data = [
  {"id" => 1, "empty_map" => {}, "int_map" => {1 => "a"}, "full_set" => Set.new(["x", "y"]), "empty_set" => Set.new},
  {"id" => 2, "empty_map" => {}, "int_map" => {1 => "b"}, "full_set" => Set.new(["x"]), "empty_set" => Set.new},
]
