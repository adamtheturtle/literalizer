module Fixture_nested_maps_with_opposed_value_types_Crystal
extend self
my_data = [
    {"input" => {"name" => "alice", "city" => "paris"}, "expected" => {"count" => 1, "total" => 2}},
    {"input" => {"name" => 10, "city" => 20}, "expected" => {"count" => "done", "total" => "pending"}},
]
end
