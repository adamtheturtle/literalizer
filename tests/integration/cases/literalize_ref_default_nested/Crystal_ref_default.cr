module Fixture_literalize_ref_default_nested_Crystal_ref_default
extend self
my_var = {
    "_" => "_",
}
item_var = {
    "_" => "_",
}
my_data = {
    "key" => my_var,
    "items" => [item_var, {"fallback" => "value"}],
}
end
