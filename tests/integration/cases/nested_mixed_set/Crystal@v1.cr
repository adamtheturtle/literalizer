require "set"
module Fixture_nested_mixed_set_Crystal
extend self
my_data = {
    "name" => "Alice",
    "tags" => Set{true, 42, "apple"},
}
end
