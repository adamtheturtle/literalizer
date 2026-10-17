module Fixture_literalize_ref_nonstring_names_Crystal_ref
extend self
actual = {
    "_" => "_",
}
my_data = [
    {"$ref" => 1},
    {"$ref" => nil},
    actual,
]
end
