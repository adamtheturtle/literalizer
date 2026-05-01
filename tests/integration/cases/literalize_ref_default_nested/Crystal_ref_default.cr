module Fixture_literalize_ref_default_nested_Crystal_ref_default
extend self
item_var = {
    "_" => "_",
}
my_data = {
    "items" => [item_var, {"fallback" => "value"}],
}
end
