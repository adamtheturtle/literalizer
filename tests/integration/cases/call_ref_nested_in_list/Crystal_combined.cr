module Fixture_call_ref_nested_in_list_Crystal_combined
extend self
my_data = [
    [[{"$ref" => "my_var"}, 42, "static"]],
    [[{"$ref" => "my_other"}, 7, "label"]],
]
my_data = [
    [[{"$ref" => "my_var"}, 42, "static"]],
    [[{"$ref" => "my_other"}, 7, "label"]],
]
end
