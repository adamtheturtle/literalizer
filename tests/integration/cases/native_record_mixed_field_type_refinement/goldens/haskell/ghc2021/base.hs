module Fixture_native_record_mixed_field_type_refinement_Haskell where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("first", HMap [("items", HList [1, HMap [("value", 2)]])]),
    ("second", HMap [("items", HList [1, HMap [("value", HStr "s")]])])
    ]
main :: IO ()
main = seq my_data (return ())
