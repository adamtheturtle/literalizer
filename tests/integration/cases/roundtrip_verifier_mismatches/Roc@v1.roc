Val := [
    RBool(Bool),
    RInt(I128),
    RFloat(F64),
    RStr(Str),
    RList(List(Val)),
    RDict(List((Str, Val))),
]

my_data : Val
my_data = RDict([
    ("true_to_one", RDict([("value", RInt(1.I128))])),
    ("one_to_true", RDict([("value", RBool(Bool.True))])),
    ("false_to_zero", RDict([("value", RInt(0.I128))])),
    ("zero_to_false", RDict([("value", RBool(Bool.False))])),
    ("nested_boolean_to_float", RDict([("value", RList([RFloat(1.0.F64)]))])),
    ("nested_float_to_boolean", RDict([("value", RList([RBool(Bool.False)]))])),
    ("nested_value_types_changed", RDict([("value", RDict([("nested", RList([RBool(Bool.True), RInt(0.I128)]))]))])),
    ("nested_value_types_reversed", RDict([("value", RDict([("nested", RList([RInt(1.I128), RBool(Bool.False)]))]))])),
    ("array_order_changed", RDict([("value", RList([RInt(2.I128), RInt(1.I128)]))])),
    ("array_length_changed", RDict([("value", RList([RInt(1.I128), RInt(2.I128)]))])),
    ("null_to_zero", RDict([("value", RInt(0.I128))])),
    ("string_to_boolean", RDict([("value", RBool(Bool.True))])),
    ("object_key_changed", RDict([("value", RDict([("b", RInt(1.I128))]))])),
])

main! = |_args| {
    _ = my_data
    Ok({})
}
