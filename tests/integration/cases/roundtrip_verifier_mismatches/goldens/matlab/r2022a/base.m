my_data = struct(
    'true_to_one', struct('value', 1),
    'one_to_true', struct('value', true),
    'false_to_zero', struct('value', 0),
    'zero_to_false', struct('value', false),
    'nested_boolean_to_float', struct('value', {{1.0}}),
    'nested_float_to_boolean', struct('value', {{false}}),
    'nested_value_types_changed', struct('value', struct('nested', {{true, 0}})),
    'nested_value_types_reversed', struct('value', struct('nested', {{1, false}})),
    'array_order_changed', struct('value', {{2, 1}}),
    'array_length_changed', struct('value', {{1, 2}}),
    'null_to_zero', struct('value', 0),
    'string_to_boolean', struct('value', true),
    'object_key_changed', struct('value', struct('b', 1))
);
