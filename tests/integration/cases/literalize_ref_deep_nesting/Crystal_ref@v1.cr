module Fixture_literalize_ref_deep_nesting_Crystal_ref
extend self
deep = {
    "_" => "_",
}
my_data = {
    "a" => {"b" => {"c" => deep}},
}
end
