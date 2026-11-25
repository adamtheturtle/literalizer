module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("true_to_one", FMap [("value", FInt 1L)]);
    ("one_to_true", FMap [("value", FBool true)]);
    ("false_to_zero", FMap [("value", FInt 0L)]);
    ("zero_to_false", FMap [("value", FBool false)]);
    ("nested_boolean_to_float", FMap [("value", FList [FFloat 1.0])]);
    ("nested_float_to_boolean", FMap [("value", FList [FBool false])]);
    ("nested_value_types_changed", FMap [("value", FMap [("nested", FList [FBool true; FInt 0L])])]);
    ("nested_value_types_reversed", FMap [("value", FMap [("nested", FList [FInt 1L; FBool false])])]);
    ("array_order_changed", FMap [("value", FList [FInt 2L; FInt 1L])]);
    ("array_length_changed", FMap [("value", FList [FInt 1L; FInt 2L])]);
    ("null_to_zero", FMap [("value", FInt 0L)]);
    ("string_to_boolean", FMap [("value", FBool true)]);
    ("object_key_changed", FMap [("value", FMap [("b", FInt 1L)])])
]
