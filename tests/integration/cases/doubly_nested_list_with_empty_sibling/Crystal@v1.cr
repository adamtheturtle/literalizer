module Fixture_doubly_nested_list_with_empty_sibling_Crystal
extend self
my_data = [
    [[1, 2]],
    [] of Array(Int32),
    [[3, 4]],
]
end
