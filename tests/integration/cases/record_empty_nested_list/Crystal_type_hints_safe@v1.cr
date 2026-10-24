module Fixture_record_empty_nested_list_Crystal_type_hints_safe
extend self
my_data = {
    "a" => [[1, 2], [3]],
    "b" => [[] of Int32, [1]],
}
end
