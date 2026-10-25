require "set"
module Fixture_empty_sequence_and_integer_set_fields_Crystal
extend self
my_data = {
    "a" => [] of Nil,
    "b" => Set{1, 2},
}
end
