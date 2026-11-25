module Fixture_empty_map_nested_value_Crystal_sequence_tuple
extend self
my_data = {
     { {"mapping" => {} of String => String},  {} of String => String},
     { {} of String => String,  {"mapping" => {} of String => String}},
}
end
