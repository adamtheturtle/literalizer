module Fixture_empty_map_nested_list_value_Crystal_sequence_tuple
extend self
my_data = {
     { {"values" => {Tuple.new}},  {} of String => String},
     { {} of String => String,  {"values" => {Tuple.new}}},
}
end
