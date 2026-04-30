module Fixture_call_ref_nested_in_list_Crystal
extend self
my_data = [
    [[{"$ref" => "my_var"}, 42, "static"]],
    [[{"$ref" => "my_other"}, 7, "label"]],
]
end
