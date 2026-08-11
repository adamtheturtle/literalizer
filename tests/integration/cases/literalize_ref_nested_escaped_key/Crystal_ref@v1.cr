module Fixture_literalize_ref_nested_escaped_key_Crystal_ref
extend self
foo = {
    "_" => "_",
}
my_data = {
    "items" => [{"other" => 1}, foo],
    "mapping" => {"value" => foo},
}
end
