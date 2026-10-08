module Fixture_deep_list_cousin_empty_map_Crystal
extend self
my_data = [
    {"items" => [{"inner" => {"x" => 1}}, {"inner" => {} of String => String}]},
    {"items" => [{"inner" => {"x" => 2}}, {"inner" => {} of String => String}]},
]
end
