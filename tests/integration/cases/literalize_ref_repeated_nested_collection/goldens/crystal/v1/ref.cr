module Fixture_literalize_ref_repeated_nested_collection_Crystal_ref
extend self
shared = [
    [1, 2],
    {"value" => 1},
]
my_data = [
    shared,
    shared,
]
end
