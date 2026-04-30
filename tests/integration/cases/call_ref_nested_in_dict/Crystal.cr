module Fixture_call_ref_nested_in_dict_Crystal
extend self
my_data = [
    [{"key" => {"$ref" => "my_var"}, "count" => 42}],
]
end
