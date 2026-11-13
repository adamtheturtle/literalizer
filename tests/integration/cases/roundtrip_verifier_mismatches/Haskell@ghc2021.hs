module Fixture_roundtrip_verifier_mismatches_Haskell where
data Val = HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("true_to_one", HMap [("value", 1)]),
    ("one_to_true", HMap [("value", HBool True)]),
    ("false_to_zero", HMap [("value", 0)]),
    ("zero_to_false", HMap [("value", HBool False)]),
    ("nested_boolean_to_float", HMap [("value", HList [1.0])]),
    ("nested_float_to_boolean", HMap [("value", HList [HBool False])]),
    ("nested_value_types_changed", HMap [("value", HMap [("nested", HList [HBool True, 0])])]),
    ("nested_value_types_reversed", HMap [("value", HMap [("nested", HList [1, HBool False])])]),
    ("array_order_changed", HMap [("value", HList [2, 1])]),
    ("array_length_changed", HMap [("value", HList [1, 2])]),
    ("null_to_zero", HMap [("value", 0)]),
    ("string_to_boolean", HMap [("value", HBool True)]),
    ("object_key_changed", HMap [("value", HMap [("b", 1)])])
    ]
main :: IO ()
main = seq my_data (return ())
