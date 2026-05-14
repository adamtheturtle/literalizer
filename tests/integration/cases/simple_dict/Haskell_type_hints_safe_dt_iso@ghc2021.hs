module Fixture_simple_dict_Haskell_type_hints_safe_dt_iso where
data Val = HNull | HBool Bool | HInt Integer | HStr String | HMap [(String, Val)]
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
    ("name", HStr "Alice"),
    ("age", 30),
    ("active", HBool True),
    ("score", HNull)
    ]
main :: IO ()
main = seq my_data (return ())
