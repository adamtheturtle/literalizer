set my_data [dict create \
    "true_to_one" [dict create "value" 1] \
    "one_to_true" [dict create "value" true] \
    "false_to_zero" [dict create "value" 0] \
    "zero_to_false" [dict create "value" false] \
    "nested_boolean_to_float" [dict create "value" [list 1.0]] \
    "nested_float_to_boolean" [dict create "value" [list false]] \
    "nested_value_types_changed" [dict create "value" [dict create "nested" [list true 0]]] \
    "nested_value_types_reversed" [dict create "value" [dict create "nested" [list 1 false]]] \
    "array_order_changed" [dict create "value" [list 2 1]] \
    "array_length_changed" [dict create "value" [list 1 2]] \
    "null_to_zero" [dict create "value" 0] \
    "string_to_boolean" [dict create "value" true] \
    "object_key_changed" [dict create "value" [dict create "b" 1]] \
]
