datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SReal of real
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("true_to_one", SMap [("value", SInt 1)]),
    ("one_to_true", SMap [("value", SBool true)]),
    ("false_to_zero", SMap [("value", SInt 0)]),
    ("zero_to_false", SMap [("value", SBool false)]),
    ("nested_boolean_to_float", SMap [("value", SList [SReal 1.0])]),
    ("nested_float_to_boolean", SMap [("value", SList [SBool false])]),
    ("nested_value_types_changed", SMap [("value", SMap [("nested", SList [SBool true, SInt 0])])]),
    ("nested_value_types_reversed", SMap [("value", SMap [("nested", SList [SInt 1, SBool false])])]),
    ("array_order_changed", SMap [("value", SList [SInt 2, SInt 1])]),
    ("array_length_changed", SMap [("value", SList [SInt 1, SInt 2])]),
    ("null_to_zero", SMap [("value", SInt 0)]),
    ("string_to_boolean", SMap [("value", SBool true)]),
    ("object_key_changed", SMap [("value", SMap [("b", SInt 1)])])
]
val _ = my_data
