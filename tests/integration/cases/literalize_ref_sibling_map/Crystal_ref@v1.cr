module Fixture_literalize_ref_sibling_map_Crystal_ref
extend self
sibling_map = {
    "k" => 2,
}
my_data = [
    {"k" => 1},
    sibling_map,
]
end
