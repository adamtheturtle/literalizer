module Fixture_literalize_ref_deep_nesting_Crystal
extend self
my_data = {
    "a" => {"b" => {"c" => {"$ref" => "deep"}}},
}
end
