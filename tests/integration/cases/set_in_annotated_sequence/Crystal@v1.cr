require "set"
module Fixture_set_in_annotated_sequence_Crystal
extend self
my_data = [
    Set(String).new,
    Set{1, 2},
    [] of Nil,
]
end
