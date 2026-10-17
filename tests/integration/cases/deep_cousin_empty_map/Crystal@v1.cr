module Fixture_deep_cousin_empty_map_Crystal
extend self
my_data = [
    {"outer" => {"inner" => {"x" => 1}}},
    {"outer" => {"inner" => {} of String => String}},
]
end
