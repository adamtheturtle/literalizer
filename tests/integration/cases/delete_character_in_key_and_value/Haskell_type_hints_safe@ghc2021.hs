module Fixture_delete_character_in_key_and_value_Haskell_type_hints_safe where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
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
    ("v", HStr "a\x7f\&b"),
    ("a\x7f\&b", 1)
    ]
main :: IO ()
main = seq my_data (return ())
