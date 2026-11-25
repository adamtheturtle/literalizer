module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EFloat Float
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("true_to_one", EDict [("value", EInt 1)]),
    ("one_to_true", EDict [("value", EBool True)]),
    ("false_to_zero", EDict [("value", EInt 0)]),
    ("zero_to_false", EDict [("value", EBool False)]),
    ("nested_boolean_to_float", EDict [("value", EList (EFloat 1.0 :: []))]),
    ("nested_float_to_boolean", EDict [("value", EList (EBool False :: []))]),
    ("nested_value_types_changed", EDict [("value", EDict [("nested", EList [EBool True, EInt 0])])]),
    ("nested_value_types_reversed", EDict [("value", EDict [("nested", EList [EInt 1, EBool False])])]),
    ("array_order_changed", EDict [("value", EList [EInt 2, EInt 1])]),
    ("array_length_changed", EDict [("value", EList [EInt 1, EInt 2])]),
    ("null_to_zero", EDict [("value", EInt 0)]),
    ("string_to_boolean", EDict [("value", EBool True)]),
    ("object_key_changed", EDict [("value", EDict [("b", EInt 1)])])
    ]
