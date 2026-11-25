module Fixture_tuple_fields_with_nested_vectors_Crystal
extend self
my_data = {
    "lint" => [2, [] of String],
    "test" => [5, ["compile"]],
    "package" => [7, ["link", "test"]],
}
end
