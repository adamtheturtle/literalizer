module Fixture_raku_single_element_containers_Crystal
extend self
my_data = {
    "single_map" => [{} of String => String],
    "single_list" => [[1]],
    "single_deep" => [[[2]]],
}
end
