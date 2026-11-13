module [my_data]

Val : [
    RBool Bool,
    RInt I128,
    RFloat F64,
    RStr Str,
    RList (List Val),
    RDict (List (Str, Val)),
]

my_data : Val
my_data = RDict [
    ("true_to_one", RDict [("value", RInt 1i128)]),
    ("one_to_true", RDict [("value", RBool Bool.true)]),
    ("false_to_zero", RDict [("value", RInt 0i128)]),
    ("zero_to_false", RDict [("value", RBool Bool.false)]),
    ("nested_boolean_to_float", RDict [("value", RList [RFloat 1.0])]),
    ("nested_float_to_boolean", RDict [("value", RList [RBool Bool.false])]),
    ("nested_value_types_changed", RDict [("value", RDict [("nested", RList [RBool Bool.true, RInt 0i128])])]),
    ("nested_value_types_reversed", RDict [("value", RDict [("nested", RList [RInt 1i128, RBool Bool.false])])]),
    ("array_order_changed", RDict [("value", RList [RInt 2i128, RInt 1i128])]),
    ("array_length_changed", RDict [("value", RList [RInt 1i128, RInt 2i128])]),
    ("null_to_zero", RDict [("value", RInt 0i128)]),
    ("string_to_boolean", RDict [("value", RBool Bool.true)]),
    ("object_key_changed", RDict [("value", RDict [("b", RInt 1i128)])]),
]
