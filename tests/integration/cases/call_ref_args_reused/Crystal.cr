module Fixture_call_ref_args_reused_Crystal
extend self
my_data = [
    [{"$ref" => "repeated_var"}, 1],
    [{"$ref" => "single_var"}, 0],
    [{"$ref" => "repeated_var"}, 8],
]
end
