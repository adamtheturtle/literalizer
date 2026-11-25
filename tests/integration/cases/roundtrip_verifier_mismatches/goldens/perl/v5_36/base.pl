use JSON::PP;
my $my_data = {
    "true_to_one" => {"value" => 1},
    "one_to_true" => {"value" => JSON::PP::true},
    "false_to_zero" => {"value" => 0},
    "zero_to_false" => {"value" => JSON::PP::false},
    "nested_boolean_to_float" => {"value" => [(0.0 + 1.0)]},
    "nested_float_to_boolean" => {"value" => [JSON::PP::false]},
    "nested_value_types_changed" => {"value" => {"nested" => [JSON::PP::true, 0]}},
    "nested_value_types_reversed" => {"value" => {"nested" => [1, JSON::PP::false]}},
    "array_order_changed" => {"value" => [2, 1]},
    "array_length_changed" => {"value" => [1, 2]},
    "null_to_zero" => {"value" => 0},
    "string_to_boolean" => {"value" => JSON::PP::true},
    "object_key_changed" => {"value" => {"b" => 1}},
};
